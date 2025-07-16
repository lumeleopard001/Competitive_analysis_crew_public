"""
Analysis-related data models for competitive analysis reports.

This module defines data structures for competitive analysis reports,
market analysis, and recommendations.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum

from .company import CompanyProfile


class RecommendationType(str, Enum):
    """Types of recommendations that can be made."""
    STRATEGIC = "strategic"
    TACTICAL = "tactical"
    OPERATIONAL = "operational"
    INVESTMENT = "investment"
    PARTNERSHIP = "partnership"
    PRODUCT = "product"
    MARKETING = "marketing"


class RecommendationPriority(str, Enum):
    """Priority levels for recommendations."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Recommendation(BaseModel):
    """Represents a strategic recommendation from the analysis."""
    
    title: str = Field(..., description="Recommendation title")
    description: str = Field(..., description="Detailed recommendation description")
    type: RecommendationType = Field(..., description="Type of recommendation")
    priority: RecommendationPriority = Field(..., description="Priority level")
    rationale: str = Field(..., description="Reasoning behind the recommendation")
    
    # Implementation details
    expected_impact: Optional[str] = Field(None, description="Expected business impact")
    implementation_timeline: Optional[str] = Field(None, description="Suggested timeline")
    required_resources: List[str] = Field(
        default_factory=list,
        description="Resources needed for implementation"
    )
    success_metrics: List[str] = Field(
        default_factory=list,
        description="Metrics to measure success"
    )
    
    # Risk assessment
    risks: List[str] = Field(
        default_factory=list,
        description="Potential risks and challenges"
    )
    mitigation_strategies: List[str] = Field(
        default_factory=list,
        description="Risk mitigation strategies"
    )
    
    # Supporting data
    supporting_evidence: List[str] = Field(
        default_factory=list,
        description="Evidence supporting this recommendation"
    )
    related_companies: List[str] = Field(
        default_factory=list,
        description="Companies relevant to this recommendation"
    )


class MarketSegment(BaseModel):
    """Represents a market segment in the competitive landscape."""
    
    name: str = Field(..., description="Segment name")
    size: Optional[str] = Field(None, description="Market size")
    growth_rate: Optional[str] = Field(None, description="Growth rate")
    key_players: List[str] = Field(
        default_factory=list,
        description="Key players in this segment"
    )
    characteristics: List[str] = Field(
        default_factory=list,
        description="Key characteristics of this segment"
    )
    trends: List[str] = Field(
        default_factory=list,
        description="Current trends in this segment"
    )


class CompetitiveLandscape(BaseModel):
    """Represents the overall competitive landscape analysis."""
    
    market_overview: str = Field(..., description="High-level market overview")
    total_market_size: Optional[str] = Field(None, description="Total addressable market")
    market_growth_rate: Optional[str] = Field(None, description="Overall market growth rate")
    
    # Market segmentation
    segments: List[MarketSegment] = Field(
        default_factory=list,
        description="Market segments"
    )
    
    # Competitive dynamics
    competitive_intensity: Optional[str] = Field(
        None,
        description="Assessment of competitive intensity"
    )
    barriers_to_entry: List[str] = Field(
        default_factory=list,
        description="Barriers to market entry"
    )
    key_success_factors: List[str] = Field(
        default_factory=list,
        description="Critical success factors in the market"
    )
    
    # Market trends
    emerging_trends: List[str] = Field(
        default_factory=list,
        description="Emerging market trends"
    )
    disruptive_forces: List[str] = Field(
        default_factory=list,
        description="Potential disruptive forces"
    )
    regulatory_factors: List[str] = Field(
        default_factory=list,
        description="Regulatory considerations"
    )


