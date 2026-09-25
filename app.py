import os
import streamlit as st
from google import genai


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Soft Skills And Communication Coach",
    page_icon="🎯",
    layout="centered"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🎯 Soft Skills & Communication Coach")

st.write(
    "Practice behavioral interview answers, polish workplace emails, "
    "and master difficult professional conversations."
)


# --------------------------------------------------
# GEMINI API KEY FROM ENVIRONMENT
# --------------------------------------------------

api_key = os.getenv("GOOGLE_API_KEY")


# --------------------------------------------------
# SELECT MODULE
# --------------------------------------------------

module = st.selectbox(
    "Choose a practice module:",
    [
        "Interview Response (STAR Method Evaluator)",
        "Email Tone Polisher & Rephraser",
        "Workplace Scenario Coach"
    ]
)


# --------------------------------------------------
# FORM INTERFACES
# --------------------------------------------------

prompt = ""
ready_to_send = False

if module == "Interview Response (STAR Method Evaluator)":
    st.subheader("Behavioral Interview Coach")
    question = st.text_input(
        "Interview Question:",
        value="Tell me about a time you handled a tight deadline or high-pressure situation."
    )
    user_answer = st.text_area(
        "Your Response:",
        height=180,
        placeholder="Describe the situation, your specific role, what action you took, and the final measurable outcome..."
    )

    if st.button("Evaluate Response", type="primary"):
        if not user_answer.strip():
            st.warning("Please type your response before submitting.")
        else:
            ready_to_send = True
            prompt = f"""
You are an executive interview and communication coach.
Evaluate this candidate's behavioral answer using the STAR method (Situation, Task, Action, Result).

Question: {question}
Answer: {user_answer}

Provide your feedback in this format:
- Overall Score (out of 10)
- Breakdown:
  * Situation & Task: (Did they set context without rambling?)
  * Action: (Did they highlight what they personally contributed?)
  * Result: (Is there a measurable, tangible outcome?)
- Areas to Improve:
- Improved, High-Impact Version:
"""

elif module == "Email Tone Polisher & Rephraser":
    st.subheader("Workplace Email & Message Polisher")
    tone_goal = st.selectbox(
        "Desired Tone:",
        [
            "Polite yet Assertive",
            "Professional & Formal",
            "Concise Executive Update",
            "Empathetic Follow-up"
        ]
    )
    raw_email = st.text_area(
        "Draft your message:",
        height=150,
        placeholder="e.g., Send me that report today because the client needs it right now."
    )

    if st.button("Polish Communication", type="primary"):
        if not raw_email.strip():
            st.warning("Please enter a message to polish.")
        else:
            ready_to_send = True
            prompt = f"""
You are a corporate communication specialist. Rewrite the following message to match this tone: {tone_goal}.

Original Message:
"{raw_email}"

Output Format:
1. Polished Version (ready to copy and paste)
2. Tone Breakdown (what was changed and why)
3. Delivery Tip (best timing or delivery approach)
"""

else:
    st.subheader("Workplace Scenario Coaching")
    scenario = st.selectbox(
        "Select a conversation scenario:",
        [
            "Saying 'No' to extra work when your plate is full",
            "Addressing an underperforming or unresponsive team member",
            "Negotiating salary or asking for a promotion",
            "Disagreeing with a manager's decision respectfully"
        ]
    )
    context = st.text_area(
        "Add specific details (optional):",
        placeholder="e.g., I have a project deadline tomorrow, and my team lead asked me to review 5 pull requests today."
    )

    if st.button("Generate Conversation Script", type="primary"):
        ready_to_send = True
        prompt = f"""
You are a senior leadership and workplace negotiation coach.
Provide a clear, tactful script and strategy for this scenario:

Scenario: {scenario}
Details: {context if context else 'Standard professional office environment'}

Output Format:
1. Key Mindset Boundary (how to think about this conversation)
2. Word-for-Word Script (assertive, polite, and professional)
3. How to Handle Pushback (if the other person resists)
"""


# --------------------------------------------------
# GENERATE ANSWER
# --------------------------------------------------

if ready_to_send:

    try:
        with st.spinner("Analyzing and generating coaching guidance..."):

            # Create Gemini client
            client = genai.Client(api_key=api_key)

            # Gemini Model Fallback
            models_to_try = [
                "gemini-3.8-flash",
                "gemini-3.7-flash",
                "gemini-3.5-flash"
            ]

            response = None
            last_error = None
            successful_model = None

            for model_name in models_to_try:
                try:
                    response = client.models.generate_content(
                        model=model_name,
                        contents=prompt
                    )
                    if response.text:
                        successful_model = model_name
                        break
                except Exception as e:
                    last_error = e
                    continue

            # If all models fail
            if response is None or not response.text:
                raise Exception(
                    "All Gemini models are temporarily unavailable. "
                    f"Please try again later. Last error: {last_error}"
                )

            # Display Output
            st.subheader("Coach Advice & Output:")
            st.markdown(response.text)

            st.caption(f"Generated using: {successful_model}")

    except Exception as e:
        st.error(f"Error generating response: {e}")
