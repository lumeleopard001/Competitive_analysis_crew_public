"""
Pydantic models for competitive analysis data structures.

This module provides comprehensive data models for the competitive analysis crew,
ensuring type safety and data validation throughout the workflow.
"""

from .company import CompanyProfile, FinancialData, NewsItem
from .analysis import CompetitiveAnalysisReport, CompetitiveLandscape, MarketAnalysis, Recommendation
from .research import ResearchDossier, MarketContext, ResearchMetadata
from .validation import ValidationCriteria, ValidationResult

__all__ = [
    "CompanyProfile",
    "FinancialData", 
    "NewsItem",
    "CompetitiveAnalysisReport",
    "CompetitiveLandscape",
    "MarketAnalysis",
    "Recommendation",
    "ResearchDossier",
    "MarketContext",
    "ResearchMetadata",
    "ValidationCriteria",
    "ValidationResult",
]