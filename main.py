import streamlit as st
from datetime import datetime
import base64
import os
import secrets
import hashlib

if not os.path.exists('users.txt'):
    with open('users.txt', 'w') as users:
        users.writelines([])

def sha256(password):
    salt = os.urandom(32)
    pwd = password.encode('utf-8')
    kdf = hashlib.pbkdf2_hmac('sha256', pwd, salt, 100000)
    return base64.b64encode(salt + kdf)

def check_password(hashed_password, password):
    decoded_pass = base64.b64decode(hashed_password)
    salt = decoded_pass[:32]
    kdf = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return base64.b64encode(salt + kdf) == hashed_password

def save_user(username, email, hashed_password):
    with open('users.txt', 'ab') as users:
        user_info = f"{username},{email},{hashed_password}\n".encode()
        users.write(user_info)

def load_users():
    users = []
    with open('users.txt', 'rb') as ufile:
        for line in ufile:
            info = line.strip().decode()
            username, email, hashed_password = info.split(",")
            users.append((username, email, hashed_password))
    return users

STYLE = """
<style>
body {{
    padding: 2rem;
    margin: auto;
    max-width: 80%;
    box-shadow: 0 0.5rem 1.5rem rgba(0, 0, 0, 0.2);
    border-radius: 0.5rem;
    background-color: #fafbfc;
}}

h1 {{
    font-family: Arial, sans-serif;
    font-weight: bold;
    font-size: 2.5rem;
    line-height: 1.2;
    letter-spacing: 0.02em;
    color: #1c3fa3;
    margin-bottom: 2rem;
}}

label {{
    display: inline-block;
    margin-top: 0.5rem;
    margin-right: 0.5rem;
    font-weight: bold;
    color: #2b2b2b;
}}

input[type="text"],
input[type="password"] {{
    border: none;
    outline: none;
    border-radius: 0.25rem;
    padding: 0.5rem 1rem;
    margin-bottom: 1rem;
    font-size: 1rem;
    line-height: 1.5;
    width: calc(100% - 2rem);
    background-color: #fff;
    box-shadow: 0 0.25rem 0.5rem rgba(0, 0, 0, 0.1);
}}

button {{
    cursor: pointer;
    border: none;
    border-radius: 0.25rem;
    padding: 0.5rem 2rem;
    font-size: 1rem;
    line-height: 1.5;
    font-weight: bold;
    color: #fff;
    background-color: #1c3fa3;
    transition: background-color 0.25s ease-out;
}}

button:hover {{
    background-color: #0c234c;
}}
</style>
"""

st.markdown(STYLE, unsafe_allow_html=True)

# Load users
users = load_users()

st.title('Welcome to :black[USD/KES Analysis App]')

choice = st.selectbox('Login/Sign_Up', ['Login', 'Sign_Up'], label_visibility='collapsed')

if choice == 'Login':
    email = st.text_input('Enter Email Address', label_visibility='collapsed')
    password = st.text_input('Password', type='password', label_visibility='collapsed')

    if st.button('Login'):
        matching_user = [user for user in users if user[-2] == email]
        if len(matching_user) == 1 and check_password(matching_user[0][-1], password):
            st.success('Authentication Successful!')
        else:
            st.error('Email or Password is incorrect.', icon='❌')
else:
    email = st.text_input('Enter Email Address', label_visibility='collapsed')
    password = st.text_input('Password', type='password', label_visibility='collapsed')
    username = st.text_input('Enter your unique Username', label_visibility='collapsed')

    if st.button("Create My Account"):
        if len([u for u in users if u[-3] == username]) == 0:
            hashed_password = sha256(password)
            save_user(username, email, hashed_password)
            st.success('Account created successfully!')
            st.markdown('Please Login using your Email and Password')
        else:
            st.error('Username is already taken.', icon='❌')