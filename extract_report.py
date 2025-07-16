#!/usr/bin/env python3
"""
Script to extract and display the competitive analysis report from crew execution.
"""

import os
from src.Competitive_analysis_crew.crew import CompetitiveAnalysisCrew

def extract_report_from_crew():
    """Extract the report from the crew's last execution."""
    print("Attempting to extract report from crew execution...")
    
    try:
        # Initialize the crew
        crew_instance = CompetitiveAnalysisCrew()
        crew = crew_instance.crew()
        
        # Check if there's any stored output or memory
        print("Crew initialized successfully")
        print(f"Crew has memory enabled: {crew.memory}")
        
        # Try to access crew memory if available
        if hasattr(crew, '_memory') and crew._memory:
            print("Checking crew memory for report content...")
            # This would depend on CrewAI's memory implementation
        
        print("\nTo see the report, you'll need to run the crew again and capture the output.")
        print("The issue seems to be that the translator agent isn't properly displaying the full report.")
        
        return None
        
    except Exception as e:
        print(f"Error extracting report: {e}")
        return None

if __name__ == "__main__":
    extract_report_from_crew()