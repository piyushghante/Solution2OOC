import streamlit as st

def display_markdown_report(report: str):
    """
    Renders a formatted markdown report in Streamlit.
    """
    if report and report.strip():
        st.markdown(report, unsafe_allow_html=True)
    # else:
    #     st.info("ℹ️ No report to display.")



def highlight_verdict(text: str):
    """
    Highlights eligibility verdict in green (eligible), red (not eligible), or yellow (unclear).
    """
    verdict = text.upper()
    
    
    if "NOT ELIGIBLE" in verdict:
        st.error("🚫 Verdict: NOT ELIGIBLE")
    elif "ELIGIBLE" in verdict:
        st.success("✅ Verdict: ELIGIBLE")
    elif "UNCLEAR" in verdict:
        st.warning("⚠️ Verdict: UNCLEAR")
    else:
        st.info("ℹ️ Verdict not found or unrecognized.")
    return verdict 
