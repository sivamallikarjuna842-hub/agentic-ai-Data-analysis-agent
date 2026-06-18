"""
Data Analyst Agent - Supports Groq (primary) with OpenAI fallback
"""
import json
import logging
import time
from typing import Any, Dict, List, Optional
from datetime import datetime

import pandas as pd
import numpy as np
import plotly.express as px
from langchain_core.messages import HumanMessage, SystemMessage

from config import config
from models import (
    Analysis, SQLGeneration, QueryResult, Visualization, Interpretation,
    ChartType, QueryStatus
)
from database import get_db_manager

logger = logging.getLogger(__name__)


class DataAnalystAgent:
    """Data Analyst Agent - processes natural language questions about data"""

    def __init__(self):
        """Initialize the agent - prefers Groq, falls back to OpenAI"""
        self.db_manager = get_db_manager()

        # Use Groq if API key is configured
        if config.GROQ_API_KEY and not config.GROQ_API_KEY.startswith("gsk_YOUR"):
            try:
                from langchain_groq import ChatGroq
                self.llm = ChatGroq(
                    model=config.GROQ_MODEL,
                    temperature=config.LLM_TEMPERATURE,
                    api_key=config.GROQ_API_KEY
                )
                logger.info(f"✓ Using Groq LLM (model: {config.GROQ_MODEL})")
            except Exception as e:
                logger.warning(f"Failed to init ChatGroq: {e}, falling back to OpenAI")
                self._init_openai()
        else:
            self._init_openai()

    def _init_openai(self):
        """Initialize with OpenAI fallback"""
        from langchain_openai import ChatOpenAI
        self.llm = ChatOpenAI(
            model=config.OPENAI_MODEL,
            temperature=config.LLM_TEMPERATURE,
            api_key=config.OPENAI_API_KEY
        )
        logger.info(f"Using OpenAI LLM (model: {config.OPENAI_MODEL})")

    async def analyze(
        self,
        question: str,
        conversation_history: Optional[List[Dict]] = None,
        user_id: Optional[str] = None
    ) -> Analysis:
        """
        Run complete analysis workflow

        Args:
            question: Natural language question
            conversation_history: Previous messages for context
            user_id: User identifier

        Returns:
            Complete analysis result
        """
        start_time = time.time()
        analysis_id = f"a_{int(time.time() * 1000)}"

        try:
            # Step 1: Generate SQL
            sql_generation = self._generate_sql(question)

            # Step 2: Execute query
            query_result = self._execute_query(sql_generation.sql)

            # Step 3: Create visualization (if data exists)
            visualization = None
            if query_result.status == QueryStatus.SUCCESS and query_result.rows:
                visualization = self._create_visualization(
                    question,
                    query_result.rows
                )

            # Step 4: Generate interpretation
            interpretation = self._generate_interpretation(
                question,
                query_result.rows,
                sql_generation
            )

            # Calculate execution time
            execution_time_ms = (time.time() - start_time) * 1000

            return Analysis(
                analysis_id=analysis_id,
                timestamp=datetime.now(),
                question=question,
                sql_generation=sql_generation,
                query_result=query_result,
                visualization=visualization,
                interpretation=interpretation,
                execution_time_ms=execution_time_ms
            )

        except Exception as e:
            logger.error(f"Analysis error: {e}")
            raise

    def _generate_sql(self, question: str) -> SQLGeneration:
        """Generate SQL from natural language question using LLM"""
        schema = self.db_manager.get_schema()
        schema_str = json.dumps(schema, indent=2)

        prompt = f"""Based on the database schema below, generate a SQL query for this question:

Question: {question}

Database Schema:
{schema_str}

Generate a safe, efficient SQL query. Respond with ONLY valid SQL, no explanations."""

        try:
            response = self.llm.invoke([
                SystemMessage(content="You are an expert SQL developer."),
                HumanMessage(content=prompt)
            ])

            sql = response.content.strip()
            if sql.startswith("```"):
                sql = sql.split("```")[1]
                if sql.startswith("sql"):
                    sql = sql[3:]
            sql = sql.strip()

        except Exception as e:
            logger.warning(f"LLM SQL generation failed: {e}, using fallback")
            sql = self._fallback_sql_generation(question)

        return SQLGeneration(
            sql=sql,
            confidence=0.85,
            pattern_type="dynamic",
            explanation=f"Generated SQL query to answer: {question}"
        )

    def _fallback_sql_generation(self, question: str) -> str:
        """Fallback SQL generation when LLM is unavailable"""
        q = question.lower()

        if "total" in q and "revenue" in q:
            if "category" in q:
                return ("SELECT p.category, SUM(s.revenue) as total_revenue, COUNT(*) as transactions "
                        "FROM sales s JOIN products p ON s.product_id = p.id "
                        "GROUP BY p.category ORDER BY total_revenue DESC LIMIT 10")
            if "product" in q:
                return ("SELECT p.name, SUM(s.revenue) as total_revenue, SUM(s.quantity) as total_quantity "
                        "FROM sales s JOIN products p ON s.product_id = p.id "
                        "GROUP BY p.id, p.name ORDER BY total_revenue DESC LIMIT 10")
            if "segment" in q:
                return ("SELECT s.segment, SUM(s.revenue) as total_revenue, COUNT(*) as transaction_count "
                        "FROM sales s GROUP BY s.segment ORDER BY total_revenue DESC")
            return "SELECT SUM(revenue) as total_revenue FROM sales"

        if "sales" in q and ("date" in q or "daily" in q or "trend" in q or "day" in q):
            return ("SELECT s.date, SUM(s.revenue) as daily_revenue, SUM(s.quantity) as daily_quantity "
                    "FROM sales s GROUP BY s.date ORDER BY s.date ASC")

        if "top" in q and "product" in q:
            return ("SELECT p.name, SUM(s.revenue) as total_revenue, SUM(s.quantity) as total_quantity "
                    "FROM sales s JOIN products p ON s.product_id = p.id "
                    "GROUP BY p.id, p.name ORDER BY total_revenue DESC LIMIT 5")

        if "average" in q and "price" in q:
            return ("SELECT category, AVG(price) as avg_price, COUNT(*) as product_count "
                    "FROM products GROUP BY category ORDER BY avg_price DESC")

        if "segment" in q:
            return ("SELECT segment, COUNT(*) as customer_count, SUM(revenue) as total_revenue "
                    "FROM sales GROUP BY segment ORDER BY total_revenue DESC")

        return "SELECT * FROM sales ORDER BY date DESC LIMIT 10"

    def _execute_query(self, sql: str) -> QueryResult:
        """Execute SQL query"""
        start_time = time.time()
        result = self.db_manager.execute_query(sql)
        execution_time_ms = (time.time() - start_time) * 1000

        if result["success"]:
            return QueryResult(
                query_id=f"q_{int(time.time() * 1000)}",
                status=QueryStatus.SUCCESS,
                rows=result["data"],
                row_count=result["row_count"],
                execution_time_ms=execution_time_ms
            )
        else:
            return QueryResult(
                query_id=f"q_{int(time.time() * 1000)}",
                status=QueryStatus.FAILED,
                rows=[],
                row_count=0,
                execution_time_ms=execution_time_ms,
                error=result.get("error")
            )

    def _create_visualization(self, question: str, data: List[Dict]) -> Optional[Visualization]:
        """Create visualization from data"""
        try:
            df = pd.DataFrame(data)
            chart_type = self._select_chart_type(question, df)
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

            if numeric_cols and non_numeric_cols:
                x_key = non_numeric_cols[0]
                y_key = numeric_cols[0]
            elif numeric_cols:
                x_key = numeric_cols[0]
                y_key = numeric_cols[1] if len(numeric_cols) > 1 else numeric_cols[0]
            else:
                return None

            if chart_type == ChartType.BAR:
                fig = px.bar(df, x=x_key, y=y_key)
            elif chart_type == ChartType.LINE:
                fig = px.line(df, x=x_key, y=y_key)
            elif chart_type == ChartType.PIE:
                fig = px.pie(df, names=x_key, values=y_key)
            elif chart_type == ChartType.AREA:
                fig = px.area(df, x=x_key, y=y_key)
            else:
                fig = px.bar(df, x=x_key, y=y_key)

            return Visualization(
                type=chart_type,
                title=f"Analysis: {question[:50]}...",
                x_axis=x_key, y_axis=y_key,
                x_key=x_key, y_key=y_key,
                interactive_html=fig.to_html()
            )
        except Exception as e:
            logger.warning(f"Visualization creation failed: {e}")
            return None

    def _select_chart_type(self, question: str, df: pd.DataFrame) -> ChartType:
        q = question.lower()
        if any(w in q for w in ["trend", "over time", "daily", "weekly", "monthly"]):
            return ChartType.LINE
        if any(w in q for w in ["distribution", "proportion", "breakdown", "percentage"]):
            return ChartType.PIE
        if any(w in q for w in ["cumulative", "stacked"]):
            return ChartType.AREA
        return ChartType.BAR

    def _generate_interpretation(self, question: str, rows: List[Dict], sql_generation: SQLGeneration) -> Interpretation:
        """Generate interpretation of results"""
        if not rows:
            return Interpretation(
                summary="No data found matching your query.",
                key_metrics={}, patterns=[], anomalies=[],
                recommendations=[],
                next_steps=["Try refining your question with different criteria"],
                confidence=0.0
            )

        df = pd.DataFrame(rows)
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        summary_parts = [f"Analysis of {len(rows)} records completed."]
        patterns, anomalies, recommendations = [], [], []

        if numeric_cols:
            for col in numeric_cols[:3]:
                total = df[col].sum()
                avg = df[col].mean()
                mx = df[col].max()
                mn = df[col].min()
                summary_parts.append(f"Total {col}: {total:,.0f} (avg: {avg:,.0f}, range: {mn:,.0f} - {mx:,.0f}).")
                if mx > avg * 1.5:
                    patterns.append(f"High variance in {col} with peaks exceeding average by more than 50%")
                    anomalies.append(f"Some {col} values are significantly above the average")

            if "revenue" in str(numeric_cols).lower():
                recommendations.append("Focus on top-performing categories to maximize revenue growth")
                recommendations.append("Consider analyzing low-performing segments for improvement opportunities")
                next_steps = ["Drill down into specific product categories",
                              "Compare performance across different time periods",
                              "Analyze customer segment profitability"]
            else:
                next_steps = ["Ask more specific questions about revenue or sales trends",
                              "Explore the data by different categories",
                              "Request a detailed breakdown by time period"]
        else:
            next_steps = ["Ask about numerical metrics like revenue or sales",
                          "Request category-based breakdowns"]

        summary = " ".join(summary_parts)

        # Try LLM enhancement
        try:
            data_summary = {"row_count": len(df), "columns": df.columns.tolist(), "sample_data": rows[:5]}
            prompt = f"""Analyze this data and provide a brief insight:

Question: {question}
Data Summary: {json.dumps(data_summary, default=str)}
SQL Used: {sql_generation.sql}

Provide a professional analysis in JSON format:
{{
    "summary": "2-3 sentence summary of findings",
    "key_metrics": {{"metric_name": value}},
    "patterns": ["pattern1", "pattern2"],
    "anomalies": ["anomaly1"],
    "recommendations": ["recommendation1", "recommendation2"],
    "next_steps": ["analysis1", "analysis2"]
}}"""

            response = self.llm.invoke([
                SystemMessage(content="You are an expert business analyst."),
                HumanMessage(content=prompt)
            ])
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            data = json.loads(content)
            return Interpretation(
                summary=data.get("summary", summary),
                key_metrics=data.get("key_metrics", {}),
                patterns=data.get("patterns", patterns),
                anomalies=data.get("anomalies", anomalies),
                recommendations=data.get("recommendations", recommendations),
                next_steps=data.get("next_steps", next_steps),
                confidence=0.90
            )
        except Exception as e:
            logger.warning(f"LLM interpretation failed: {e}, using programmatic")
            key_metrics = {}
            if numeric_cols:
                for col in numeric_cols[:5]:
                    key_metrics[f"total_{col}"] = float(df[col].sum())
                    key_metrics[f"avg_{col}"] = float(df[col].mean())
            return Interpretation(
                summary=summary, key_metrics=key_metrics,
                patterns=patterns or ["Standard distribution across records"],
                anomalies=anomalies or ["No significant anomalies detected"],
                recommendations=recommendations or ["Review the visualization for detailed insights"],
                next_steps=next_steps, confidence=0.7
            )


# Global agent instance
_agent_instance: Optional[DataAnalystAgent] = None


def get_agent() -> DataAnalystAgent:
    """Get or create agent instance"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = DataAnalystAgent()
    return _agent_instance