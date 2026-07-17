import streamlit as st
import pandas as pd
import requests
from pdf_generator import generate_pdf
# FastAPI Backend URL
import os


try:
    BACKEND_URL = st.secrets["BACKEND_URL"]
except Exception:
    BACKEND_URL = os.getenv(
        "BACKEND_URL",
        "https://ai-startup-idea-validator-yz0v.onrender.com",
    )

BACKEND_URL = BACKEND_URL.rstrip("/")

def api_error_message(response, fallback="Request failed"):
    try:
        payload = response.json()
        if isinstance(payload, dict):
            detail = payload.get("detail", fallback)
            if isinstance(detail, list):
                return "; ".join(str(item) for item in detail)
            return str(detail)
    except requests.exceptions.JSONDecodeError:
        text = response.text.strip()
        if text:
            return text
    return f"{fallback} (HTTP {response.status_code})"
st.set_page_config(
    page_title="AI Startup Idea Validator",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("💡 AI Startup Idea Validator")

# --- Session State Management ---
if "token" not in st.session_state:
    st.session_state.token = None
if "page" not in st.session_state:
    st.session_state.page = "auth"
if "username" not in st.session_state:
    st.session_state.username = None

# --- Helper Functions ---
def set_page(page_name):
    st.session_state.page = page_name

def show_auth_page():
    st.session_state.page = "auth"
    st.session_state.token = None
    st.session_state.username = None

def get_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}

# --- Authentication Pages ---
def render_auth_page():
    st.sidebar.header("Authentication")
    auth_choice = st.sidebar.radio("Choose an option:", ["Login", "Sign Up"])

    if auth_choice == "Sign Up":
        with st.form("signup_form"):
            st.subheader("Create a New Account")
            new_username = st.text_input("Username", key="signup_username")
            new_password = st.text_input("Password", type="password", key="signup_password")
            submit_button = st.form_submit_button("Sign Up")

            if submit_button:
                if new_username and new_password:
                    try:
                        response = requests.post(
                            f"{BACKEND_URL}/signin",
                            json={"username": new_username, "password": new_password},
                            timeout=60,
                        )
                        if response.status_code == 200:
                            st.success("Account created successfully! Please log in.")
                        else:
                            st.error(f"Sign Up failed: {api_error_message(response, 'Unknown error')}")
                    except requests.exceptions.ConnectionError:
                        st.error("Could not connect to the backend server. Please check if it's running.")
                    except requests.exceptions.RequestException as exc:
                        st.error(f"Sign Up failed: {exc}")
                else:
                    st.warning("Please enter a username and password.")

    elif auth_choice == "Login":
        with st.form("login_form"):
            st.subheader("Login to your Account")
            username = st.text_input("Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            submit_button = st.form_submit_button("Login")

            if submit_button:
                if username and password:
                    try:
                        response = requests.post(
                            f"{BACKEND_URL}/login",
                            data={"username": username, "password": password},
                            timeout=60,
                        )
                        if response.status_code == 200:
                            token_data = response.json()
                            st.session_state.token = token_data["access_token"]
                            st.session_state.username = username
                            st.success("Login successful!")
                            set_page("main")
                            st.rerun()
                        else:
                            st.error(f"Login failed: {api_error_message(response, 'Invalid credentials')}")
                    except requests.exceptions.ConnectionError:
                        st.error("Could not connect to the backend server. Please check if it's running.")
                    except requests.exceptions.RequestException as exc:
                        st.error(f"Login failed: {exc}")
                else:
                    st.warning("Please enter your username and password.")

# --- Main Application Page ---
def render_main_page():
    # st.sidebar.success(f"Logged in as **{st.session_state.username}**")
    st.sidebar.markdown("### 👤 User")
    st.sidebar.success(st.session_state.username)
    st.sidebar.button("Logout", on_click=show_auth_page)
    st.sidebar.markdown("---")
    st.sidebar.button("Submit New Idea", on_click=lambda: set_page("main"))
    st.sidebar.button("View History", on_click=lambda: set_page("history"))

    st.subheader("Submit a Startup Idea for Evaluation")
    idea_text = st.text_area("Describe your startup idea:", height=200)
    
    col1, col2 = st.columns([1, 4])
    with col1:
        validate_button = st.button("Validate Idea")

    if validate_button and idea_text:
        with st.spinner("🤖 Evaluating your startup idea... This may take a few seconds."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/ideas", 
                    json={"startup_idea" : idea_text}, 
                    headers=get_headers(),
                    timeout=60
                )
                
                if response.status_code == 201:
                    evaluation_data = response.json()
                    st.session_state.last_evaluation = evaluation_data
                    st.session_state.idea_evaluated = True
                    st.success("Evaluation complete!")
                    st.rerun()
                elif response.status_code == 401:
                    st.error("Your session has expired. Please log in again.")
                    show_auth_page()
                    st.rerun()
                elif response.status_code == 500:
                    detail = api_error_message(response, "Server error")

                    if "503" in str(detail):
                        st.warning(
                            "⚠️ Gemini AI is currently experiencing high demand.\n\n"
                            "Please wait a few seconds and try again."
                        )
                    else:
                        st.error(detail)
                else:
                    st.error(f"Error: {api_error_message(response, 'Failed to get evaluation.')}")
            except requests.exceptions.ConnectionError:
                st.error(
                    "❌ Unable to connect to the backend service. "
                    "Please try again later."
                )   

    if "last_evaluation" in st.session_state and st.session_state.get("idea_evaluated", False):
        st.markdown("---")
        display_evaluation(st.session_state.last_evaluation)

def display_evaluation(evaluation_data):
    st.subheader(f"Evaluation for: *{evaluation_data['startup_idea']}*")
    
    if 'thinker' in evaluation_data and evaluation_data['thinker'] is not None:
        st.caption(f"Submitted by: **{evaluation_data['thinker']['username']}**")
    
    categories = ["creativity", "demand", "uniqueness", "scale", "investment"]
    
    scores_dict = {}
    for cat in categories:
        score_key = f"{cat}_score"
        if score_key in evaluation_data and evaluation_data[score_key] is not None:
            scores_dict[cat.title()] = evaluation_data[score_key]

    if scores_dict:
        # Create a DataFrame for the bar chart
        scores_df = pd.DataFrame(
            {'Category': scores_dict.keys(), 'Score': scores_dict.values()}
        )
        scores_df = scores_df.set_index('Category')
        overall = sum(scores_dict.values()) / len(scores_dict)

        st.metric(
            label="⭐ Overall Startup Score",
            value=f"{overall:.1f}/10"
        )

        st.markdown("#### Overall Score Analysis (1-10)")
        st.bar_chart(scores_df, use_container_width=True)
    else:
        st.warning("No scores available for this idea.")

    st.markdown("---")
    st.markdown("#### Detailed AI Feedback")
    
    col_scores, col_statements = st.columns([1, 4])
    
    with col_scores:
        st.markdown("##### Scores")
        for cat in categories:
            score_key = f"{cat}_score"
            if score_key in evaluation_data and evaluation_data[score_key] is not None:
                score = evaluation_data[score_key]
                st.metric(cat.title(), f"{score}/10")
                st.progress(score / 10)                
                st.markdown("---")

    with col_statements:
        st.markdown("##### Statements")
        for cat in categories:
            sentence_key = f"{cat}_sentence"
            if sentence_key in evaluation_data and evaluation_data[sentence_key] is not None:
                sentence = evaluation_data[sentence_key]
                st.info(sentence)
                st.markdown("---")
    pdf = generate_pdf(evaluation_data)

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf,
        file_name="startup_report.pdf",
        mime="application/pdf",
    )

