import streamlit as st
from google import genai
import os
import time

st.set_page_config(page_title="Soft Skills & Communication Coach", page_icon="🎯", layout="centered")

st.title("🎯 Soft Skills & Communication Coach")
st.write("Sharpen your interview storytelling, professional etiquette, and workplace conversation skills.")

# API Key handling
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("Enter your Gemini API Key:", type="password")

# Select Coaching Module
module = st.selectbox(
    "Choose a practice module:",
    [
        "Interview Response (STAR Method Evaluator)",
        "Email Tone Polisher & Rephraser",
        "Workplace Conflict & Scenario Coach"
    ]
)

# Function to query Gemini with retry
def call_gemini(prompt_text):
    client = genai.Client(api_key=api_key)
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt_text
            )
            return response.text
        except Exception as e:
            if "503" in str(e) and attempt < 2:
                time.sleep(2)
                continue
            return f"Error: {e}"

# UI Forms based on selected module
if module == "Interview Response (STAR Method Evaluator)":
    st.subheader("Behavioral Interview Coach")
    question = st.text_input("Interview Question:", "Tell me about a time you handled a tight deadline or high-pressure situation.")
    user_answer = st.text_area("Your Response:", height=180, placeholder="Describe what happened, what your goal was, the specific actions you took, and the final metric/outcome...")

    if st.button("Evaluate Response", type="primary"):
        if not api_key:
            st.error("Please provide a Gemini API Key.")
        elif not user_answer.strip():
            st.warning("Please type your response first.")
        else:
            with st.spinner("Analyzing communication structure..."):
                prompt = f"""
                You are an executive interview and communication coach.
                Evaluate this candidate's behavioral answer using the STAR method (Situation, Task, Action, Result).

                Question: {question}
                Answer: {user_answer}

                Provide your feedback in this format:
                - Overall Score (out of 10)
                - Breakdown:
                  * Situation & Task: (Did they set context without rambling?)
                  * Action: (Did they focus on what *they* did vs. the team?)
                  * Result: (Is there a measurable, clear outcome?)
                - Areas to Improve:
                - Better, Stronger Example Version:
                """
                feedback = call_gemini(prompt)
                st.markdown(feedback)

elif module == "Email Tone Polisher & Rephraser":
    st.subheader("Workplace Email & Message Polisher")
    tone_goal = st.selectbox("Desired Tone:", ["Polite yet Assertive", "Professional & Formal", "Concise Executive Update", "Empathetic Follow-up"])
    raw_email = st.text_area("Draft your message:", height=150, placeholder="e.g., I need that report today or we miss the client call.")

    if st.button("Polish Communication", type="primary"):
        if not api_key:
            st.error("Please provide a Gemini API Key.")
        elif not raw_email.strip():
            st.warning("Please draft a message first.")
        else:
            with st.spinner("Rewriting for professional impact..."):
                prompt = f"""
                You are a business communications expert. Rewrite the following message to match this tone: {tone_goal}.
                
                Original Draft:
                "{raw_email}"

                Output:
                1. Rewritten Version (ready to copy and paste)
                2. Tone Breakdown (what was changed and why)
                3. Pro-Tip for delivering this message
                """
                feedback = call_gemini(prompt)
                st.markdown(feedback)

else:
    st.subheader("Workplace Scenario Coaching")
    scenario = st.selectbox(
        "Select a difficult conversation:",
        [
            "Saying 'No' to extra work when your plate is full",
            "Addressing an underperforming or unresponsive team member",
            "Negotiating salary or asking for a promotion",
            "Disagreeing with a manager's decision respectfully"
        ]
    )
    context = st.text_area("Add any specific details (optional):", placeholder="e.g., Working on a deadline for tomorrow, manager just dumped another task.")

    if st.button("Generate Conversation Script", type="primary"):
        if not api_key:
            st.error("Please provide a Gemini API Key.")
        else:
            with st.spinner("Creating conversation blueprint..."):
                prompt = f"""
                You are a senior workplace leadership coach.
                Provide a structured strategy and word-for-word script for this scenario:
                Scenario: {scenario}
                Specific context: {context if context else 'Standard corporate workplace'}

                Include:
                1. Mindset Preparation (Key psychological boundary)
                2. Word-for-Word Script (Phrased politely, clearly, and assertively)
                3. What to do if they push back
                """
                feedback = call_gemini(prompt)
                st.markdown(feedback)
