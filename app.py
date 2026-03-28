
import time
import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
import re

genai.configure(api_key="GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-2.5-flash")

PROMPT = """
Analyze this conversation for warning signs. Return ONLY valid JSON:
{
  "risk_score": 0-100,
  "risk_level": "LOW/MEDIUM/HIGH/DANGER",
  "red_flags": ["flag1", "flag2"],
  "patterns": ["manipulation", "threats", "gaslighting"],
  "recommendation": "specific advice"
}
"""

def display_results(result):
    score = result["risk_score"]
    level = result["risk_level"]
    
    color = {"LOW":"🟢","MEDIUM":"🟡","HIGH":"🟠","DANGER":"🔴"}
    st.metric("Risk Score", f"{score}/100")
    st.markdown(f"## {color[level]} {level} RISK")
    
    if result["red_flags"]:
        st.error("🚩 Red Flags Detected:")
        for flag in result["red_flags"]:
            st.write(f"• {flag}")
    
    st.info(f"💡 Recommendation: {result['recommendation']}")

st.title("🚨 Conversation Risk Analyzer")
st.caption("Upload a screenshot or paste text to analyze for red flags")

tab1, tab2 = st.tabs(["📸 Screenshot", "📝 Text"])

with tab1:
    uploaded = st.file_uploader("Upload conversation screenshot", type=["png","jpg","jpeg"])
    if uploaded and st.button("Analyze Image"):
        image = Image.open(uploaded)
        st.image(image, caption="Uploaded conversation")
        with st.spinner("Analyzing..."):
            time.sleep(2)
            response = model.generate_content([PROMPT, image])
            response_text = response.text.strip()
            response_text = re.sub(r'```json|```', '', response_text).strip()
            result = json.loads(response_text)
            display_results(result)

with tab2:
    text = st.text_area("Paste conversation here", height=200)
    if text and st.button("Analyze Text"):
        with st.spinner("Analyzing..."):
            time.sleep(2)
            response = model.generate_content(PROMPT + "\n\nConversation:\n" + text)
            response_text = response.text.strip()
            response_text = re.sub(r'```json|```', '', response_text).strip()
            result = json.loads(response_text)
            display_results(result)