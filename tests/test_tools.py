"""
Unit tests for custom tools in the Competitive Analysis Crew.

This module contains comprehensive unit tests for all custom tools:
- CompetitiveSearchTool
- MarketAnalysisTool  
- ReportValidationTool
"""

import pytest
import json
from unittest.mock import patch, MagicMock

from Competitive_analysis_crew.tools.competitive_search import CompetitiveSearchTool, SearchQuery
from Competitive_analysis_crew.tools.market_analysis import MarketAnalysisTool, MarketAnalysisRequest, CompanyInsight
from Competitive_analysis_crew.tools.report_validation import ReportValidationTool, ValidationCriteria, ValidationResult


class TestCompetitiveSearchTool:
    """Test cases for CompetitiveSearchTool."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.tool = CompetitiveSearchTool()
    
    def test_tool_initialization(self):
        """Test that the tool initializes correctly."""
        assert self.tool.name == "Competitive Intelligence Search"
        assert "competitive analysis research" in self.tool.description.lower()
    
    def test_basic_search_execution(self):
        """Test basic search functionality."""
        result = self.tool._run(
            query="financial performance",
            company="TechCorp",
            focus_area="financial"
        )
        
        assert isinstance(result, str)
        assert "TechCorp" in result
        assert "Financial Performance" in result
        assert "Competitive Intelligence Search Results" in result
    
    def test_search_without_company(self):
        """Test search functionality without specific company."""
        result = self.tool._run(
            query="market trends",
            company="",
            focus_area="market"
        )
        
        assert isinstance(result, str)
        assert "Market" in result
        assert "Industry Market Analysis" in result
    
    def test_build_competitive_query(self):
        """Test query enhancement functionality."""
        enhanced_query = self.tool._build_competitive_query(
            query="performance analysis",
            company="TestCorp",
            focus_area="financial"
        )
        
        assert "TestCorp" in enhanced_query
        assert "performance analysis" in enhanced_query
        assert any(term in enhanced_query for term in ["revenue", "earnings"])
    
    def test_generate_realistic_results(self):
        """Test realistic result generation."""
        results = self.tool._generate_realistic_results("TechCorp", "financial")
        
        assert isinstance(results, list)
        assert len(results) > 0
        
        for result in results:
            assert "title" in result
            assert "snippet" in result
            assert "relevance_score" in result
            assert "TechCorp" in result["title"]
    
    def test_different_focus_areas(self):
        """Test search with different focus areas."""
        focus_areas = ["financial", "products", "strategy", "market", "general"]
        
        for focus_area in focus_areas:
            result = self.tool._run(
                query="analysis",
                company="TestCorp",
                focus_area=focus_area
            )
            assert isinstance(result, str)
            assert focus_area.title() in result
    
    def test_format_competitive_results(self):
        """Test result formatting functionality."""
        mock_results = {
            "company": "TestCorp",
            "query": "test query",
            "results": [
                {
                    "title": "Test Result",
                    "url": "test-url",
                    "snippet": "Test snippet",
                    "relevance_score": 0.85,
                    "source_type": "test",
                    "date": "2024-01-01"
                }
            ],
            "competitive_insights": {
                "market_position": "Strong position",
                "key_strengths": ["Innovation"],
                "potential_threats": ["Competition"],
                "opportunities": ["Growth"]
            }
        }
        
        formatted = self.tool._format_competitive_results(mock_results, "general")
        
        assert "TestCorp" in formatted
        assert "Test Result" in formatted
        assert "Strong position" in formatted
        assert "Innovation" in formatted
    
    @patch('structlog.get_logger')
    def test_error_handling(self, mock_logger):
        """Test error handling in search execution."""
        # Mock logger to avoid actual logging during tests
        mock_logger.return_value = MagicMock()
        
        # Test with invalid input that might cause an error
        with patch.object(self.tool, '_simulate_competitive_search', side_effect=Exception("Test error")):
            result = self.tool._run("test query", "TestCorp", "general")
            assert "Error performing competitive search" in result


class TestMarketAnalysisTool:
    """Test cases for MarketAnalysisTool."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.tool = MarketAnalysisTool()
    
    def test_tool_initialization(self):
        """Test that the tool initializes correctly."""
        assert self.tool.name == "Market Position Analyzer"
        assert "market analysis" in self.tool.description.lower()
    
    def test_basic_market_analysis(self):
        """Test basic market analysis functionality."""
        result = self.tool._run(
            companies="TechCorp, InnovaCorp",
            industry="technology",
            analysis_type="competitive_positioning"
        )
        
        assert isinstance(result, str)
        assert "Market Analysis Report" in result
        assert "TechCorp" in result
        assert "InnovaCorp" in result
        assert "technology" in result.lower()
    
    def test_single_company_analysis(self):
        """Test analysis with single company."""
        result = self.tool._run(
            companies="SingleCorp",
            industry="finance",
            analysis_type="competitive_positioning"
        )
        
        assert isinstance(result, str)
        assert "SingleCorp" in result
        assert "finance" in result.lower()
    
    def test_generate_industry_trends(self):
        """Test industry trend generation."""
        # Test known industry
        tech_trends = self.tool._generate_industry_trends("technology")
        assert isinstance(tech_trends, list)
        assert len(tech_trends) > 0
        assert any("digital transformation" in trend.lower() for trend in tech_trends)
        
        # Test unknown industry (should return default trends)
        unknown_trends = self.tool._generate_industry_trends("unknown_industry")
        assert isinstance(unknown_trends, list)
        assert len(unknown_trends) > 0
    
    def test_analyze_company_position(self):
        """Test individual company position analysis."""
        insight = self.tool._analyze_company_position("TechCorp Inc", "technology")
        
        assert isinstance(insight, CompanyInsight)
        assert insight.name == "TechCorp Inc"
        assert isinstance(insight.strengths, list)
        assert isinstance(insight.weaknesses, list)
        assert isinstance(insight.competitive_advantages, list)
        assert len(insight.strengths) > 0
    
    def test_company_type_detection(self):
        """Test company type detection in analysis."""
        # Test large corporation
        large_corp = self.tool._analyze_company_position("BigCorp Inc", "technology")
        assert "market leader" in large_corp.market_position.lower()
        
        # Test tech-focused company
        tech_company = self.tool._analyze_company_position("TechSolutions", "technology")
        assert "innovator" in tech_company.market_position.lower()
        
        # Test regional company
        regional_company = self.tool._analyze_company_position("Nordic Services", "technology")
        assert "regional" in regional_company.market_position.lower()
    
    def test_analyze_competitive_dynamics(self):
        """Test competitive dynamics analysis."""
        # High competition scenario
        high_comp = self.tool._analyze_competitive_dynamics(
            ["Corp1", "Corp2", "Corp3", "Corp4"], "technology"
        )
        assert "intense competitive dynamics" in high_comp.lower()
        
        # Moderate competition scenario
        mod_comp = self.tool._analyze_competitive_dynamics(
            ["Corp1", "Corp2"], "technology"
        )
        assert "balanced competitive dynamics" in mod_comp.lower()
    
    def test_identify_market_forces(self):
        """Test market forces identification."""
        opportunities, threats = self.tool._identify_market_forces("technology", ["Corp1", "Corp2"])
        
        assert isinstance(opportunities, list)
        assert isinstance(threats, list)
        assert len(opportunities) > 0
        assert len(threats) > 0
    
    def test_perform_market_analysis(self):
        """Test comprehensive market analysis."""
        from Competitive_analysis_crew.tools.market_analysis import MarketAnalysis
        
        analysis = self.tool._perform_market_analysis(
            ["TechCorp", "InnovaCorp"], "technology", "competitive_positioning"
        )
        
        assert isinstance(analysis, MarketAnalysis)
        assert analysis.industry == "technology"
        assert len(analysis.company_insights) == 2
        assert len(analysis.key_trends) > 0
        assert len(analysis.opportunities) > 0
        assert len(analysis.threats) > 0
    
    def test_format_market_analysis(self):
        """Test market analysis formatting."""
        from Competitive_analysis_crew.tools.market_analysis import MarketAnalysis, CompanyInsight
        
        mock_analysis = MarketAnalysis(
            industry="technology",
            analysis_date="2024-01-01",
            market_overview="Test overview",
            key_trends=["Trend 1", "Trend 2"],
            competitive_dynamics="Test dynamics",
            company_insights=[
                CompanyInsight(
                    name="TestCorp",
                    market_position="Strong position",
                    strengths=["Innovation"],
                    weaknesses=["Scale"],
                    recent_developments=["Development 1"],
                    competitive_advantages=["Advantage 1"]
                )
            ],
            opportunities=["Opportunity 1"],
            threats=["Threat 1"],
            market_outlook="Positive outlook"
        )
        
        formatted = self.tool._format_market_analysis(mock_analysis)
        
        assert "Market Analysis Report: technology" in formatted
        assert "TestCorp" in formatted
        assert "Strong position" in formatted
        assert "Innovation" in formatted
    
    @patch('structlog.get_logger')
    def test_error_handling(self, mock_logger):
        """Test error handling in market analysis."""
        mock_logger.return_value = MagicMock()
        
        # Test with invalid input
        with patch.object(self.tool, '_perform_market_analysis', side_effect=Exception("Test error")):
            result = self.tool._run("TestCorp", "technology")
            assert "Error performing market analysis" in result


