"""
Research-related data models for competitive analysis workflow.

This module defines data structures for research context, metadata,
and the overall research dossier used throughout the analysis process.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any, Set
from pydantic import BaseModel, Field, validator
from enum import Enum

from .company import CompanyProfile


class ResearchScope(str, Enum):
    """Defines the scope of research to be conducted."""
    BASIC = "basic"
    COMPREHENSIVE = "comprehensive"
    DEEP_DIVE = "deep_dive"
    COMPETITIVE_INTELLIGENCE = "competitive_intelligence"


class ResearchPriority(str, Enum):
    """Priority levels for research tasks."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class DataSource(BaseModel):
    """Represents a data source for research."""
    
    name: str = Field(..., description="Data source name")
    type: str = Field(..., description="Type of data source")
    url: Optional[str] = Field(None, description="Source URL if applicable")
    access_method: str = Field(..., description="How to access this source")
    reliability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Reliability score of the source"
    )
    cost: Optional[str] = Field(None, description="Cost to access if applicable")
    update_frequency: Optional[str] = Field(None, description="How often source is updated")
    
    @validator('reliability')
    def validate_reliability(cls, v):
        if v < 0.0 or v > 1.0:
            raise ValueError('Reliability must be between 0.0 and 1.0')
        return v


class ResearchQuestion(BaseModel):
    """Represents a specific research question to be answered."""
    
    question: str = Field(..., description="The research question")
    priority: ResearchPriority = Field(..., description="Priority level")
    category: str = Field(..., description="Question category")
    expected_sources: List[str] = Field(
        default_factory=list,
        description="Expected data sources for this question"
    )
    success_criteria: Optional[str] = Field(
        None,
        description="What constitutes a successful answer"
    )
    assigned_agent: Optional[str] = Field(None, description="Agent assigned to this question")
    status: str = Field(default="pending", description="Current status")


class MarketContext(BaseModel):
    """
    Provides market context for the competitive analysis.
    
    This model captures the broader market environment and conditions
    that influence the competitive landscape.
    """
    
    # Market definition
    market_name: str = Field(..., description="Name of the market being analyzed")
    market_definition: str = Field(..., description="Clear definition of the market scope")
    geographic_scope: List[str] = Field(
        default_factory=list,
        description="Geographic regions included in analysis"
    )
    time_period: str = Field(..., description="Time period for the analysis")
    
    # Market characteristics
    market_size: Optional[str] = Field(None, description="Total market size")
    growth_rate: Optional[str] = Field(None, description="Market growth rate")
    maturity_stage: Optional[str] = Field(None, description="Market maturity stage")
    seasonality: Optional[str] = Field(None, description="Seasonal patterns if any")
    
    # Economic context
    economic_conditions: Optional[str] = Field(
        None,
        description="Current economic conditions affecting the market"
    )
    regulatory_environment: List[str] = Field(
        default_factory=list,
        description="Key regulatory factors"
    )
    technological_trends: List[str] = Field(
        default_factory=list,
        description="Relevant technological trends"
    )
    
    # Customer context
    customer_segments: List[str] = Field(
        default_factory=list,
        description="Key customer segments"
    )
    buying_patterns: Optional[str] = Field(None, description="Customer buying patterns")
    decision_factors: List[str] = Field(
        default_factory=list,
        description="Key factors in customer decisions"
    )
    
    # Competitive dynamics
    competitive_intensity: Optional[str] = Field(
        None,
        description="Level of competitive intensity"
    )
    entry_barriers: List[str] = Field(
        default_factory=list,
        description="Barriers to market entry"
    )
    substitute_threats: List[str] = Field(
        default_factory=list,
        description="Threat of substitute products/services"
    )


