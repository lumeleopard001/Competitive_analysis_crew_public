"""
Competitive Analysis Crew

This module defines the main crew class for competitive analysis automation.
It orchestrates multiple agents to perform comprehensive market intelligence
gathering, analysis, and reporting with human-in-the-loop oversight.
"""

import os
from typing import Dict, Any, Optional
import structlog

from crewai import Agent, Crew, Task, Process
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from langchain_community.chat_models import ChatOpenAI

from Competitive_analysis_crew.tools.competitive_search import CompetitiveSearchTool
from Competitive_analysis_crew.tools.market_analysis import MarketAnalysisTool
from Competitive_analysis_crew.tools.report_validation import ReportValidationTool
from Competitive_analysis_crew.tools.date_context import DateContextTool
from Competitive_analysis_crew.config.llm_config import LLMConfigManager

# Initialize structured logging
logger = structlog.get_logger()


class CompetitiveAnalysisCrew:
    """
    Main crew class for competitive analysis automation.
    
    This class orchestrates a multi-agent workflow that includes:
    - User onboarding and data collection
    - Competitive research and analysis
    - Report generation and validation
    - Quality assurance and editing
    - Optional translation services
    """
    
    def __init__(self):
        """Initialize the competitive analysis crew with agents, tasks, and tools."""
        self.llm_config = LLMConfigManager()
        self._initialize_tools()
        self._initialize_agents()
        self._initialize_tasks()
        
        logger.info("Competitive Analysis Crew initialized successfully")
    
    def _initialize_tools(self):
        """Initialize all tools used by the crew."""
        self.search_tool = SerperDevTool()
        self.scrape_tool = ScrapeWebsiteTool()
        self.competitive_search_tool = CompetitiveSearchTool()
        self.market_analysis_tool = MarketAnalysisTool()
        self.report_validation_tool = ReportValidationTool()
        self.date_context_tool = DateContextTool()
        
        logger.info("Tools initialized", tool_count=6)
    
    def _initialize_agents(self):
        """Initialize all agents with their roles, goals, and tools."""
        
        # Onboarding Specialist - Collects user information
        self.onboarding_specialist = Agent(
            role="User Onboarding Specialist",
            goal="Efficiently collect essential information about the client company and competitors for competitive analysis",
            backstory=(
                "You are an experienced business analyst specializing in competitive intelligence. "
                "Your expertise lies in quickly identifying the key information needed for thorough "
                "competitive analysis. You ask targeted questions to gather company details and "
                "competitor information efficiently."
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.llm_config.get_llm("openai", "gpt-4o-mini", "onboarding")
        )
        
        # Research Analyst - Conducts competitive research
        self.research_analyst = Agent(
            role="Senior Competitive Research Analyst",
            goal="Conduct comprehensive competitive analysis research using advanced tools and methodologies",
            backstory=(
                "You are a seasoned competitive intelligence analyst with over 10 years of experience "
                "in market research and competitive analysis. You excel at gathering, synthesizing, "
                "and analyzing information from multiple sources to create comprehensive competitive "
                "intelligence reports. Your research is thorough, accurate, and actionable. "
                "CRITICAL: You MUST always use the DateContextTool FIRST before any analysis to get "
                "current date context. Never assume what year it is - always check the current date."
            ),
            tools=[self.search_tool, self.scrape_tool, self.competitive_search_tool, self.market_analysis_tool, self.date_context_tool],
            verbose=True,
            allow_delegation=True,
            llm=self.llm_config.get_llm("openai", "gpt-4o", "research")
        )
        
        # Report Writer - Creates structured reports
        self.report_writer = Agent(
            role="Strategic Report Writer",
            goal="Transform research findings into professional, actionable competitive analysis reports",
            backstory=(
                "You are an expert business writer specializing in competitive intelligence reports. "
                "You have a talent for transforming complex research data into clear, structured, "
                "and actionable reports that executives can use for strategic decision-making. "
                "Your reports are known for their clarity, insight, and professional presentation."
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.llm_config.get_llm("openai", "gpt-4o", "writing")
        )
        
        # Quality Manager - Validates and manages quality
        self.quality_manager = Agent(
            role="Quality Assurance Manager",
            goal="Ensure all reports meet enterprise-grade quality standards and coordinate the writing process",
            backstory=(
                "You are a quality assurance expert with extensive experience in business report "
                "validation and process management. You ensure that all deliverables meet the highest "
                "standards of quality, accuracy, and professionalism. You coordinate between different "
                "team members to ensure smooth workflow and exceptional results."
            ),
            tools=[self.report_validation_tool],
            verbose=True,
            allow_delegation=True,
            llm=self.llm_config.get_llm("openai", "gpt-4o", "management")
        )
        
        # Senior Editor - Polishes final reports
        self.senior_editor = Agent(
            role="Senior Executive Editor",
            goal="Polish reports to executive presentation standards with impeccable language and flow",
            backstory=(
                "You are a senior editor with decades of experience in executive communications. "
                "You specialize in refining business documents to meet the highest standards of "
                "professional presentation. Your editing ensures clarity, impact, and executive-level "
                "polish while maintaining the integrity of the original analysis."
            ),
            verbose=True,
            allow_delegation=False,
            llm=self.llm_config.get_llm("openai", "gpt-4o", "editing")
        )
        
        # Translator - Provides multilingual support
        self.translator = Agent(
            role="Professional Business Translator",
            goal="Provide accurate, context-aware translations of business reports while maintaining professional tone",
            backstory=(
                "You are a professional translator specializing in business and competitive intelligence "
                "documents. You have expertise in multiple languages and understand the nuances of "
                "business terminology across different cultures. Your translations maintain the "
                "professional tone and accuracy of the original while being natural in the target language. "
                "IMPORTANT: Today's date is July 16, 2025. The current year is 2025, not 2023."
            ),
            tools=[self.date_context_tool],
            verbose=True,
            allow_delegation=False,
            llm=self.llm_config.get_llm("openai", "gpt-4o", "translation")
        )
        
        logger.info("Agents initialized", agent_count=6)
    
    def _initialize_tasks(self):
        """Initialize all tasks for the competitive analysis workflow."""
        
        # Task 1: Collect company and competitor information
        self.task_collect_info = Task(
            description=(
                "Collect essential information for competitive analysis:\n"
                "1. Ask the user for their company name and basic details\n"
                "2. Ask for a list of main competitors to analyze\n"
                "3. Gather any specific focus areas or preferences for the analysis\n"
                "4. Confirm all information is accurate before proceeding"
            ),
            expected_output=(
                "A structured summary containing:\n"
                "- Client company name and basic details\n"
                "- List of competitor companies to analyze\n"
                "- Any specific focus areas or analysis preferences\n"
                "- Confirmation that all information is accurate"
            ),
            agent=self.onboarding_specialist,
            human_input=True
        )
        
        # Task 2: Conduct comprehensive research
        self.task_research = Task(
            description=(
                "Conduct comprehensive competitive research:\n"
                "1. FIRST: Use the DateContextTool to get current date context for accurate temporal analysis\n"
                "2. Research the client company: recent news, financial performance, market position\n"
                "3. Research each competitor: business model, strengths, weaknesses, recent developments\n"
                "4. Analyze market trends and competitive landscape\n"
                "5. Gather quantitative and qualitative data from multiple reliable sources\n"
                "6. Synthesize findings into a comprehensive research dossier\n\n"
                "IMPORTANT: Always use the DateContextTool at the beginning to understand what 'current', "
                "'recent', and 'latest' mean in terms of actual dates. When discussing financial data, "
                "always specify the actual year (e.g., '2025 financial performance') rather than "
                "relative terms like 'last year' or 'recent year'."
            ),
            expected_output=(
                "A detailed research dossier containing:\n"
                "- Client company profile with recent developments and market position\n"
                "- Comprehensive competitor profiles with strengths, weaknesses, and strategies\n"
                "- Market landscape analysis and trends\n"
                "- Key insights and competitive dynamics\n"
                "- All sources properly cited and verified"
            ),
            agent=self.research_analyst,
            context=[self.task_collect_info]
        )
        
        # Task 3: Write the competitive analysis report
        self.task_write_report = Task(
            description=(
                "Create a professional competitive analysis report:\n"
                "1. Structure the report with clear sections: Executive Summary, Company Profiles, "
                "Competitive Analysis, Market Insights, and Recommendations\n"
                "2. Use the research dossier to create comprehensive company profiles\n"
                "3. Develop a comparative analysis highlighting key differentiators\n"
                "4. Include actionable recommendations based on the analysis\n"
                "5. Ensure the report is professional, well-formatted, and executive-ready"
            ),
            expected_output=(
                "A comprehensive competitive analysis report in markdown format with:\n"
                "- Executive Summary (2-3 paragraphs)\n"
                "- Detailed company profiles for client and competitors\n"
                "- Comparative analysis with SWOT-style insights\n"
                "- Market positioning and competitive dynamics\n"
                "- Strategic recommendations and next steps\n"
                "- Professional formatting suitable for executive presentation"
            ),
            agent=self.report_writer,
            context=[self.task_research]
        )
        
        # Task 4: Quality validation and management
        self.task_validate_quality = Task(
            description=(
                "Validate report quality and manage the writing process:\n"
                "1. Review the report for completeness, accuracy, and professional standards\n"
                "2. Check that all required sections are present and well-developed\n"
                "3. Validate that recommendations are actionable and well-supported\n"
                "4. Ensure proper formatting and executive-level presentation\n"
                "5. If quality standards are not met, coordinate with the writer for improvements"
            ),
            expected_output=(
                "Quality validation report containing:\n"
                "- Assessment of report completeness and accuracy\n"
                "- Validation of professional standards and formatting\n"
                "- Confirmation that all requirements are met\n"
                "- Any recommendations for improvements (if needed)\n"
                "- Final approval for the report to proceed to editing"
            ),
            agent=self.quality_manager,
            context=[self.task_write_report]
        )
        
        # Task 5: Editorial review and polishing
        self.task_edit_report = Task(
            description=(
                "Perform final editorial review and polishing:\n"
                "1. Review the report for grammar, style, and clarity\n"
                "2. Enhance language for executive-level presentation\n"
                "3. Ensure consistent tone and professional flow\n"
                "4. Optimize readability and impact\n"
                "5. Maintain all factual content while improving presentation"
            ),
            expected_output=(
                "A polished, executive-ready competitive analysis report with:\n"
                "- Impeccable grammar and professional language\n"
                "- Enhanced clarity and readability\n"
                "- Consistent executive-level tone throughout\n"
                "- Optimized structure and flow\n"
                "- Professional formatting and presentation"
            ),
            agent=self.senior_editor,
            context=[self.task_validate_quality]
        )
        
        # Task 6: Translation (optional)
        self.task_translate = Task(
            description=(
                "Provide optional translation services:\n"
                "1. Ask the user if they need the report translated to another language\n"
                "2. If translation is requested, ask for the target language\n"
                "3. Translate the report while maintaining professional tone and accuracy\n"
                "4. Ensure business terminology is correctly translated\n"
                "5. Provide both original and translated versions\n"
                "6. IMPORTANT: Always display the full report content in your final answer"
            ),
            expected_output=(
                "Translation service result with FULL REPORT CONTENT:\n"
                "- Complete original report text\n"
                "- If translation requested: complete translated report text\n"
                "- Both versions must be fully displayed in the final answer\n"
                "- Maintained professional tone and business terminology"
            ),
            agent=self.translator,
            context=[self.task_edit_report],
            human_input=True
        )
        
        logger.info("Tasks initialized", task_count=6)
    
    def crew(self) -> Crew:
        """
        Create and return the configured crew.
        
        Returns:
            Crew: Configured competitive analysis crew ready for execution
        """
        return Crew(
            agents=[
                self.onboarding_specialist,
                self.research_analyst,
                self.report_writer,
                self.quality_manager,
                self.senior_editor,
                self.translator
            ],
            tasks=[
                self.task_collect_info,
                self.task_research,
                self.task_write_report,
                self.task_validate_quality,
                self.task_edit_report,
                self.task_translate
            ],
            process=Process.sequential,
            memory=True,
            verbose=True,
            manager_llm=self.llm_config.get_llm("openai", "gpt-4o", "manager")
        )