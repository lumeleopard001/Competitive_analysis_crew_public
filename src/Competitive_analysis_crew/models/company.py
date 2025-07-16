"""
Company-related data models for competitive analysis.

This module defines data structures for representing companies, their financial data,
and related information used throughout the competitive analysis process.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class CompanySize(str, Enum):
    """Enumeration for company size categories."""
    STARTUP = "startup"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    ENTERPRISE = "enterprise"


class NewsItem(BaseModel):
    """Represents a news item related to a company."""
    
    title: str = Field(..., description="News article title")
    summary: str = Field(..., description="Brief summary of the news")
    source: str = Field(..., description="News source")
    url: Optional[str] = Field(None, description="URL to the full article")
    published_date: Optional[datetime] = Field(None, description="Publication date")
    relevance_score: Optional[float] = Field(
        None, 
        ge=0.0, 
        le=1.0, 
        description="Relevance score from 0.0 to 1.0"
    )
    
    @validator('relevance_score')
    def validate_relevance_score(cls, v):
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError('Relevance score must be between 0.0 and 1.0')
        return v


class FinancialData(BaseModel):
    """Represents financial information for a company."""
    
    revenue: Optional[str] = Field(None, description="Annual revenue")
    revenue_growth: Optional[str] = Field(None, description="Revenue growth rate")
    employees: Optional[int] = Field(None, ge=0, description="Number of employees")
    funding: Optional[str] = Field(None, description="Total funding raised")
    valuation: Optional[str] = Field(None, description="Company valuation")
    profitability: Optional[str] = Field(None, description="Profitability status")
    market_cap: Optional[str] = Field(None, description="Market capitalization")
    fiscal_year: Optional[int] = Field(None, description="Fiscal year for the data")
    
    @validator('employees')
    def validate_employees(cls, v):
        if v is not None and v < 0:
            raise ValueError('Number of employees cannot be negative')
        return v
    
    @validator('fiscal_year')
    def validate_fiscal_year(cls, v):
        if v is not None:
            current_year = datetime.now().year
            if v < 1900 or v > current_year + 1:
                raise ValueError(f'Fiscal year must be between 1900 and {current_year + 1}')
        return v


class CompanyProfile(BaseModel):
    """
    Comprehensive profile of a company for competitive analysis.
    
    This model represents all relevant information about a company
    that is needed for competitive analysis and market research.
    """
    
    name: str = Field(..., description="Company name")
    industry: str = Field(..., description="Primary industry")
    size: Optional[CompanySize] = Field(None, description="Company size category")
    headquarters: Optional[str] = Field(None, description="Headquarters location")
    founded: Optional[int] = Field(None, description="Year founded")
    website: Optional[str] = Field(None, description="Company website URL")
    
    # Business information
    key_products: List[str] = Field(
        default_factory=list, 
        description="List of key products or services"
    )
    business_model: Optional[str] = Field(None, description="Business model description")
    target_market: Optional[str] = Field(None, description="Primary target market")
    geographic_presence: List[str] = Field(
        default_factory=list,
        description="Geographic markets where company operates"
    )
    
    # Recent information
    recent_news: List[NewsItem] = Field(
        default_factory=list,
        description="Recent news items about the company"
    )
    financial_highlights: Optional[FinancialData] = Field(
        None,
        description="Financial information and highlights"
    )
    
    # Competitive positioning
    market_position: Optional[str] = Field(None, description="Market position description")
    competitive_advantages: List[str] = Field(
        default_factory=list,
        description="Key competitive advantages"
    )
    key_partnerships: List[str] = Field(
        default_factory=list,
        description="Strategic partnerships"
    )
    
    # Additional metadata
    description: Optional[str] = Field(None, description="Company description")
    leadership: Dict[str, str] = Field(
        default_factory=dict,
        description="Key leadership positions and names"
    )
    social_media: Dict[str, str] = Field(
        default_factory=dict,
        description="Social media profiles"
    )
    
    # Analysis metadata
    last_updated: datetime = Field(
        default_factory=datetime.now,
        description="When this profile was last updated"
    )
    data_sources: List[str] = Field(
        default_factory=list,
        description="Sources used to compile this profile"
    )
    confidence_score: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Confidence score for the data accuracy"
    )
    
    @validator('founded')
    def validate_founded_year(cls, v):
        if v is not None:
            current_year = datetime.now().year
            if v < 1800 or v > current_year:
                raise ValueError(f'Founded year must be between 1800 and {current_year}')
        return v
    
    @validator('confidence_score')
    def validate_confidence_score(cls, v):
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError('Confidence score must be between 0.0 and 1.0')
        return v
    
    @validator('website')
    def validate_website_url(cls, v):
        if v is not None and v.strip():
            if not (v.startswith('http://') or v.startswith('https://')):
                v = f'https://{v}'
        return v
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "name": "TechCorp Inc.",
                "industry": "Software Technology",
                "size": "large",
                "headquarters": "San Francisco, CA",
                "founded": 2010,
                "website": "https://techcorp.com",
                "key_products": ["Cloud Platform", "AI Tools", "Analytics Suite"],
                "business_model": "SaaS subscription with enterprise licensing",
                "target_market": "Enterprise and mid-market businesses",
                "geographic_presence": ["North America", "Europe", "Asia-Pacific"],
                "market_position": "Leading provider in cloud analytics space",
                "competitive_advantages": ["Advanced AI capabilities", "Strong enterprise relationships"],
                "confidence_score": 0.85
            }
        }