class TestReportValidationTool:
    """Test cases for ReportValidationTool."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.tool = ReportValidationTool()
        
        # Sample valid report for testing
        self.valid_report = """
# Executive Summary
This is a comprehensive competitive analysis report that provides detailed insights into the market landscape and competitive positioning.

## Analysis
The market analysis reveals significant opportunities for growth and competitive advantage through strategic positioning and innovation.

### Market Trends
- Digital transformation acceleration
- Increased focus on customer experience
- Growing emphasis on sustainability

## Recommendations
Based on our analysis, we recommend the following strategic initiatives:
1. Invest in digital capabilities
2. Enhance customer experience programs
3. Develop sustainable business practices

## Conclusion
The competitive landscape presents both challenges and opportunities for strategic growth.
"""
        
        # Sample invalid report for testing
        self.invalid_report = """
# Short Report
This is too short.
"""
    
    def test_tool_initialization(self):
        """Test that the tool initializes correctly."""
        assert self.tool.name == "Report Quality Validator"
        assert "validates" in self.tool.description.lower()
    
    def test_valid_report_validation(self):
        """Test validation of a valid report."""
        result = self.tool._run(self.valid_report)
        
        assert isinstance(result, str)
        assert "PASSED" in result or "score" in result.lower()
    
    def test_invalid_report_validation(self):
        """Test validation of an invalid report."""
        result = self.tool._run(self.invalid_report)
        
        assert isinstance(result, str)
        assert ("FAILED" in result or "too short" in result.lower() or 
                "issues found" in result.lower())
    
    def test_parse_criteria_default(self):
        """Test parsing of default validation criteria."""
        criteria = self.tool._parse_criteria(None)
        
        assert isinstance(criteria, ValidationCriteria)
        assert criteria.min_word_count == 500
        assert "Executive Summary" in criteria.required_sections
    
    def test_parse_criteria_custom(self):
        """Test parsing of custom validation criteria."""
        custom_criteria = json.dumps({
            "min_word_count": 300,
            "required_sections": ["Summary", "Analysis"]
        })
        
        criteria = self.tool._parse_criteria(custom_criteria)
        
        assert criteria.min_word_count == 300
        assert "Summary" in criteria.required_sections
    
    def test_parse_criteria_invalid_json(self):
        """Test parsing of invalid JSON criteria (should use defaults)."""
        criteria = self.tool._parse_criteria("invalid json")
        
        assert isinstance(criteria, ValidationCriteria)
        assert criteria.min_word_count == 500  # Default value
    
    def test_extract_sections(self):
        """Test section extraction from markdown."""
        sections = self.tool._extract_sections(self.valid_report)
        
        assert isinstance(sections, dict)
        assert "Executive Summary" in sections
        assert "Analysis" in sections
        assert "Recommendations" in sections
    
    def test_analyze_sections(self):
        """Test section analysis functionality."""
        sections = self.tool._extract_sections(self.valid_report)
        criteria = ValidationCriteria()
        
        analysis = self.tool._analyze_sections(sections, criteria)
        
        assert isinstance(analysis, dict)
        for section_name in sections.keys():
            assert section_name in analysis
            assert "word_count" in analysis[section_name]
            assert "meets_minimum" in analysis[section_name]
    
    def test_check_formatting(self):
        """Test formatting validation."""
        # Test content with good formatting
        good_content = """
