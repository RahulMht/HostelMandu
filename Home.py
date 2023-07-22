import streamlit as st
import requests
from streamlit_lottie import st_lottie 
import firebase_admin
import pyrebase
from firebase_admin import credentials
from firebase_admin import auth

col1, col2 = st.columns([1, 1])

with col1:
    # Page title and team members
    st.title("Hostel Finder 🏡")
    st.subheader("_Project by team: Let Us(Isha Hitang, Priyanka Sinha, Sahishna Budhathoki)")
    # Home page content
    st.write("Welcome to the Hostel Finder application!🙏")
    st.markdown("The project is a **hostel finder** application designed to assist **:violet[college students]** in **__[finding suitable hostels near their college__** that fit their **:blue[budget and room-sharing preferences]**. It provides a user-friendly interface where students can input their college name, preferred room type (**:orange[__single, 2-sharing, or 3-sharing__)]**, and **:green[price range.]**")
    st.caption("The Fisebase serves as the database and Authenticaton for the application.💾")
with col2:
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    lottie_hello = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_gClLfk.json")
    
    st_lottie(
        lottie_hello,
        speed=1,
        reverse=False,
        loop=True,
        quality="high", 
        width=500,
        key=None,
    )
    firebaseConfig = {
  'apiKey': "AIzaSyBQ1lnRueNB8ZljI6lgYRryTSq-x3fdZxU",
  'authDomain': "campusday-aebdc.firebaseapp.com",
  'databaseURL': "https://campusday-aebdc-default-rtdb.firebaseio.com",
  'projectId': "campusday-aebdc",
  'storageBucket': "campusday-aebdc.appspot.com",
  'messagingSenderId': "132302673110",
  'appId': "1:132302673110:web:deec03b22a6202fd30a577",
  'measurementId': "G-NJ2F7VZ1ZQ"
};

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
auth_pyrebase = firebase.auth()

# Initialize Firebase with Admin SDK
cred = credentials.Certificate("pages/campusday-aebdc-94e7767c0207.json")
# firebase_admin.initialize_app(cred)
auth_admin = auth

def login():
    st.sidebar.header("Login")

    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        try:
            auth_pyrebase.sign_in_with_email_and_password(email,password)
            
            user = auth.get_user_by_email(email)
            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            
            global Usernm
            Usernm=(user.uid)

            st.session_state.signedout = True
            st.session_state.signout = True
            st.sidebar.success("Login successful!")
        except Exception as e:
            st.sidebar.error("Login failed. Please check your credentials.")
            st.error(e)

def sign_up():
    st.sidebar.header("Sign Up")

    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    username = st.sidebar.text_input("Enter unique username")
    phone = st.sidebar.number_input('Insert your phone number', min_value=9700000000)
     

    if st.sidebar.button("Sign Up"):
        try:
            user = auth.create_user(email = email, password = password,uid=username)

            db.child("username").child(username).child("emails").set(user.email)
            db.child("username").child(username).child("Phone").set(phone)
            # SDK to update user display name
            #auth_admin.update_user(user['localId'], display_name=username)
            st.sidebar.success("Sign up successful!")
            st.sidebar.markdown("Please Login using your email and password")
            st.sidebar.balloons()
        except Exception as e:
            st.sidebar.error("Sign up failed.")
            st.sidebar.error(e)

def reset_password():
    st.sidebar.header("Reset Password")

    email = st.sidebar.text_input("Email")

    if st.sidebar.button("Reset Password"):
        try:
            auth_pyrebase.send_password_reset_email(email)
            st.sidebar.success("Password reset email sent! Please check your email.")
        except Exception as e:
            st.sidebar.error("Failed to send password reset email.")
            st.sidebar.error(e)

def main():
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    if "signedout" not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False

    if not st.session_state["signedout"]:
        choice = st.sidebar.radio('', ['Login', 'Sign up', 'Reset'],horizontal= True)
        if choice == 'Sign up':
            sign_up()
        elif choice == 'Login':
            login()
        elif choice == 'Reset':
            reset_password()

    if st.session_state.signout:
        st.sidebar.success('You are logged in as ' + st.session_state.username +", Welcome!", icon="✅")
        

if __name__ == "__main__":
    main()
