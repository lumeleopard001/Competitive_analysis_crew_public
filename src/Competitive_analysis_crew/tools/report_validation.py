"""
Report Validation Tool

A specialized tool for validating competitive analysis reports against
enterprise-grade quality standards and business requirements.
"""

import re
from typing import Dict, List, Any, Optional
import structlog

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

logger = structlog.get_logger()


class ValidationCriteria(BaseModel):
    """Model for report validation criteria."""
    min_word_count: int = Field(default=500, description="Minimum word count for the report")
    max_word_count: int = Field(default=3000, description="Maximum word count for the report")
    required_sections: List[str] = Field(
        default=["Executive Summary", "Analysis", "Recommendations"],
        description="Required sections that must be present"
    )
    min_section_length: int = Field(default=50, description="Minimum words per section")
    check_citations: bool = Field(default=True, description="Whether to check for proper citations")
    check_formatting: bool = Field(default=True, description="Whether to check markdown formatting")


class ValidationResult(BaseModel):
    """Model for validation results."""
    is_valid: bool = Field(..., description="Whether the report passes validation")
    score: float = Field(..., description="Overall quality score (0-100)")
    word_count: int = Field(..., description="Total word count")
    issues: List[str] = Field(default=[], description="List of validation issues found")
    recommendations: List[str] = Field(default=[], description="Recommendations for improvement")
    section_analysis: Dict[str, Any] = Field(default={}, description="Analysis of each section")


