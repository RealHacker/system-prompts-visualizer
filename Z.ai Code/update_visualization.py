#!/usr/bin/env python3
"""
Script to update the visualization data for the Z.ai Code system prompt.
"""

import subprocess
import sys
import os

def main():
    print("Updating Z.ai Code system prompt visualization data...")
    
    # Run the analysis script
    try:
        result = subprocess.run([
            sys.executable, 
            os.path.join(os.path.dirname(__file__), 'analyze_prompt.py')
        ], capture_output=True, text=True, check=True)
        
        print("Analysis completed successfully!")
        print(result.stdout)
        
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)
            
    except subprocess.CalledProcessError as e:
        print(f"Error running analysis script: {e}")
        print(f"Error output: {e.stderr}")
        return 1
    except FileNotFoundError:
        print("Error: Could not find analyze_prompt.py script")
        return 1
    
    print("\nVisualization data has been updated!")
    print("Open system_prompt_visualizer.html in your browser to view the updated visualization.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())