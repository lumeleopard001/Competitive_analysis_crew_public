
#!/usr/bin/env python
"""
Alternative entry point for the Competitive Analysis Crew.

This script provides a simple way to run the crew without using the CLI commands.
It's useful for quick testing and development.
"""

import sys
import os

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, 'src')
sys.path.insert(0, src_path)

try:
    from Competitive_analysis_crew.main import run
    print("🚀 Starting Competitive Analysis Crew...")
    run()
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
