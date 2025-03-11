import streamlit as st
import pandas as pd
import io

# Set page title and configuration
st.set_page_config(
    page_title="CSV Viewer and Filter",
    layout="wide"
)

# Initialize session state variables if they don't exist
if 'df' not in st.session_state:
    st.session_state.df = None
if 'filtered_df' not in st.session_state:
    st.session_state.filtered_df = None
if 'filter_applied' not in st.session_state:
    st.session_state.filter_applied = False

# Title and description
st.title("CSV Viewer and Filter")
st.write("Upload a CSV file to view it as a table and filter on specific columns.")

# File upload component
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Function to handle file upload
def process_upload(file):
    try:
        # Read CSV file into a pandas DataFrame
        df = pd.read_csv(file)
        return df
    except Exception as e:
        st.error(f"Error reading the CSV file: {e}")
        return None

# Process the uploaded file
if uploaded_file is not None:
    # Display loading message
    with st.spinner("Processing CSV file..."):
        # Process the file
        st.session_state.df = process_upload(uploaded_file)
        
        # If the file was processed successfully
        if st.session_state.df is not None:
            # Initialize filtered_df with the original df if not already filtered
            if not st.session_state.filter_applied:
                st.session_state.filtered_df = st.session_state.df.copy()
            
            st.success("File uploaded successfully!")
            
            # Display basic info about the DataFrame
            st.write(f"**Rows:** {st.session_state.df.shape[0]}, **Columns:** {st.session_state.df.shape[1]}")
            
            # Filter section
            st.subheader("Filter Data")
            
            # Create two columns for filter inputs
            col1, col2 = st.columns(2)
            
            with col1:
                # Dropdown to select column for filtering
                selected_column = st.selectbox(
                    "Select column to filter on",
                    options=st.session_state.df.columns
                )
            
            with col2:
                # Text input for filter value
                filter_value = st.text_input("Enter value to filter by (exact match)")
            
            # Filter action buttons
            filter_col, reset_col = st.columns(2)
            
            with filter_col:
                # Apply filter button
                if st.button("Apply Filter"):
                    if filter_value.strip() != "":
                        try:
                            # Try to convert the filter value to the column's data type
                            column_type = st.session_state.df[selected_column].dtype
                            
                            # Apply filter with equality matching
                            filtered_data = st.session_state.df[
                                st.session_state.df[selected_column].astype(str) == filter_value
                            ]
                            
                            if len(filtered_data) > 0:
                                st.session_state.filtered_df = filtered_data
                                st.session_state.filter_applied = True
                                st.success(f"Filter applied on column '{selected_column}' with value '{filter_value}'")
                            else:
                                st.warning(f"No rows match the filter value '{filter_value}' in column '{selected_column}'")
                        except Exception as e:
                            st.error(f"Error applying filter: {e}")
                    else:
                        st.warning("Please enter a filter value")
            
            with reset_col:
                # Reset filter button
                if st.button("Reset Filter"):
                    st.session_state.filtered_df = st.session_state.df.copy()
                    st.session_state.filter_applied = False
                    st.success("Filter reset. Showing all data.")
            
            # Display filter status
            if st.session_state.filter_applied:
                st.info(f"Showing filtered data: {len(st.session_state.filtered_df)} rows out of {len(st.session_state.df)} total rows")
            
            # Display the DataFrame (filtered or original)
            st.subheader("Data Preview")
            st.dataframe(st.session_state.filtered_df, use_container_width=True)
            
            # Download filtered data option
            if st.session_state.filtered_df is not None:
                csv = st.session_state.filtered_df.to_csv(index=False)
                st.download_button(
                    label="Download filtered data as CSV",
                    data=csv,
                    file_name="filtered_data.csv",
                    mime="text/csv",
                )
else:
    # Display instructions when no file is uploaded
    st.info("Please upload a CSV file to get started.")
    st.markdown("""
    ### How to use this app:
    1. Click on 'Browse files' to upload your CSV file
    2. View your data as a table
    3. Select a column and enter a value to filter on
    4. Click 'Apply Filter' to show only rows that match exactly
    5. Click 'Reset Filter' to show all data again
    """)