import re
import subprocess
import sys
import os
import json

def get_prompt_stats():
    """Get statistics from the prompt analysis."""
    try:
        # Run the word count script
        result = subprocess.run(
            ['python', 'word_count.py'], 
            capture_output=True, 
            text=True, 
            cwd='e:\\Toy\\system-prompts-and-models-of-ai-tools\\Lovable'
        )
        
        # Extract word counts from output
        prompt_word_count = 0
        tools_word_count = 0
        total_words = 0
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'Words in prompt file:' in line:
                    match = re.search(r'(\d+)', line)
                    if match:
                        prompt_word_count = int(match.group(1))
                elif 'Words in tools file:' in line:
                    match = re.search(r'(\d+)', line)
                    if match:
                        tools_word_count = int(match.group(1))
                elif 'Total words in system prompt and tools:' in line:
                    match = re.search(r'(\d+)', line)
                    if match:
                        total_words = int(match.group(1))
        
        # Run the analysis script to get tool count
        result = subprocess.run(
            ['python', 'analyze_prompt.py'], 
            capture_output=True, 
            text=True, 
            cwd='e:\\Toy\\system-prompts-and-models-of-ai-tools\\Lovable'
        )
        
        # Extract tool count from output
        tool_count = 0
        if result.returncode == 0:
            match = re.search(r'Number of tools: (\d+)', result.stdout)
            if match:
                tool_count = int(match.group(1))
        
        return total_words, tool_count
    except Exception as e:
        print(f"Error getting prompt stats: {e}")
        return 0, 0

def update_html_file(word_count, tool_count):
    """Update the HTML file with new statistics."""
    try:
        html_file = 'e:\\Toy\\system-prompts-and-models-of-ai-tools\\Lovable\\system_prompt_visualizer.html'
        
        with open(html_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Update word count
        content = re.sub(
            r'<div class="value" id="totalWords">.*?</div>',
            f'<div class="value" id="totalWords">{word_count:,}</div>',
            content
        )
        
        # Update tool count
        content = re.sub(
            r'<div class="value" id="toolCount">.*?</div>',
            f'<div class="value" id="toolCount">{tool_count}</div>',
            content
        )
        
        with open(html_file, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"Successfully updated HTML file with {word_count:,} words and {tool_count} tools")
        return True
    except Exception as e:
        print(f"Error updating HTML file: {e}")
        return False

if __name__ == "__main__":
    print("Updating Lovable system prompt visualization...")
    
    # Get current statistics
    word_count, tool_count = get_prompt_stats()
    
    if word_count > 0 and tool_count >= 0:
        # Update the HTML file
        if update_html_file(word_count, tool_count):
            print("Visualization updated successfully!")
        else:
            print("Failed to update visualization")
            sys.exit(1)
    else:
        print("Failed to get prompt statistics")
        sys.exit(1)