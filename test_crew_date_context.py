#!/usr/bin/env python3
"""
Test script to verify DateContextTool integration with the crew.
"""

import os
from src.Competitive_analysis_crew.crew import CompetitiveAnalysisCrew

def test_crew_with_date_context():
    """Test that the crew can access and use DateContextTool."""
    print("Testing CrewAI with DateContextTool integration...")
    
    # Initialize the crew
    crew_instance = CompetitiveAnalysisCrew()
    
    # Check that DateContextTool is available
    print(f"\nTools initialized: {len(crew_instance.research_analyst.tools)} tools")
    
    # List all tools available to research analyst
    print("\nResearch Analyst Tools:")
    for i, tool in enumerate(crew_instance.research_analyst.tools, 1):
        tool_name = tool.__class__.__name__
        print(f"  {i}. {tool_name}")
        
        # Test DateContextTool specifically
        if tool_name == "DateContextTool":
            print(f"     Testing {tool_name}...")
            try:
                result = tool._run("full")
                print(f"     ✅ DateContextTool working! Current context:")
                # Print first few lines of the result
                lines = result.split('\n')[:5]
                for line in lines:
                    if line.strip():
                        print(f"        {line}")
                print("        ...")
            except Exception as e:
                print(f"     ❌ Error testing DateContextTool: {e}")
    
    # Verify task descriptions include date context instructions
    print(f"\nResearch Task Description includes date context: {'DateContextTool' in crew_instance.task_research.description}")
    
    print("\n" + "="*60)
    print("CREW DATE CONTEXT TEST SUMMARY:")
    print("="*60)
    
    # Check if DateContextTool is properly integrated
    has_date_tool = any(tool.__class__.__name__ == "DateContextTool" 
                       for tool in crew_instance.research_analyst.tools)
    
    print(f"✅ DateContextTool added to research analyst: {has_date_tool}")
    print(f"✅ Task description updated with date instructions: {'DateContextTool' in crew_instance.task_research.description}")
    print(f"✅ Total tools available to research analyst: {len(crew_instance.research_analyst.tools)}")
    
    if has_date_tool:
        print("\n🎉 SUCCESS: DateContextTool is properly integrated!")
        print("   The research analyst now has access to current date context")
        print("   and should provide accurate temporal references in analysis.")
    else:
        print("\n❌ ISSUE: DateContextTool not found in research analyst tools")
    
    return has_date_tool

if __name__ == "__main__":
    test_crew_with_date_context()