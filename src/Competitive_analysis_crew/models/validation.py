"""
Validation-related data models for quality assurance.

This module defines data structures for validating reports and analysis quality,
ensuring enterprise-grade output standards.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class ValidationStatus(str, Enum):
    """Status of validation checks."""
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    SKIPPED = "skipped"


class ValidationSeverity(str, Enum):
    """Severity levels for validation issues."""
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ValidationCheck(BaseModel):
    """Represents a single validation check."""
    
    check_name: str = Field(..., description="Name of the validation check")
    description: str = Field(..., description="Description of what this check validates")
    status: ValidationStatus = Field(..., description="Status of this check")
    severity: ValidationSeverity = Field(..., description="Severity level")
    
    # Check results
    passed: bool = Field(..., description="Whether the check passed")
    score: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Numeric score for this check (0.0 to 1.0)"
    )
    message: Optional[str] = Field(None, description="Detailed message about the check")
    
    # Remediation
    suggestions: List[str] = Field(
        default_factory=list,
        description="Suggestions for improvement"
    )
    auto_fixable: bool = Field(
        default=False,
        description="Whether this issue can be automatically fixed"
    )
    
    # Metadata
    checked_at: datetime = Field(
        default_factory=datetime.now,
        description="When this check was performed"
    )
    checker_version: Optional[str] = Field(None, description="Version of the checker used")
    
    @validator('score')
    def validate_score(cls, v):
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError('Score must be between 0.0 and 1.0')
        return v


class ContentQualityCheck(ValidationCheck):
    """Specific validation check for content quality."""
    
    # Content-specific metrics
    word_count: Optional[int] = Field(None, ge=0, description="Word count")
    readability_score: Optional[float] = Field(
        None,
        ge=0.0,
        le=100.0,
        description="Readability score"
    )
    grammar_issues: int = Field(default=0, ge=0, description="Number of grammar issues")
    spelling_errors: int = Field(default=0, ge=0, description="Number of spelling errors")
    
    # Structure checks
    has_executive_summary: bool = Field(default=False, description="Has executive summary")
    has_recommendations: bool = Field(default=False, description="Has recommendations")
    has_methodology: bool = Field(default=False, description="Has methodology section")
    section_count: int = Field(default=0, ge=0, description="Number of sections")
    
    @validator('readability_score')
    def validate_readability_score(cls, v):
        if v is not None and (v < 0.0 or v > 100.0):
            raise ValueError('Readability score must be between 0.0 and 100.0')
        return v


class DataQualityCheck(ValidationCheck):
    """Specific validation check for data quality."""
    
    # Data completeness
    completeness_score: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Data completeness score"
    )
    missing_fields: List[str] = Field(
        default_factory=list,
        description="List of missing required fields"
    )
    
    # Data accuracy
    accuracy_score: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Data accuracy score"
    )
    inconsistencies: List[str] = Field(
        default_factory=list,
        description="Data inconsistencies found"
    )
    
    # Source validation
    source_count: int = Field(default=0, ge=0, description="Number of sources")
    verified_sources: int = Field(default=0, ge=0, description="Number of verified sources")
    source_reliability: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Average source reliability"
    )
    
    @validator('completeness_score', 'accuracy_score', 'source_reliability')
    def validate_scores(cls, v):
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError('Score must be between 0.0 and 1.0')
        return v


class ValidationCriteria(BaseModel):
    """
    Defines the criteria and thresholds for validation.
    
    This model specifies what constitutes acceptable quality
    for different aspects of the competitive analysis.
    """
    
    # Overall quality thresholds
    minimum_overall_score: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum overall quality score required"
    )
    critical_issues_allowed: int = Field(
        default=0,
        ge=0,
        description="Number of critical issues allowed"
    )
    
    # Content quality criteria
    minimum_word_count: int = Field(
        default=1000,
        ge=0,
        description="Minimum word count for reports"
    )
    maximum_grammar_errors: int = Field(
        default=5,
        ge=0,
        description="Maximum grammar errors allowed"
    )
    minimum_readability_score: float = Field(
        default=60.0,
        ge=0.0,
        le=100.0,
        description="Minimum readability score"
    )
    
    # Data quality criteria
    minimum_completeness: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Minimum data completeness required"
    )
    minimum_accuracy: float = Field(
        default=0.85,
        ge=0.0,
        le=1.0,
        description="Minimum data accuracy required"
    )
    minimum_source_count: int = Field(
        default=3,
        ge=1,
        description="Minimum number of sources required"
    )
    minimum_source_reliability: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum average source reliability"
    )
    
    # Structure requirements
    required_sections: List[str] = Field(
        default_factory=lambda: [
            "executive_summary",
            "methodology",
            "competitive_landscape",
            "recommendations"
        ],
        description="Required sections in the report"
    )
    
    # Business requirements
    minimum_companies_analyzed: int = Field(
        default=3,
        ge=1,
        description="Minimum number of companies to analyze"
    )
    minimum_recommendations: int = Field(
        default=3,
        ge=1,
        description="Minimum number of recommendations"
    )
    
    @validator('minimum_overall_score', 'minimum_completeness', 'minimum_accuracy', 'minimum_source_reliability')
    def validate_score_thresholds(cls, v):
        if v < 0.0 or v > 1.0:
            raise ValueError('Score thresholds must be between 0.0 and 1.0')
        return v
    
    @validator('minimum_readability_score')
    def validate_readability_threshold(cls, v):
        if v < 0.0 or v > 100.0:
            raise ValueError('Readability score must be between 0.0 and 100.0')
        return v


class ValidationResult(BaseModel):
    """
    Comprehensive validation result for a competitive analysis report.
    
    This model contains all validation checks, scores, and recommendations
    for improving the quality of the analysis.
    """
    
    # Validation metadata
    validation_id: str = Field(..., description="Unique validation identifier")
    validated_at: datetime = Field(
        default_factory=datetime.now,
        description="When validation was performed"
    )
    validator_version: str = Field(default="1.0", description="Version of validator used")
    
    # Overall results
    overall_status: ValidationStatus = Field(..., description="Overall validation status")
    overall_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Overall quality score"
    )
    passed: bool = Field(..., description="Whether validation passed overall")
    
    # Detailed checks
    content_checks: List[ContentQualityCheck] = Field(
        default_factory=list,
        description="Content quality validation checks"
    )
    data_checks: List[DataQualityCheck] = Field(
        default_factory=list,
        description="Data quality validation checks"
    )
    custom_checks: List[ValidationCheck] = Field(
        default_factory=list,
        description="Custom validation checks"
    )
    
    # Issue summary
    critical_issues: int = Field(default=0, ge=0, description="Number of critical issues")
    high_issues: int = Field(default=0, ge=0, description="Number of high severity issues")
    medium_issues: int = Field(default=0, ge=0, description="Number of medium severity issues")
    low_issues: int = Field(default=0, ge=0, description="Number of low severity issues")
    
    # Improvement recommendations
    priority_improvements: List[str] = Field(
        default_factory=list,
        description="High-priority improvements needed"
    )
    suggested_improvements: List[str] = Field(
        default_factory=list,
        description="Suggested improvements for better quality"
    )
    auto_fixes_available: List[str] = Field(
        default_factory=list,
        description="Issues that can be automatically fixed"
    )
    
    # Compliance and standards
    criteria_used: ValidationCriteria = Field(
        ...,
        description="Validation criteria used for this check"
    )
    compliance_score: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Compliance with enterprise standards"
    )
    
    # Performance metrics
    validation_duration: Optional[float] = Field(
        None,
        ge=0.0,
        description="Time taken for validation in seconds"
    )
    
    def get_failed_checks(self) -> List[ValidationCheck]:
        """Get all failed validation checks."""
        failed_checks = []
        
        for check in self.content_checks + self.data_checks + self.custom_checks:
            if not check.passed:
                failed_checks.append(check)
        
        return failed_checks
    
    def get_checks_by_severity(self, severity: ValidationSeverity) -> List[ValidationCheck]:
        """Get all checks of a specific severity level."""
        all_checks = self.content_checks + self.data_checks + self.custom_checks
        return [check for check in all_checks if check.severity == severity]
    
    def calculate_improvement_score(self) -> float:
        """Calculate potential improvement score if all issues are fixed."""
        if not self.get_failed_checks():
            return self.overall_score
        
        # Simple calculation - could be more sophisticated
        total_possible_improvement = len(self.get_failed_checks()) * 0.1
        return min(1.0, self.overall_score + total_possible_improvement)
    
    @validator('overall_score', 'compliance_score')
    def validate_scores(cls, v):
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError('Scores must be between 0.0 and 1.0')
        return v
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "validation_id": "VAL-2024-001",
                "overall_status": "passed",
                "overall_score": 0.85,
                "passed": True,
                "critical_issues": 0,
                "high_issues": 1,
                "medium_issues": 3,
                "low_issues": 5,
                "compliance_score": 0.90
            }
        }