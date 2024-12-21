import streamlit as st  # Importing the Streamlit library for creating web applications
import json  # Importing the JSON library for handling JSON data
import os  # Importing the OS library for interacting with the operating system

def signUpPage():
    # User registration form
    st.markdown("<h2 style='text-align: center;'>Sign Up New Member</h2>",
                unsafe_allow_html=True)  # Display a header for the sign-up form

    email = st.text_input("New Email")  # Input field for the new user's email
    name = st.text_input("New Name")  # Input field for the new user's name
    password = st.text_input("New Password", type='password')  # Input field for the new user's password, masked

    if st.button("Sign Up"):  # Check if the "Sign Up" button is clicked
        add_user(email, name, password)  # Call the function to add the new user
        # Switch to the login page after successful sign-up
        if len(st.session_state.page_stack) > 1:  # Ensure we don't pop the last page
            st.session_state.page_stack.pop()
            st.rerun()  # Trigger rerun to go back


    if st.button("Go Back"):
        # Pop the current page from the stack and rerun
        if len(st.session_state.page_stack) > 1:  # Ensure we don't pop the last page
            st.session_state.page_stack.pop()
            st.rerun()  # Trigger rerun to go back

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
def check_credentials(email, name, password):
    # Check if the users.json file exists
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:  # Open the users.json file for reading
            users = json.load(f)  # Load the JSON data from the file
        hashed_password = hash_password(password)  # Hash the provided password
        # Check if the hashed password matches the stored hashed password
        return users["Credentials"][email][name][password] == hashed_password
    return False  # Return False if the file does not exist

# Function to add a new user
def add_user(email, name, password):
    hashed_password = hash_password(password)  # Hash the provided password
    # Check if the users.json file exists
    if os.path.exists('users.json'):
        with open('users.json', 'r+') as f:  # Open the users.json file for reading and writing
            users = json.load(f)  # Load the JSON data from the file
            # Check if the email is already registered
            if email in users["Credentials"]:
                st.error("Email is registered!")  # Show an error message if the email is already registered
            else:
                # Add the new user's credentials
                users["Credentials"][email] = {
                    "Name": name,
                    "Password": hashed_password
                }

                f.seek(0)  # Move the file pointer to the beginning of the file
                json.dump(users, f, indent=4)  # Write the updated JSON data back to the file
                f.truncate()  # Truncate the file to remove any leftover data
                st.success("Email Added Successfully!")  # Show a success message
                add_item_storage(email)  # Call the function to add item storage for the new user
    else:
        # If the users.json file does not exist, create it
        with open('users.json', 'w') as f:
            users = {"Credentials": {
                email: {
                    "Name": name,
                    "Password": hashed_password
                }}}
            json.dump(users, f)  # Write the new user data to the file
            st.success("Email Added Successfully!")  # Show a success message
            add_item_storage(email)  # Call the function to add item storage for the new user

# Function to add item storage
def add_item_storage(email):
    # Check if the itemStorage.json file exists
    if os.path.exists('itemStorage.json'):
        with open('itemStorage.json', 'r+') as f:  # Open the itemStorage.json file for reading and writing
            items = json.load(f)  # Load the JSON data from the file
            items["Item Storage"][email] = {}  # Initialize an empty storage for the new user
            f.seek(0)  # Move the file pointer to the beginning of the file
            json.dump(items, f, indent=4)  # Write the updated JSON data back to the file
            f.truncate()  # Truncate the file to remove any leftover data
            st.success("Storage Updated")  # Show a success message
    else:
        # If the itemStorage.json file does not exist, create it
        with open('itemStorage.json', 'w') as f:
            items = {"Item Storage": {
                email: {
                }}}
            json.dump(items, f)  # Write the new item storage data to the file
            st.success("Storage Created")  # Show a success message

