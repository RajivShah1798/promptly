import streamlit as st
import requests
import json
from streamlit_lottie import st_lottie

# API endpoint
BACKEND_URL = "http://127.0.0.1:8000"

# ------------------- AUTHENTICATION ------------------- #

def login(email, password):
    res = requests.post(f"{BACKEND_URL}/login", json={
        "email_id": email,
        "password": password
    })
    if res.status_code == 200 and res.json():
        st.session_state["user"] = res.json()[0]
        st.rerun()
    else:
        st.error("❌ Login failed. Please double-check your credentials.")

def signup(email, password, firstname, lastname, organization_id):
    res = requests.post(f"{BACKEND_URL}/signup", json={
        "firstname": firstname,
        "lastname": lastname,
        "email_id": email,
        "password": password,
        "organization_id": organization_id
    })
    if res.status_code == 200:
        st.session_state["user"] = res.json()["user"]
        st.success("✅ Account created successfully! Redirecting...")
        st.rerun()
    else:
        st.error("❌ Sign up failed. Please try again or contact support.")

# ------------------- LOTTIE LOADER ------------------- #

def load_lottie(path: str):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        st.warning("⚠️ Animation failed to load.")
        return None

# ------------------- AUTH UI ENTRYPOINT ------------------- #

def show_auth_page():
    # Inject CSS
    with open("frontend/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Load Lottie animation
    lottie_logo = load_lottie("frontend/assets/promptly-logo-animation.json")

    # Branding section
    st.markdown("""
    <div class="promptly-auth-container">
        <div>
            <div class="promptly-logo-text">Promptly</div>
            <div class="promptly-tagline">Ask anything. <span style='color:#ffffff;'>Find everything.</span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st_lottie(lottie_logo, height=200, key="promptly-logo")

    st.markdown("---")

    # ---------------- Sign Up ---------------- #
    if st.session_state.get("isNewUser", False):
        st.subheader("📝 Create Your Free Account")

        col1, col2 = st.columns(2)
        with col1:
            firstname = st.text_input("🧑 First Name")
            org_id = st.text_input("🏢 Organization ID")
        with col2:
            lastname = st.text_input("🧑 Last Name")
            email = st.text_input("✉️ Email Address")

        password = st.text_input("🔒 Choose a Password", type="password")

        if st.button("🎉 Sign Up", use_container_width=True):
            if all([email.strip(), password.strip(), firstname.strip(), lastname.strip(), org_id.strip()]):
                signup(email, password, firstname, lastname, org_id)
            else:
                st.warning("⚠️ Please fill in all fields to proceed.")

        st.markdown("---")
        st.markdown("<div style='text-align:center;'>Already have an account?</div>", unsafe_allow_html=True)
        if st.button("🔁 Back to Sign In", use_container_width=True):
            st.session_state["isNewUser"] = False
            st.rerun()

    # ---------------- Sign In ---------------- #
    else:
        st.subheader("🔐 Log In to Your Account")

        email = st.text_input("✉️ Email Address")
        password = st.text_input("🔑 Password", type="password")

        if st.button("🔓 Sign In", use_container_width=True):
            if email.strip() and password.strip():
                login(email, password)
            else:
                st.warning("⚠️ Please enter both email and password.")

        st.markdown("---")
        st.markdown("<div style='text-align:center;'>Don't have an account yet?</div>", unsafe_allow_html=True)
        if st.button("🆕 Create New Account", use_container_width=True):
            st.session_state["isNewUser"] = True
            st.rerun()
