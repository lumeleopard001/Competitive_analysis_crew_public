import sys
import os
sys.path.insert(0, 'src')

try:
    # Use the correct case - capital C
    from Competitive_analysis_crew.main import run
    print("🚀 Starting Competitive Analysis Crew...")
    run()
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
