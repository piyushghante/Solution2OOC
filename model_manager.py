import google.generativeai as genai
import streamlit as st
import re

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
    match = re.search(
        r"Final\s+Verdict\s*[:\-]?\s*(ELIGIBLE|NOT ELIGIBLE|UNCLEAR)",
        text,
        re.IGNORECASE
    )
    return match.group(1).upper() if match else "UNCLEAR"

# Agent 1: Verdict Agent
def run_verdict_agent(rfp_text: str, company_profile: str) -> str:
    prompt = f"""
You are a government procurement compliance expert.

Your job is to determine if the company is eligible to bid on the RFP. Follow the structured steps below strictly and be objective.

## STEP 1: Extract Key Eligibility Criteria from the RFP
List all mandatory eligibility criteria. Use bullet points. Include requirements like:
- Years of experience
- Certifications
- Turnover/financial thresholds
- Legal registrations
- Specific technical capabilities
- Past project experience

## STEP 2: Identify Deal-Breaker Requirements
Clearly highlight any criteria that are non-negotiable or will disqualify the bidder if unmet.

## STEP 3: Evaluate Company Profile Against Each Criteria
For each requirement from Step 1, say whether the company **Meets** or **Does Not Meet** it. Justify briefly.

Use this format:
- Requirement: [quoted requirement]
  - Company Status: Meets / Does Not Meet / Unclear
  - Reason: [brief explanation]

## STEP 4: Final Verdict
Based on the evaluation above, write this line clearly at the end:

Final Verdict: [ELIGIBLE / NOT ELIGIBLE / UNCLEAR]

Be strict and accurate. Do not make assumptions beyond the provided text.

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
