## 🚀 Gemini Data Auditor Pipeline (Python + Structured AI)

This project demonstrates the integration of **Gemini AI** into a fundamental Data Engineering workflow to automate and enhance data quality assurance. It uses Python and the Google Generative AI SDK to audit structured data based on natural language business rules, outputting a clear, structured JSON audit log.

This project showcases competency in **AI Integration, Data Quality (DQ), ETL principles, Python scripting, and structured API usage (JSON Schema)**—all essential skills for Data Analyst and Entry-Level Data Engineer roles.

---

### 💡 Core Concept: Replacing Rigid Rules with Flexible AI

Instead of writing hundreds of lines of brittle `IF/ELSE` logic for data validation, this pipeline uses the Gemini model to dynamically check for quality issues (missing values, logical errors, format errors) based on simple, plain-text instructions. The AI enforces data governance, making the ETL process faster and more adaptable.

### Technical Stack

* **Language:** Python 3.9+
* **AI/LLM:** **Google Gemini API** (`gemini-2.5-flash`)
* **Data Processing:** Pandas (for simulating data load/transformation)
* **Key Feature:** Structured Output using **JSON Schema** (`types.GenerateContentConfig`)

### 🛠️ Installation and Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YourGitHubUsername/Gemini-Data-Auditor-Pipeline.git](https://github.com/YourGitHubUsername/Gemini-Data-Auditor-Pipeline.git)
    cd Gemini-Data-Auditor-Pipeline
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Your API Key:**
    Before running, you must set your Gemini API key as an environment variable.

    **Mac/Linux:**
    ```bash
    export GEMINI_API_KEY='YOUR_API_KEY_HERE'
    ```
    **Windows (PowerShell):**
    ```bash
    $env:GEMINI_API_KEY='YOUR_API_KEY_HERE'
    ```

### ▶️ How to Run the Pipeline

Execute the main Python script directly:

```bash
python data_auditor.py