class ResearchMetadata(BaseModel):
    """
    Metadata about the research process and parameters.
    
    This model tracks the research methodology, constraints,
    and quality parameters for the competitive analysis.
    """
    
    # Research parameters
    research_scope: ResearchScope = Field(..., description="Scope of research")
    start_date: datetime = Field(
        default_factory=datetime.now,
        description="Research start date"
    )
    target_completion: Optional[datetime] = Field(
        None,
        description="Target completion date"
    )
    budget_constraints: Optional[str] = Field(
        None,
        description="Budget constraints for research"
    )
    
    # Research questions
    primary_questions: List[ResearchQuestion] = Field(
        default_factory=list,
        description="Primary research questions"
    )
    secondary_questions: List[ResearchQuestion] = Field(
        default_factory=list,
        description="Secondary research questions"
    )
    
    # Data sources and methodology
    approved_sources: List[DataSource] = Field(
        default_factory=list,
        description="Approved data sources"
    )
    excluded_sources: List[str] = Field(
        default_factory=list,
        description="Sources to exclude from research"
    )
    research_methodology: str = Field(
        ...,
        description="Research methodology being used"
    )
    
    # Quality parameters
    minimum_confidence_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum confidence threshold for findings"
    )
    required_source_count: int = Field(
        default=3,
        ge=1,
        description="Minimum number of sources required per finding"
    )
    fact_checking_required: bool = Field(
        default=True,
        description="Whether fact-checking is required"
    )
    
    # Constraints and limitations
    time_constraints: Optional[str] = Field(None, description="Time constraints")
    resource_constraints: List[str] = Field(
        default_factory=list,
        description="Resource constraints"
    )
    access_limitations: List[str] = Field(
        default_factory=list,
        description="Access limitations for data sources"
    )
    
    # Progress tracking
    completion_percentage: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Research completion percentage"
    )
    milestones: Dict[str, bool] = Field(
        default_factory=dict,
        description="Research milestones and completion status"
    )
    
    @validator('minimum_confidence_threshold')
    def validate_confidence_threshold(cls, v):
        if v < 0.0 or v > 1.0:
            raise ValueError('Confidence threshold must be between 0.0 and 1.0')
        return v
    
    @validator('completion_percentage')
    def validate_completion_percentage(cls, v):
        if v < 0.0 or v > 100.0:
            raise ValueError('Completion percentage must be between 0.0 and 100.0')
        return v


class ResearchDossier(BaseModel):
    """
    Comprehensive research dossier for competitive analysis.
    
    This is the main research coordination model that contains all
    research context, parameters, and collected information for
    the competitive analysis project.
    """
    
    # Dossier identification
    dossier_id: str = Field(..., description="Unique identifier for this dossier")
    project_name: str = Field(..., description="Name of the research project")
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Dossier creation timestamp"
    )
    last_updated: datetime = Field(
        default_factory=datetime.now,
        description="Last update timestamp"
    )
    
    # Core research subjects
    client_company: Optional[CompanyProfile] = Field(
        None,
        description="Profile of the client company"
    )
    target_companies: List[str] = Field(
        default_factory=list,
        description="Names of companies to analyze"
    )
    competitors: List[CompanyProfile] = Field(
        default_factory=list,
        description="Detailed profiles of competitor companies"
    )
    
    # Research context and parameters
    market_context: MarketContext = Field(
        ...,
        description="Market context for the analysis"
    )
    research_metadata: ResearchMetadata = Field(
        ...,
        description="Research methodology and parameters"
    )
    
    # Research findings and insights
    key_findings: List[str] = Field(
        default_factory=list,
        description="Key research findings"
    )
    data_gaps: List[str] = Field(
        default_factory=list,
        description="Identified data gaps"
    )
    assumptions: List[str] = Field(
        default_factory=list,
        description="Research assumptions made"
    )
    
    # Quality and validation
    validation_notes: List[str] = Field(
        default_factory=list,
        description="Validation notes and checks performed"
    )
    confidence_assessment: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Overall confidence in research quality"
    )
    
    # Collaboration and workflow
    assigned_researchers: List[str] = Field(
        default_factory=list,
        description="Researchers assigned to this dossier"
    )
    review_status: str = Field(
        default="in_progress",
        description="Current review status"
    )
    approval_required: bool = Field(
        default=False,
        description="Whether approval is required before proceeding"
    )
    
    @validator('confidence_assessment')
    def validate_confidence_assessment(cls, v):
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError('Confidence assessment must be between 0.0 and 1.0')
        return v
    
    def update_timestamp(self):
        """Update the last_updated timestamp."""
        self.last_updated = datetime.now()
    
    def add_finding(self, finding: str):
        """Add a new key finding."""
        self.key_findings.append(finding)
        self.update_timestamp()
    
    def add_competitor(self, competitor: CompanyProfile):
        """Add a new competitor profile."""
        self.competitors.append(competitor)
        self.update_timestamp()
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "dossier_id": "CA-2024-001",
                "project_name": "Cloud Analytics Competitive Analysis",
                "target_companies": ["TechCorp", "DataSoft", "AnalyticsPro"],
                "review_status": "in_progress",
                "confidence_assessment": 0.85
            }
        }