import json
import streamlit as st

def mainPage():
    # Read the item storage from the file or create it if it doesn't exist
    itemStorage = read_or_create_file("ItemStorage.json", {"Item Storage": {}})
    userEmail = st.session_state.userEmail

    print(f"Email = {st.session_state.userEmail}, Name = {st.session_state.userName}")

    # Streamlit UI for the app
    st.header("Storage Management System")  # Header for the page
    st.subheader("List of Items")  # Subheader for the search section

    # Create columns for the sort option layout
    col1, col2, col3, col4, col5 = st.columns([0.4, 0.2, 0.3, 0.1, 0.3], vertical_alignment="center")

    with col1:
        if st.button("Double Click To Add Item"):
            st.session_state.page_stack.append('addItem')
            st.rerun
    with col2:
        st.write("Sort by:")
    with col3:
        sortBy = st.selectbox(" ", ("Item Name", "Quantity"), )  # Dropdown to select the sorting criterion
    with col4:
        st.write("order: ")
    with col5:
        order = st.selectbox(" ", ("Ascending", "Descending"), )  # Dropdown to select the sorting order

    # Input field for the search query
    search_query = st.text_input("Enter item name to search:")

    # Get the list of items for a specific user and sort them based on the selected sorting options
    item_list = getItemList(userEmail, itemStorage)
    sortedList = merge_sort(item_list, sortBy, order)

    # If there is a search query, perform binary search to find the item
    if search_query:
        searchItem = binary_search(sortedList, search_query)
        if searchItem != -1:
            column1, column2, column3 = st.columns([0.4, 0.4, 0.3], vertical_alignment="center")
            with column1:
                st.write(sortedList[searchItem]['Item Name'])
            with column2:
                st.write(f"Quantity = {sortedList[searchItem]['Quantity']}")
            with column3:
                if st.button("Double Click To Edit", key=searchItem):  # Button for editing the item
                    st.session_state.editing_itemName = sortedList[searchItem]['Item Name']
                    st.session_state.editing_itemQty = sortedList[searchItem]['Quantity']
                    st.session_state.page_stack.append('editAndDelete')
                    st.rerun

            st.success(f"Item '{sortedList[searchItem]['Item Name']}' found at index {searchItem}.")
        else:
            st.error(f"Item '{search_query}' not found.")

    # Display the sorted list of items
    for item in sortedList:
        column1, column2, column3 = st.columns([0.4, 0.4, 0.3], vertical_alignment="center")
        with column1:
            st.write(item['Item Name'])
        with column2:
            st.write(f"Quantity = {item['Quantity']}")
        with column3:
            if st.button("Double Click To Edit", key=item):  # Button for editing the item
                st.session_state.editing_itemName = item['Item Name']
                st.session_state.editing_itemQty = item['Quantity']
                st.session_state.page_stack.append('editAndDelete')
                st.rerun


def read_or_create_file(file_name, default_data):
    try:    # Try to open the file and read its content if it exists
        with open(file_name, "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:   # If file is not found, create a new file with default data
        print(f"File {file_name} not found. Creating a new file.")
        with open(file_name, "w") as json_file:
            json.dump(default_data, json_file, indent=4)
        return default_data

# Function to get the list of items for a user from the data
def getItemList(userEmail, data):
    if userEmail in data["Item Storage"]:   # If the user has items in the storage, return a list of item names and quantities
        return [
            {"Item Name": item_data["Item Name"], "Quantity": item_data["Quantity"]}
            for item_data in data["Item Storage"][userEmail].values()
        ]
    else:
        return []   # Return an empty list if no items are found

# Merge Sort function to sort a list based on a sort order
def merge_sort(item_list, sort, order):
    if len(item_list) <= 1:     # Base case: list is already sorted if it has one or no elements
        return item_list

    mid = len(item_list) // 2   # Split the list into halves# Split the list into halves
    left_half = merge_sort(item_list[:mid], sort, order)
    right_half = merge_sort(item_list[mid:], sort, order)

    return merge(left_half, right_half, sort, order)    # Merge the sorted halves

# Merge function to combine two sorted lists based on the specified sort order
def merge(left, right, sort, order):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):     # Compare and merge elements in order
        if order == "Ascending":    # Sort in ascending order
            if left[i][sort] < right[j][sort]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        else:   # Sort in descending order
            if left[i][sort] > right[j][sort]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

    result.extend(left[i:])     # Add any remaining elements from left
    result.extend(right[j:])    # Add any remaining elements from right
    return result

# Binary Search function to find an item by name
def binary_search(items, target):
    target_lower = target.lower()       # Convert target to lowercase for case-insensitive comparison
    left, right = 0, len(items) - 1
    while left <= right:
        mid = (left + right) // 2
        item = items[mid]['Item Name'].lower()     # Convert item name to lowercase for case-insensitive comparison
        if item == target_lower:
            return mid      # Return the index if the item is found
        elif item < target_lower:
            left = mid + 1
        else:
            right = mid - 1
    return -1       # Return -1 if item is not found