class MarketAnalysis(BaseModel):
    """Detailed market analysis including positioning and opportunities."""
    
    market_positioning: Dict[str, str] = Field(
        default_factory=dict,
        description="Positioning of key players"
    )
    
    # Opportunity analysis
    market_opportunities: List[str] = Field(
        default_factory=list,
        description="Identified market opportunities"
    )
    white_space_analysis: Optional[str] = Field(
        None,
        description="Analysis of underserved market areas"
    )
    
    # Competitive gaps
    competitive_gaps: List[str] = Field(
        default_factory=list,
        description="Gaps in competitive offerings"
    )
    differentiation_opportunities: List[str] = Field(
        default_factory=list,
        description="Opportunities for differentiation"
    )
    
    # Market dynamics
    customer_needs: List[str] = Field(
        default_factory=list,
        description="Key customer needs and pain points"
    )
    buying_criteria: List[str] = Field(
        default_factory=list,
        description="Customer buying criteria"
    )
    decision_makers: List[str] = Field(
        default_factory=list,
        description="Key decision makers in the buying process"
    )
    
    # Pricing analysis
    pricing_models: Dict[str, str] = Field(
        default_factory=dict,
        description="Common pricing models in the market"
    )
    price_sensitivity: Optional[str] = Field(
        None,
        description="Market price sensitivity analysis"
    )


class Source(BaseModel):
    """Represents a data source used in the analysis."""
    
    name: str = Field(..., description="Source name")
    type: str = Field(..., description="Type of source (website, report, interview, etc.)")
    url: Optional[str] = Field(None, description="URL if applicable")
    date_accessed: datetime = Field(
        default_factory=datetime.now,
        description="When the source was accessed"
    )
    reliability_score: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Reliability score of the source"
    )
    
    @validator('reliability_score')
    def validate_reliability_score(cls, v):
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError('Reliability score must be between 0.0 and 1.0')
        return v


class CompetitiveAnalysisReport(BaseModel):
    """
    Comprehensive competitive analysis report.
    
    This is the main output model that contains all analysis results
    and recommendations for the competitive intelligence study.
    """
    
    # Report metadata
    title: str = Field(..., description="Report title")
    executive_summary: str = Field(..., description="Executive summary")
    generated_at: datetime = Field(
        default_factory=datetime.now,
        description="Report generation timestamp"
    )
    version: str = Field(default="1.0", description="Report version")
    
    # Core analysis content
    client_company: Optional[CompanyProfile] = Field(
        None,
        description="Profile of the client company"
    )
    company_profiles: List[CompanyProfile] = Field(
        default_factory=list,
        description="Profiles of analyzed companies"
    )
    competitive_landscape: CompetitiveLandscape = Field(
        ...,
        description="Competitive landscape analysis"
    )
    market_analysis: MarketAnalysis = Field(
        ...,
        description="Detailed market analysis"
    )
    
    # Recommendations and insights
    recommendations: List[Recommendation] = Field(
        default_factory=list,
        description="Strategic recommendations"
    )
    key_insights: List[str] = Field(
        default_factory=list,
        description="Key insights from the analysis"
    )
    
    # Methodology and sources
    methodology: str = Field(..., description="Analysis methodology used")
    sources: List[Source] = Field(
        default_factory=list,
        description="Data sources used in the analysis"
    )
    limitations: List[str] = Field(
        default_factory=list,
        description="Analysis limitations and caveats"
    )
    
    # Quality metrics
    confidence_level: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Overall confidence in the analysis"
    )
    completeness_score: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Completeness score of the analysis"
    )
    
    # Additional metadata
    analyst_notes: Optional[str] = Field(None, description="Additional analyst notes")
    next_steps: List[str] = Field(
        default_factory=list,
        description="Suggested next steps"
    )
    
    @validator('confidence_level', 'completeness_score')
    def validate_scores(cls, v):
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError('Score must be between 0.0 and 1.0')
        return v
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "title": "Competitive Analysis: Cloud Analytics Market",
                "executive_summary": "This report analyzes the competitive landscape...",
                "version": "1.0",
                "methodology": "Mixed-method approach combining desk research, web scraping, and market analysis",
                "confidence_level": 0.85,
                "completeness_score": 0.90
            }
        }