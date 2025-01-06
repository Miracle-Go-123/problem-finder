#!/usr/bin/env python
import sys
import warnings
import json
from pathlib import Path
from typing import List, Dict, Any

from problemfinder.crew import ProblemFinder

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def load_input_data() -> Dict[str, Any]:
    """Load document URLs and chat history from JSON files"""
    assets_path = Path("assets")
    
    with open(assets_path / "document.json", "r") as f:
        documents = json.load(f)
        
    with open(assets_path / "chat.json", "r") as f:
        chat = json.load(f)
        
    return {
        "documents": documents,
        "chat": chat
    }

def run() -> List[str]:
    """
    Run the ProblemFinder crew to analyze documents and chat history
    Returns a list of identified problems/issues
    """
    # Initialize input data
    input_data = load_input_data()
    
    # Create and run the crew
    crew = ProblemFinder()
    crew.crew().kickoff(inputs=input_data)
    
    

def main():
    try:
        run()
    except Exception as e:
        print(f"Error running ProblemFinder: {str(e)}")
        raise

if __name__ == "__main__":
    main()
