import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

def login(email, password):
    res = requests.post(f"{BACKEND_URL}/login", json={"email_id": email, "password": password})
    if res.status_code == 200 and res.json():
        st.session_state['user'] = res.json()[0]
        st.rerun()
    else:
        st.error("Login failed. Please check credentials.")

def signup(email, password, firstname, lastname, organization_id):
    res = requests.post(f"{BACKEND_URL}/signup", json={
        "firstname": firstname,
        "lastname": lastname,
        "email_id": email,
        "password": password,
        "organization_id": organization_id
    })
    if res.status_code == 200:
        st.session_state['user'] = res.json()['user']
        st.success("Sign Up successful.")
        st.rerun()
    else:
        st.error("Sign Up failed.")

def show_auth_page():
    st.title("🔐 Promptly – Secure Access")

    if st.session_state["isNewUser"]:
        st.subheader("Sign Up")
        email = st.text_input("Email ID")
        password = st.text_input("Password", type="password")
        firstname = st.text_input("First Name")
        lastname = st.text_input("Last Name")
        org_id = st.text_input("Organization ID")

        if st.button("Sign Up"):
            if all([email.strip(), password.strip(), firstname.strip(), lastname.strip(), org_id.strip()]):
                signup(email, password, firstname, lastname, org_id)
            else:
                st.error("All fields are required.")

        if st.button("Already have an account? Sign In"):
            st.session_state["isNewUser"] = False
            st.rerun()

    else:
        st.subheader("Sign In")
        email = st.text_input("Email ID")
        password = st.text_input("Password", type="password")

        if st.button("Sign In"):
            if email.strip() and password.strip():
                login(email, password)
            else:
                st.error("Please fill in all fields.")

        if st.button("New User? Sign Up"):
            st.session_state["isNewUser"] = True
            st.rerun()
