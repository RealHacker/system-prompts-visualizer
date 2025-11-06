import re
import subprocess
import sys
import os

def get_prompt_stats():
    """Get statistics from the prompt analysis."""
    try:
        # Run the word count script
        result = subprocess.run(
            ['python', 'word_count.py'], 
            capture_output=True, 
            text=True, 
            cwd='e:\\Toy\\system-prompts-and-models-of-ai-tools\\Kiro'
        )
        
        # Extract word count from output
        word_count = 0
        if result.returncode == 0:
            match = re.search(r'(\d+)', result.stdout)
            if match:
                word_count = int(match.group(1))
        
        # Run the analysis script
        result = subprocess.run(
            ['python', 'analyze_prompt.py'], 
            capture_output=True, 
            text=True, 
            cwd='e:\\Toy\\system-prompts-and-models-of-ai-tools\\Kiro'
        )
        
        # Extract feature count from output
        feature_count = 0
        if result.returncode == 0:
            match = re.search(r'Number of tools/features: (\d+)', result.stdout)
            if match:
                feature_count = int(match.group(1))
        
        return word_count, feature_count
    except Exception as e:
        print(f"Error getting prompt stats: {e}")
        return 0, 0

def update_html_file(word_count, feature_count):
    """Update the HTML file with new statistics."""
    try:
        html_file = 'e:\\Toy\\system-prompts-and-models-of-ai-tools\\Kiro\\system_prompt_visualizer.html'
        
        with open(html_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Update word count
        content = re.sub(
            r'<div class="value" id="totalWords">.*?</div>',
            f'<div class="value" id="totalWords">{word_count:,}</div>',
            content
        )
        
        # Update feature count
        content = re.sub(
            r'<div class="value" id="toolCount">.*?</div>',
            f'<div class="value" id="toolCount">{feature_count}</div>',
            content
        )
        
        with open(html_file, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"Successfully updated HTML file with {word_count:,} words and {feature_count} features")
        return True
    except Exception as e:
        print(f"Error updating HTML file: {e}")
        return False

if __name__ == "__main__":
    print("Updating Kiro system prompt visualization...")
    
    # Get current statistics
    word_count, feature_count = get_prompt_stats()
    
    if word_count > 0 and feature_count >= 0:
        # Update the HTML file
        if update_html_file(word_count, feature_count):
            print("Visualization updated successfully!")
        else:
            print("Failed to update visualization")
            sys.exit(1)
    else:
        print("Failed to get prompt statistics")
        sys.exit(1)