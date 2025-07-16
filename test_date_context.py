#!/usr/bin/env python3
"""
Quick test script for DateContextTool functionality.
"""

from src.Competitive_analysis_crew.tools.date_context import DateContextTool

def test_date_context_tool():
    """Test the DateContextTool functionality."""
    print("Testing DateContextTool...")
    
    tool = DateContextTool()
    
    # Test full format
    print("\n=== Full Date Context ===")
    result = tool._run("full")
    print(result)
    
    # Test date only
    print("\n=== Date Only ===")
    result = tool._run("date_only")
    print(result)
    
    # Test year only
    print("\n=== Year Only ===")
    result = tool._run("year")
    print(result)
    
    # Test quarter
    print("\n=== Quarter ===")
    result = tool._run("quarter")
    print(result)
    
    print("\nDateContextTool test completed successfully!")

if __name__ == "__main__":
    test_date_context_tool()