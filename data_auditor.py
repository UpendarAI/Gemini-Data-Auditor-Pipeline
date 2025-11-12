import pandas as pd
import json
import os
from google import genai
from google.genai import types

# --- 1. Setup and Initialization ---
# NOTE: The script tries to read your API key from your environment variables.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

if not GEMINI_API_KEY:
    print("----------------------------------------------------------------------")
    print("FATAL ERROR: Please set the GEMINI_API_KEY environment variable.")
    print("----------------------------------------------------------------------")
    exit()
# ... (rest of the code is the same)
