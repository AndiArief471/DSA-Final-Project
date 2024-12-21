import streamlit as st
import json

JSON_FILE = "ItemStorage.json"

def editAndDelete():
    itemName = st.session_state.editing_itemName
    itemQty = st.session_state.editing_itemQty
    userEmail = st.session_state.userEmail
    st.title("Edit or Delete an Item")
    if st.button("Go back"):
        # Pop the current page from the stack and rerun
        if len(st.session_state.page_stack) > 1:  # Ensure we don't pop the last page
            st.session_state.page_stack.pop()
            st.rerun()  # Trigger rerun to go back
    # Input field to specify the name of the item
    name = st.text_input("Item Name", value = itemName, disabled=True)
    # Input field for the new quantity
    new_quantity = st.number_input("Quantity", value=itemQty)
    col1, col2, col3 = st.columns([0.4, 0.5, 0.3], vertical_alignment="center")
    with col1:
        if st.button("Update Item"):
            edit_item(name, new_quantity, userEmail)    # Call the edit_item function
            go_to_previous_page()

    with col2:
        st.write("")
    with col3:
        if st.button("Delete Item"):
            delete_item(name, userEmail)  # Call the delete_item function
            go_to_previous_page()

# Edit an existing item in the inventory
def edit_item(name, newQty, email):
    inventory = load_inventory()  # Load the current inventory from JSON
    # Update the item's quantity if provided
    inventory["Item Storage"][email][name]["Quantity"] = newQty
    save_inventory(inventory)  # Save the updated inventory to JSON
    return name

# Remove an item from the inventory
def delete_item(name, email):
    inventory = load_inventory()  # Load the current inventory from JSON
    del inventory["Item Storage"][email][name]
    save_inventory(inventory)
    return name

# Load inventory data from the JSON file
def load_inventory():
    try:
        with open(JSON_FILE, "r") as file:
            return json.load(file)  # Load and return the inventory list
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist

# Save inventory data to the JSON file
def save_inventory(inventory):
    with open(JSON_FILE, "w") as file:
        json.dump(inventory, file, indent=4)  # Save the inventory to the file in JSON format

def go_to_previous_page():
    # Pop the current page from the stack and rerun
    if len(st.session_state.page_stack) > 1:  # Ensure we don't pop the last page
        st.session_state.page_stack.pop()
        st.rerun()  # Trigger rerun to go back