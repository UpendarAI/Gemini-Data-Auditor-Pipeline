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

try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    exit()

# Define the Structured JSON Schema for AI Output
# This tells Gemini exactly what format to return the audit results in.
AUDIT_SCHEMA = {
    "type": "object",
    "properties": {
        "record_id": {"type": "integer"},
        "data_issue_type": {"type": "string", "enum": ["MissingValue", "LogicalError", "FormatError", "Clean"], "description": "The main type of data issue."},
        "flag_severity": {"type": "string", "enum": ["HIGH", "MEDIUM", "LOW"], "description": "Severity of the issue."},
        "recommended_action": {"type": "string", "description": "Action to fix the data (e.g., 'Impute value with mean', 'Reject record')."}
    },
    "required": ["record_id", "data_issue_type", "flag_severity", "recommended_action"]
}

# --- 2. The Core AI Auditor Function (The heavy lifting happens here) ---
def audit_record(record_data: dict, schema: dict) -> dict:
    """Uses Gemini to audit a single dictionary record against strict business rules."""
    
    # Convert the Python dictionary into a JSON string for the AI
    record_json = json.dumps(record_data)
    
    # Simple, clear instructions (The business rules)
    system_instruction = (
        "You are an automated Data Quality Auditor. Analyze the record for quality issues based on these rules: "
        "1. Any missing 'name' or 'city' is a 'MissingValue' (HIGH severity). "
        "2. Any 'spend_usd' value over $1000 is a 'LogicalError' (MEDIUM severity) unless 'is_premium' is True. "
        "3. Any record failing the rules above must be flagged. If all fields are valid, mark as 'Clean' (LOW severity)."
    )
    
    try:
        # Call the Gemini API!
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"Audit this customer record: {record_json}",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=schema,
            ),
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"  [ERROR] AI analysis failed for ID {record_data.get('id', 'Unknown')}: {e}")
        return {"record_id": record_data.get('id'), "data_issue_type": "SystemError", "flag_severity": "HIGH", "recommended_action": "Manual review required."}

# --- 3. Main Execution Function (Simple Python Flow) ---
def run_data_auditor():
    """Simulates loading data and auditing each record."""
    print("--- Starting Gemini Data Auditor Pipeline ---")
    
    # 3.1 Load Simulated Data using Pandas (Your simple ETL step)
    data = {
        'id': [101, 102, 103, 104, 105],
        'name': ['Alice Johnson', 'Bob Smith', 'Carlos Rivera', '', 'Eve Adams'], 
        'city': ['NYC', 'Boston', '', 'LA', 'Denver'],
        'spend_usd': [150, 1200, 50, 999, 15000],
        'is_premium': [False, False, False, True, False]
    }
    df = pd.DataFrame(data)
    print(f"Total records loaded: {len(df)}")

    audited_results = []
    
    # 3.2 Loop through each row (Simple Python logic)
    for index, row in df.iterrows():
        record_dict = row.to_dict() 
        
        print(f"\nAuditing ID: {record_dict['id']}...")
        
        audit_output = audit_record(record_dict, AUDIT_SCHEMA)
        
        audited_results.append(audit_output)
        print(f"  -> Issue: {audit_output.get('data_issue_type')} ({audit_output.get('flag_severity')}). Action: {audit_output.get('recommended_action')}")

    # 3.3 Create Final Report (Simple Python logic)
    clean_count = sum(1 for r in audited_results if r.get('data_issue_type') == 'Clean')
    high_count = sum(1 for r in audited_results if r.get('flag_severity') == 'HIGH')
    total_count = len(audited_results)

    print("\n\n--- FINAL DATA AUDIT REPORT ---")
    print(f"Total Records: {total_count}")
    print(f"Clean Records: {clean_count}")
    print(f"High Severity Flags: {high_count}")
    print("-----------------------------------")


if __name__ == "__main__":
    run_data_auditor()