# Header
**Bold text** and normal text.
- Bullet point 1
- Bullet point 2
"""
        issues = self.tool._check_formatting(good_content)
        assert len(issues) == 0
        
        # Test content with poor formatting
        poor_content = "Just plain text with no formatting"
        issues = self.tool._check_formatting(poor_content)
        assert len(issues) > 0
    
    def test_check_citations(self):
        """Test citation validation."""
        # Test content with citations
        cited_content = """
According to recent studies, the market is growing.
Source: Market Research Report 2024
[Link](http://example.com)
"""
        issues = self.tool._check_citations(cited_content)
        assert len(issues) == 0
        
        # Test content without citations
        uncited_content = "This is content without any citations or sources."
        issues = self.tool._check_citations(uncited_content)
        assert len(issues) > 0
    
    def test_check_content_quality(self):
        """Test content quality validation."""
        # Test content with quality issues
        poor_content = """
TODO: Add content here.
This is example.com/placeholder content.
Very short. Too short. Bad.
"""
        issues = self.tool._check_content_quality(poor_content)
        assert len(issues) > 0
        assert any("placeholder" in issue.lower() for issue in issues)
        
        # Test good quality content
        good_content = """
This comprehensive analysis examines market dynamics and competitive positioning.
The research methodology included quantitative analysis of 25% market share data.
Financial performance metrics indicate strong growth with $2.5M revenue in 2024.
Strategic recommendations focus on sustainable competitive advantages.
"""
        issues = self.tool._check_content_quality(good_content)
        # Should have fewer or no issues
        assert len(issues) <= 1  # Allow for minor issues
    
    def test_calculate_quality_score(self):
        """Test quality score calculation."""
        criteria = ValidationCriteria(min_word_count=100, max_word_count=1000)
        sections = {"Executive Summary": "content", "Analysis": "content"}
        
        # Test good score
        score = self.tool._calculate_quality_score(500, criteria, 0, sections)
        assert score >= 90
        
        # Test poor score with issues
        score = self.tool._calculate_quality_score(50, criteria, 5, {})
        assert score < 50
    
    def test_validate_report_comprehensive(self):
        """Test comprehensive report validation."""
        criteria = ValidationCriteria(
            min_word_count=50,  # Lower threshold for test
            required_sections=["Executive Summary", "Analysis"]
        )
        
        result = self.tool._validate_report(self.valid_report, criteria)
        
        assert isinstance(result, ValidationResult)
        assert isinstance(result.is_valid, bool)
        assert isinstance(result.score, float)
        assert 0 <= result.score <= 100
        assert isinstance(result.word_count, int)
        assert isinstance(result.issues, list)
        assert isinstance(result.recommendations, list)
    
    def test_format_validation_results(self):
        """Test validation result formatting."""
        mock_result = ValidationResult(
            is_valid=True,
            score=85.5,
            word_count=750,
            issues=["Minor issue"],
            recommendations=["Improve formatting"],
            section_analysis={
                "Executive Summary": {
                    "word_count": 100,
                    "meets_minimum": True,
                    "has_structure": True,
                    "quality_score": 90.0
                }
            }
        )
        
        formatted = self.tool._format_validation_results(mock_result)
        
        assert "85.5/100" in formatted
        assert "750" in formatted
        assert "Minor issue" in formatted
        assert "Executive Summary" in formatted
    
    @patch('structlog.get_logger')
    def test_error_handling(self, mock_logger):
        """Test error handling in report validation."""
        mock_logger.return_value = MagicMock()
        
        # Test with invalid input that might cause an error
        with patch.object(self.tool, '_validate_report', side_effect=Exception("Test error")):
            result = self.tool._run("test content")
            assert "Error validating report" in result


class TestToolIntegration:
    """Integration tests for tool interactions."""
    
    def test_tools_can_be_instantiated_together(self):
        """Test that all tools can be instantiated without conflicts."""
        search_tool = CompetitiveSearchTool()
        market_tool = MarketAnalysisTool()
        validation_tool = ReportValidationTool()
        
        assert search_tool.name != market_tool.name != validation_tool.name
        assert all(hasattr(tool, '_run') for tool in [search_tool, market_tool, validation_tool])
    
    def test_search_to_validation_workflow(self):
        """Test workflow from search results to validation."""
        search_tool = CompetitiveSearchTool()
        validation_tool = ReportValidationTool()
        
        # Get search results
        search_results = search_tool._run("financial analysis", "TechCorp", "financial")
        
        # Validate the search results as a report
        validation_results = validation_tool._run(search_results)
        
        assert isinstance(search_results, str)
        assert isinstance(validation_results, str)
        assert len(search_results) > 0
        assert len(validation_results) > 0
    
    def test_market_analysis_to_validation_workflow(self):
        """Test workflow from market analysis to validation."""
        market_tool = MarketAnalysisTool()
        validation_tool = ReportValidationTool()
        
        # Get market analysis
        market_results = market_tool._run("TechCorp, InnovaCorp", "technology")
        
        # Validate the market analysis as a report
        validation_results = validation_tool._run(market_results)
        
        assert isinstance(market_results, str)
        assert isinstance(validation_results, str)
        assert "Market Analysis Report" in market_results
        assert ("PASSED" in validation_results or "FAILED" in validation_results or 
                "score" in validation_results.lower())


if __name__ == "__main__":
    pytest.main([__file__])