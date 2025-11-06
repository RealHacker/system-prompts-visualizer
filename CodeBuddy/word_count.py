#!/usr/bin/env python3
"""
Accurately count words in CodeBuddy system prompts.
"""

import re

def count_words_precise(text: str) -> dict:
    """Count words with detailed breakdown."""
    # Remove code blocks to avoid counting code as words
    text_no_code = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text_no_code = re.sub(r'`[^`]*`', '', text_no_code)
    
    # Split into words (alphanumeric sequences)
    words = re.findall(r'\b[a-zA-Z0-9]+\b', text_no_code)
    
    # Count total words
    total_words = len(words)
    
    # Count unique words
    unique_words = len(set(word.lower() for word in words))
    
    # Get word frequency
    word_freq = {}
    for word in words:
        word_lower = word.lower()
        word_freq[word_lower] = word_freq.get(word_lower, 0) + 1
    
    # Sort by frequency
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    
    return {
        "total_words": total_words,
        "unique_words": unique_words,
        "most_frequent_words": sorted_words[:20]  # Top 20 most frequent words
    }

def main():
    """Count words in both prompt files."""
    import json
    
    # Read both files
    with open("Chat Prompt.txt", "r", encoding="utf-8") as f:
        chat_content = f.read()
    
    with open("Craft Prompt.txt", "r", encoding="utf-8") as f:
        craft_content = f.read()
    
    # Count words
    chat_stats = count_words_precise(chat_content)
    craft_stats = count_words_precise(craft_content)
    combined_stats = count_words_precise(chat_content + " " + craft_content)
    
    # Prepare results
    results = {
        "chat_prompt": chat_stats,
        "craft_prompt": craft_stats,
        "combined": combined_stats
    }
    
    # Save to file
    with open("word_count.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("Word count complete. Results saved to word_count.json")
    print(f"Chat Prompt: {chat_stats['total_words']} words")
    print(f"Craft Prompt: {craft_stats['total_words']} words")
    print(f"Combined: {combined_stats['total_words']} words")

if __name__ == "__main__":
    main()