# --- History Page ---
def render_history_page():
    st.sidebar.success(f"Logged in as **{st.session_state.username}**")
    st.sidebar.button("Logout", on_click=show_auth_page)
    st.sidebar.markdown("---")
    st.sidebar.button("Submit New Idea", on_click=lambda: set_page("main"))
    st.sidebar.button("View History", on_click=lambda: set_page("history"))

    st.subheader("Your Past Idea Evaluations")
    try:
        response = requests.get(f"{BACKEND_URL}/ideas/history", headers=get_headers())

        if response.status_code == 200:
            history_data = response.json()
            if history_data:
                for item in history_data:
                    with st.expander(f"**Idea:** {item['startup_idea'][:50]}..."):
                        display_evaluation(item)
                        st.markdown("---")
            else:
                st.info("You have no past evaluations yet. Submit a new idea to get started!")
        elif response.status_code == 401:
            st.error("Your session has expired. Please log in again.")
            show_auth_page()
            st.experimental_rerun()
        else:
            st.error(f"Error fetching history: {api_error_message(response, 'Failed to retrieve data.')}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend server. Please check if it's running.")

# --- Main App Logic ---
if st.session_state.page == "auth" or not st.session_state.token:
    render_auth_page()
elif st.session_state.page == "main":
    render_main_page()
elif st.session_state.page == "history":
    render_history_page()

st.markdown("-D-D-")

st.caption(
    "Built with Nightless sleep using FastAPI • Streamlit • PostgreSQL • SQLAlchemy • Gemini AI"
)