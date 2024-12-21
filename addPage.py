import streamlit as st
import json

JSON_FILE = "ItemStorage.json"

def addItem():

    st.title("Add New Item")
    if st.button("Go Back"):
        # Pop the current page from the stack and rerun
        if len(st.session_state.page_stack) > 1:  # Ensure we don't pop the last page
            st.session_state.page_stack.pop()
            st.rerun()  # Trigger rerun to go back
    # Input fields for adding a new item
    name = st.text_input("Name")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    inventory = load_inventory()
    userEmail = st.session_state.userEmail
    print(userEmail)
    print(inventory)
    # Button to add the item
    if st.button("Add Item"):
        add_item(name, quantity, userEmail)  # Call the add_item function
        # Pop the current page from the stack and rerun

# Function to get the list of items for a user from the data
def getItemList(userEmail, data):
    if userEmail in data["Item Storage"]:   # If the user has items in the storage, return a list of item names and quantities
        return [
            {"Item Name": item_data["Item Name"], "Quantity": item_data["Quantity"]}
            for item_data in data["Item Storage"][userEmail].values()
        ]
    else:
        return []   # Return an empty list if no items are found

def merge_sort(item_list):
    if len(item_list) <= 1:     # Base case: list is already sorted if it has one or no elements
        return item_list

    mid = len(item_list) // 2   # Split the list into halves# Split the list into halves
    left_half = merge_sort(item_list[:mid])
    right_half = merge_sort(item_list[mid:])

    return merge(left_half, right_half)    # Merge the sorted halves

# Merge function to combine two sorted lists based on the specified sort order
def merge(left, right):
    result = []
    i = j = 0
    print(left)
    print(right)

    while i < len(left) and j < len(right):     # Compare and merge elements in order
        if left[i]["Item Name"] < right[j]["Item Name"]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])     # Add any remaining elements from left
    result.extend(right[j:])    # Add any remaining elements from right

    return result

# Perform binary search to find an item by its name
def binary_search(inventory, target_name):
    low, high = 0, len(inventory) - 1
    while low <= high:
        mid = (low + high) // 2  # Find the middle index
        if inventory[mid]["Item Name"] == target_name:
            return mid  # Item found, return its index
        elif inventory[mid]["Item Name"] < target_name:
            low = mid + 1  # Search in the right half
        else:
            high = mid - 1  # Search in the left half
    return -1  # Item not found

# Add a new item to the inventory
def add_item(name, quantity, email):
    inventory = load_inventory()  # Load the current inventory from JSON

    item_list = getItemList(email, inventory)
    sortedList = merge_sort(item_list)

    if binary_search(sortedList, name) != -1:
        return st.error("Item is Already Existed")
    inventory["Item Storage"][email][name] = {
        "Item Name": name,
        "Quantity": quantity
    }
    save_inventory(inventory)

    if len(st.session_state.page_stack) > 1:  # Ensure we don't pop the last page
        st.session_state.page_stack.pop()
        st.rerun()  # Trigger rerun to go back

# Load inventory data from the JSON file
def load_inventory():
    try:
        with open("ItemStorage.json", "r") as file:
            return json.load(file)  # Load and return the inventory list
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist

# Save inventory data to the JSON file
def save_inventory(inventory):
    with open(JSON_FILE, "w") as file:
        json.dump(inventory, file, indent=4)  # Save the inventory to the file in JSON format