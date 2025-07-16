"""
Date Context Tool

This tool provides current date and time information to agents for accurate
temporal context in competitive analysis and financial data reporting.
"""

from datetime import datetime, timezone
from typing import Type, Optional
import structlog

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

# Initialize structured logging
logger = structlog.get_logger()


class DateContextInput(BaseModel):
    """Input schema for DateContextTool."""
    format_type: Optional[str] = Field(
        default="full",
        description="Format type: 'full', 'date_only', 'year', 'quarter', or 'fiscal'"
    )


class DateContextTool(BaseTool):
    """
    Tool for providing current date and time context to agents.
    
    This tool helps agents understand the current temporal context for:
    - Financial data analysis and reporting
    - Market trend analysis with proper time references
    - Ensuring research uses current/recent data
    - Proper contextualization of "recent" vs "historical" information
    """
    
    name: str = "DateContextTool"
    description: str = (
        "Get current date and time information for temporal context in analysis. "
        "Use this tool to understand what 'current', 'recent', and 'latest' mean "
        "in terms of actual dates for financial and market analysis."
    )
    args_schema: Type[BaseModel] = DateContextInput
    
    def _run(self, format_type: str = "full") -> str:
        """
        Get current date and time information.
        
        Args:
            format_type: Type of date format to return
                - 'full': Complete date and time with context
                - 'date_only': Just the current date
                - 'year': Current year only
                - 'quarter': Current quarter and year
                - 'fiscal': Current fiscal year context
        
        Returns:
            str: Formatted date/time information with context
        """
        try:
            now = datetime.now(timezone.utc)
            current_date = now.strftime("%B %d, %Y")
            current_time = now.strftime("%H:%M UTC")
            current_year = now.year
            current_month = now.month
            
            # Determine quarter
            quarter = (current_month - 1) // 3 + 1
            
            # Determine fiscal year context (assuming calendar year for most companies)
            fiscal_year = current_year
            
            if format_type == "date_only":
                result = f"Current date: {current_date}"
            elif format_type == "year":
                result = f"Current year: {current_year}"
            elif format_type == "quarter":
                result = f"Current quarter: Q{quarter} {current_year}"
            elif format_type == "fiscal":
                result = (
                    f"Current fiscal context: FY{fiscal_year}, Q{quarter} {current_year}. "
                    f"Note: Most companies follow calendar year fiscal cycles, but verify "
                    f"specific company fiscal year calendars for accurate financial analysis."
                )
            else:  # full format
                result = (
                    f"Current date and time: {current_date} at {current_time}\n"
                    f"Current year: {current_year}\n"
                    f"Current quarter: Q{quarter} {current_year}\n"
                    f"Fiscal year context: FY{fiscal_year}\n\n"
                    f"IMPORTANT CONTEXT FOR ANALYSIS:\n"
                    f"- When analyzing 'recent' financial data, focus on {current_year} and late {current_year-1}\n"
                    f"- 'Latest' quarterly data should be from Q{quarter} {current_year} or the most recent available\n"
                    f"- 'Current year' performance refers to {current_year} data\n"
                    f"- 'Previous year' refers to {current_year-1}\n"
                    f"- Data from {current_year-2} and earlier should be labeled as 'historical'\n"
                    f"- Always specify actual years (e.g., '{current_year}') rather than relative terms"
                )
            
            logger.info("Date context provided", format_type=format_type, current_year=current_year)
            return result
            
        except Exception as e:
            error_msg = f"Error getting date context: {str(e)}"
            logger.error("Date context tool error", error=str(e))
            return error_msg