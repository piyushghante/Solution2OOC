import google.generativeai as genai
import streamlit as st
import re
import json 

# Load separate API keys for each agent from Streamlit secrets
API_KEYS = {
    "verdict": st.secrets["GEMINI_KEY_VERDICT"],
    "checklist": st.secrets["GEMINI_KEY_CHECKLIST"],
    "risk": st.secrets["GEMINI_KEY_RISK"],
    "analyzer": st.secrets["GEMINI_KEY_ANALYZER"]
}

MODEL_NAME = "models/gemini-2.0-flash"

# Utility: Run Gemini with a specific agent and prompt
def run_gemini_prompt(prompt: str, agent: str) -> str:
    try:
        genai.configure(api_key=API_KEYS[agent])
        model = genai.GenerativeModel(model_name=MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Gemini API Error for {agent.upper()} Agent: {str(e)}"

# Utility: Extract final verdict from Gemini's response
def extract_final_verdict(text: str) -> str:
    try:
        json_start = text.find("{")
        json_text = text[json_start:]
        parsed = json.loads(json_text)
        return parsed.get("verdict", "UNCLEAR").upper()
    except Exception as e:
        print("❌ Failed to extract verdict JSON:", e)
        return "UNCLEAR"

# Agent 1: Verdict Agent
def run_verdict_agent(rfp_text: str, company_profile: str) -> str:
    prompt = f"""
You are a government procurement compliance expert.

Your task is to evaluate whether the company is eligible to bid for the given RFP. Return a strictly formatted JSON response.

--- TASK INSTRUCTIONS ---
1. Extract key eligibility criteria
2. Identify deal-breaker requirements
3. Evaluate the company against each criterion
4. Based on this, return a JSON object in this format:

{{
  "verdict": "ELIGIBLE",        // or "NOT ELIGIBLE" or "UNCLEAR"
  "reasoning": "Brief summary of why this verdict was reached.",
  "evaluation": [
    {{
      "requirement": "string",
      "status": "Meets / Does Not Meet / Unclear",
      "reason": "short justification"
    }}
  ]
}}

✅ Only return a valid JSON object.
✅ Do NOT include markdown, headings, or explanations outside the JSON.

--- RFP TEXT ---
{rfp_text}

--- COMPANY PROFILE ---
{company_profile}
"""
    return run_gemini_prompt(prompt, "verdict")

# Agent 2: Checklist Agent
def run_checklist_agent(rfp_text: str, verdict: str) -> str:
    prompt = f"""
You are a compliance analyst specializing in procurement. Based on the provided RFP document and the eligibility verdict, create a detailed submission compliance checklist for vendors. The checklist should help ensure that all submission requirements are met.

Include the following categories:

1. Document Formatting Requirements  
2. Mandatory Forms and Attachments  
3. Submission Timeline and Deadlines  
4. Submission Method and Contact Details  

Make it short, clear, and easy to follow.

--- ELIGIBILITY VERDICT ---
{verdict}

--- RFP TEXT ---
{rfp_text}
"""
    return run_gemini_prompt(prompt, "checklist")

# Agent 3: Risk Agent
def run_risk_agent(rfp_text: str, checklist: str, verdict: str) -> str:
    prompt = f"""
You are a legal expert specializing in contract and procurement law. Based on the provided RFP document, the extracted eligibility checklist, and the eligibility verdict, identify any clauses that may be:

- Risky (e.g., vague, overly restrictive, non-compliant with procurement norms)
- Biased (e.g., unfairly favoring a particular vendor or limiting fair competition)

For each identified issue:
1. Quote the clause
2. Explain why it is risky or biased
3. Suggest a mitigation or alternative wording

Keep the analysis short, simple, and based on best practices.

--- ELIGIBILITY VERDICT ---
{verdict}

--- CHECKLIST ---
{checklist}

--- RFP TEXT ---
{rfp_text}
"""
    return run_gemini_prompt(prompt, "risk")

# Agent 4: Summary Agent
def run_summary_agent(analysis: dict) -> str:
    prompt = f"""
You are a summarization expert. Summarize the following RFP analysis report into a short, clear executive summary.

The summary should:
- Briefly state if the company is eligible
- Mention any major deal-breakers
- Highlight key submission checklist items
- Flag any serious contract risks

Keep it under 150 words and easy to understand.

--- FULL ANALYSIS REPORT ---
Eligibility:
{analysis.get("Eligibility Verdict", "")}

Checklist:
{analysis.get("Submission Checklist", "")}

Risks:
{analysis.get("Contract Risks", "")}
"""
    return run_gemini_prompt(prompt, "analyzer")
