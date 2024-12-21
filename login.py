import streamlit as st  # Importing the Streamlit library for creating web applications
import json  # Importing the JSON library for handling JSON data
import os  # Importing the OS library for interacting with the operating system
import signUp, mainPage, addPage, editAndDeletePage    #import other script

def loginPage():
    st.title("Login Page")  # Set the title of the page
    st.markdown("<h1 style='text-align: center; color: gray;'>Welcome to Login Page</h1>",
                unsafe_allow_html=True)  # Display a welcome message
    # Login form
    email = st.text_input("Email")  # Input field for the user's email
    password = st.text_input("Password", type='password')  # Input field for the user's password, masked

    col1, col2, col3 = st.columns([0.4, 1, 0.3], vertical_alignment="center")
    with col1:
        submit_button1 = st.button("Login")  # Button for submitting the login form
    with col2:
        st.write("")
    with col3:
        submit_button2 = st.button("Sign Up")  # Button for navigating to the sign-up page

    data = load_inventory()

    if submit_button1:  # Check if the "Login" button is clicked
        if check_credentials(email, password):  # Check the provided credentials
            name_value = data["Credentials"][email]["Name"]
            st.success("Login Success!")
            st.session_state.userEmail = email
            st.session_state.userName = name_value
            st.session_state.page_stack.append('main')
            st.rerun()
            # Show a success message if login is successful
        else:
            st.error("Email or Password Not Match")  # Show an error message if login fails

    if submit_button2:  # Check if the "Sign Up" button is clicked
        st.session_state.page_stack.append('signUp')
        st.rerun()

# Function to hash the password
def hash_password(password, salt="kajhsdqqi"):
    # Combine the password and salt
    combined = password + salt

    # Initialize a "hash" value
    hash_value = 10

    # Process each character in the combined string
    for i, char in enumerate(combined):
        # Shift the ASCII value of the characters
        shifted = ord(char) << (i % 8)

        # XOR with the current hash value
        hash_value ^= shifted

        # Add some non-linear mixing
        hash_value = (hash_value * 67 + 7) % (2**56)

    # Convert the final hash value to a hexadecimal string
    return hex(hash_value)[2:]

# Function to check credentials
def check_credentials(email, password):
    # Check if the users.json file exists
    if os.path.exists('Users.json'):
        with open('Users.json', 'r') as f:  # Open the users.json file for reading
            users = json.load(f)  # Load the JSON data from the file
        # Check if the email exists in the credentials
        if email in users["Credentials"]:
            hashed_password = hash_password(password)  # Hash the provided password
            stored_hashed_password = users["Credentials"][email]["Password"]  # Get the stored hashed password
            print(stored_hashed_password)  # Print the stored hashed password for debugging
            print(hashed_password)  # Print the hashed password for debugging
            return hashed_password == stored_hashed_password  # Compare the hashed passwords
        else:
            return False
    else:
        st.error("File Users.json Not Found.")  # Show an error if the file is not found
        with open("Users.json", "w") as json_file:
            userData = {"Credentials": {}}
            json.dump(userData, json_file, indent=4)
        check_credentials(email, password)

def load_inventory():
    try:
        with open("Users.json", "r") as file:
            return json.load(file)  # Load and return the inventory list
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist

if 'page_stack' not in st.session_state:
    st.session_state.page_stack = ['login']

current_page = st.session_state.page_stack[-1]

#   List of all pages main function
match current_page:
    case 'login':
        loginPage()
    case 'signUp':
        signUp.signUpPage()
    case 'main':
        mainPage.mainPage()
    case 'addItem':
        addPage.addItem()
    case 'editAndDelete':
        editAndDeletePage.editAndDelete()

print(st.session_state.page_stack)

# User interface


