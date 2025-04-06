from model_manager import (
    run_checklist_agent,
    run_verdict_agent,
    run_risk_agent,
    run_summary_agent,
    extract_final_verdict 
)

# def analyze_rfp(rfp_text: str, company_profile: str) -> dict:
#     """
#     Runs a full Gemini-powered RFP analysis:
#     - Eligibility check
#     - Submission checklist extraction
#     - Risk analysis with full context
#     """
#     results = {}
# ########Added This code for Verdic
#     # Step 1: Eligibility Check (Verdict Agent)
#     eligibility_full_response = run_verdict_agent(rfp_text, company_profile)
#     final_verdict = extract_final_verdict(eligibility_full_response)
#     results['Eligibility Verdict'] = final_verdict
#     results['Verdict Details'] = eligibility_full_response.strip() 

#     # Step 2: Submission Checklist (Checklist Agent) with context from verdict
#     checklist = run_checklist_agent(rfp_text, eligibility)
#     results['Submission Checklist'] = checklist.strip()

#     # Step 3: Contract Risk Analysis (Risk Agent) with context from both verdict and checklist
#     risks = run_risk_agent(rfp_text, checklist, eligibility)
#     results['Contract Risks'] = risks.strip()

#     summary = run_summary_agent(results)
#     results['Executive Summary'] = summary.strip()

#     return results
def analyze_rfp(rfp_text: str, company_profile: str) -> dict:
    results = {}

    # Step 1: Run verdict agent and extract final eligibility
    eligibility_full_response = run_verdict_agent(rfp_text, company_profile)
    final_verdict = extract_final_verdict(eligibility_full_response)

    results['Eligibility Verdict'] = final_verdict
    results['Verdict Details'] = eligibility_full_response.strip()

    # Step 2: Checklist
    checklist = run_checklist_agent(rfp_text, final_verdict)
    results['Submission Checklist'] = checklist.strip()

    # Step 3: Risk analysis
    risks = run_risk_agent(rfp_text, checklist, final_verdict)
    results['Contract Risks'] = risks.strip()

    # Step 4: Summary
    summary = run_summary_agent(results)
    results['Executive Summary'] = summary.strip()

    return results