class ReportValidationTool(BaseTool):
    """
    Advanced report validation tool for competitive analysis reports.
    
    This tool validates reports against enterprise-grade quality standards,
    checking for completeness, structure, formatting, and professional presentation.
    """
    
    name: str = "Report Quality Validator"
    description: str = (
        "Validates competitive analysis reports against enterprise-grade quality standards. "
        "Checks for proper structure, adequate content length, professional formatting, "
        "and completeness of required sections. Use this tool to ensure reports meet "
        "business-grade quality requirements before final delivery."
    )
    
    def _run(self, report_content: str, criteria: Optional[str] = None) -> str:
        """
        Validate a competitive analysis report.
        
        Args:
            report_content: The full text content of the report to validate
            criteria: Optional JSON string with custom validation criteria
            
        Returns:
            str: Detailed validation report with scores and recommendations
        """
        try:
            logger.info("Starting report validation", content_length=len(report_content))
            
            # Parse custom criteria if provided
            validation_criteria = self._parse_criteria(criteria)
            
            # Perform comprehensive validation
            validation_result = self._validate_report(report_content, validation_criteria)
            
            logger.info("Report validation completed", 
                       score=validation_result.score, 
                       is_valid=validation_result.is_valid)
            
            return self._format_validation_results(validation_result)
            
        except Exception as e:
            logger.error("Error in report validation", error=str(e))
            return f"Error validating report: {str(e)}"
    
    def _parse_criteria(self, criteria: Optional[str]) -> ValidationCriteria:
        """
        Parse validation criteria from JSON string or use defaults.
        
        Args:
            criteria: Optional JSON string with validation criteria
            
        Returns:
            ValidationCriteria: Parsed or default validation criteria
        """
        if criteria:
            try:
                import json
                criteria_dict = json.loads(criteria)
                return ValidationCriteria(**criteria_dict)
            except Exception as e:
                logger.warning("Failed to parse custom criteria, using defaults", error=str(e))
        
        return ValidationCriteria()
    
    def _validate_report(self, content: str, criteria: ValidationCriteria) -> ValidationResult:
        """
        Perform comprehensive report validation.
        
        Args:
            content: Report content to validate
            criteria: Validation criteria to apply
            
        Returns:
            ValidationResult: Comprehensive validation results
        """
        issues = []
        recommendations = []
        section_analysis = {}
        
        # 1. Word count validation
        word_count = len(content.split())
        if word_count < criteria.min_word_count:
            issues.append(f"Report is too short: {word_count} words (minimum: {criteria.min_word_count})")
            recommendations.append(f"Expand content to reach at least {criteria.min_word_count} words")
        elif word_count > criteria.max_word_count:
            issues.append(f"Report is too long: {word_count} words (maximum: {criteria.max_word_count})")
            recommendations.append(f"Condense content to stay under {criteria.max_word_count} words")
        
        # 2. Section structure validation
        sections = self._extract_sections(content)
        section_analysis = self._analyze_sections(sections, criteria)
        
        for section_name in criteria.required_sections:
            if section_name not in sections:
                issues.append(f"Missing required section: {section_name}")
                recommendations.append(f"Add a comprehensive {section_name} section")
            elif len(sections[section_name].split()) < criteria.min_section_length:
                issues.append(f"Section '{section_name}' is too short: {len(sections[section_name].split())} words")
                recommendations.append(f"Expand the {section_name} section with more detailed content")
        
        # 3. Formatting validation
        if criteria.check_formatting:
            formatting_issues = self._check_formatting(content)
            issues.extend(formatting_issues)
            if formatting_issues:
                recommendations.append("Improve markdown formatting and structure")
        
        # 4. Citation validation
        if criteria.check_citations:
            citation_issues = self._check_citations(content)
            issues.extend(citation_issues)
            if citation_issues:
                recommendations.append("Add proper citations and source references")
        
        # 5. Content quality checks
        quality_issues = self._check_content_quality(content)
        issues.extend(quality_issues)
        if quality_issues:
            recommendations.append("Improve content quality and professional presentation")
        
        # Calculate overall score
        score = self._calculate_quality_score(word_count, criteria, len(issues), sections)
        
        return ValidationResult(
            is_valid=len(issues) == 0,
            score=score,
            word_count=word_count,
            issues=issues,
            recommendations=recommendations,
            section_analysis=section_analysis
        )
    
    def _extract_sections(self, content: str) -> Dict[str, str]:
        """
        Extract sections from markdown content.
        
        Args:
            content: Markdown content to parse
            
        Returns:
            Dict[str, str]: Dictionary mapping section names to content
        """
        sections = {}
        current_section = None
        current_content = []
        
        lines = content.split('\n')
        
        for line in lines:
            # Check for markdown headers
            if line.startswith('#'):
                # Save previous section
                if current_section:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # Start new section
                current_section = line.lstrip('#').strip()
                current_content = []
            else:
                if current_section:
                    current_content.append(line)
        
        # Save last section
        if current_section:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    def _analyze_sections(self, sections: Dict[str, str], criteria: ValidationCriteria) -> Dict[str, Any]:
        """
        Analyze individual sections for quality and completeness.
        
        Args:
            sections: Dictionary of section content
            criteria: Validation criteria
            
        Returns:
            Dict[str, Any]: Analysis results for each section
        """
        analysis = {}
        
        for section_name, content in sections.items():
            word_count = len(content.split())
            analysis[section_name] = {
                "word_count": word_count,
                "meets_minimum": word_count >= criteria.min_section_length,
                "has_structure": bool(re.search(r'[.!?]', content)),  # Has sentences
                "has_lists": bool(re.search(r'^\s*[-*+]', content, re.MULTILINE)),  # Has bullet points
                "quality_score": min(100, (word_count / criteria.min_section_length) * 100)
            }
        
        return analysis
    
    def _check_formatting(self, content: str) -> List[str]:
        """
        Check markdown formatting quality.
        
        Args:
            content: Content to check
            
        Returns:
            List[str]: List of formatting issues
        """
        issues = []
        
        # Check for proper header hierarchy
        headers = re.findall(r'^(#+)\s+(.+)$', content, re.MULTILINE)
        if not headers:
            issues.append("No markdown headers found - report lacks structure")
        
        # Check for consistent formatting
        if not re.search(r'\*\*[^*]+\*\*', content):  # Bold text
            issues.append("No bold text formatting found - consider emphasizing key points")
        
        # Check for lists
        if not re.search(r'^\s*[-*+]', content, re.MULTILINE):
            issues.append("No bullet points found - consider using lists for better readability")
        
        return issues
    
    def _check_citations(self, content: str) -> List[str]:
        """
        Check for proper citations and references.
        
        Args:
            content: Content to check
            
        Returns:
            List[str]: List of citation issues
        """
        issues = []
        
        # Look for common citation patterns
        citation_patterns = [
            r'\[.*\]\(http.*\)',  # Markdown links
            r'Source:',  # Source references
            r'According to',  # Attribution phrases
            r'\d{4}',  # Years (basic date check)
        ]
        
        has_citations = any(re.search(pattern, content, re.IGNORECASE) for pattern in citation_patterns)
        
        if not has_citations:
            issues.append("No citations or source references found")
        
        return issues
    
    def _check_content_quality(self, content: str) -> List[str]:
        """
        Check general content quality indicators.
        
        Args:
            content: Content to check
            
        Returns:
            List[str]: List of quality issues
        """
        issues = []
        
        # Check for placeholder text and URLs
        placeholders = ['TODO', 'TBD', 'PLACEHOLDER', '[INSERT', 'EXAMPLE', 'https://example.com']
        for placeholder in placeholders:
            if placeholder.lower() in content.lower():
                issues.append(f"Contains placeholder text or URLs: {placeholder}")
        
        # Check for generic placeholder patterns
        placeholder_patterns = [
            r'https://example\.com/[^)\s]*',  # Example URLs
            r'\[.*finantstulemused.*\]',  # Estonian placeholder patterns
            r'\[.*financial.*results.*\]',  # English placeholder patterns
            r'Latest financial results and performance metrics for',  # Generic descriptions
            r'Strategic initiatives and market positioning for',  # Generic descriptions
        ]
        
        for pattern in placeholder_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append(f"Contains generic placeholder content matching pattern: {pattern}")
        
        # Check for very short sentences (potential quality issue)
        sentences = re.split(r'[.!?]+', content)
        short_sentences = [s.strip() for s in sentences if 0 < len(s.strip().split()) < 3]
        if len(short_sentences) > 5:
            issues.append("Contains many very short sentences - consider improving flow")
        
        # Check for repetitive content
        words = content.lower().split()
        if len(words) > 0 and len(set(words)) / len(words) < 0.3:  # Less than 30% unique words
            issues.append("Content appears repetitive - consider varying language")
        
        # Check for lack of specific data
        if not re.search(r'\d+%|\$\d+|\d+\.\d+|\d{4}', content):
            issues.append("Report lacks specific quantitative data - consider adding metrics, percentages, or dates")
        
        return issues
    
    def _calculate_quality_score(self, word_count: int, criteria: ValidationCriteria, 
                                issue_count: int, sections: Dict[str, str]) -> float:
        """
        Calculate overall quality score.
        
        Args:
            word_count: Total word count
            criteria: Validation criteria
            issue_count: Number of issues found
            sections: Section content
            
        Returns:
            float: Quality score (0-100)
        """
        score = 100.0
        
        # Deduct points for word count issues
        if word_count < criteria.min_word_count:
            score -= 20 * (1 - word_count / criteria.min_word_count)
        elif word_count > criteria.max_word_count:
            score -= 10
        
        # Deduct points for missing sections
        missing_sections = len([s for s in criteria.required_sections if s not in sections])
        score -= missing_sections * 15
        
        # Deduct points for issues
        score -= issue_count * 5
        
        # Bonus for comprehensive content
        if word_count > criteria.min_word_count * 1.5:
            score += 5
        
        return max(0, min(100, score))
    
    def _format_validation_results(self, result: ValidationResult) -> str:
        """
        Format validation results for display.
        
        Args:
            result: Validation results to format
            
        Returns:
            str: Formatted validation report
        """
        output = []
        
        # Header
        status = "✅ PASSED" if result.is_valid else "❌ FAILED"
        output.append(f"# Report Validation Results: {status}")
        output.append(f"**Overall Score:** {result.score:.1f}/100")
        output.append(f"**Word Count:** {result.word_count}")
        output.append("")
        
        # Issues
        if result.issues:
            output.append("## Issues Found")
            for i, issue in enumerate(result.issues, 1):
                output.append(f"{i}. {issue}")
            output.append("")
        
        # Recommendations
        if result.recommendations:
            output.append("## Recommendations")
            for i, rec in enumerate(result.recommendations, 1):
                output.append(f"{i}. {rec}")
            output.append("")
        
        # Section Analysis
        if result.section_analysis:
            output.append("## Section Analysis")
            for section, analysis in result.section_analysis.items():
                status_icon = "✅" if analysis["meets_minimum"] else "⚠️"
                output.append(f"### {status_icon} {section}")
                output.append(f"- Word Count: {analysis['word_count']}")
                output.append(f"- Quality Score: {analysis['quality_score']:.1f}/100")
                output.append(f"- Has Structure: {'Yes' if analysis['has_structure'] else 'No'}")
                output.append("")
        
        # Summary
        if result.is_valid:
            output.append("## Summary")
            output.append("✅ Report meets all validation criteria and is ready for delivery.")
        else:
            output.append("## Summary")
            output.append("❌ Report requires improvements before it meets quality standards.")
            output.append("Please address the issues and recommendations listed above.")
        
        output.append("")
        output.append("---")
        output.append("*Validation performed by Report Quality Validator*")
        
        return "\n".join(output)