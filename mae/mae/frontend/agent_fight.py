import json

import streamlit as st
import requests

headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}
# Set the title and page configuration for the Streamlit app
st.set_page_config(page_title="Agent Fight", page_icon="🤖", layout="centered")
st.title("🤖 Agent Fight")

# Add a description and a separator
st.write("""
    Welcome to Agent Fight! Use this tool to send your agents' data to the backend API for a battle simulation.
    Please fill out the input fields below and click the submit button to initiate the fight.
""")
st.markdown("---")

# Arrange the input fields using columns
col1, col2 = st.columns(2)

with col1:
    primary_agent = st.text_input("Primary Agent", placeholder="Enter primary agent data")

with col2:
    secondary_agent = st.text_input("Secondary Agent", placeholder="Enter secondary agent data")

fight_task = st.text_input("Fight Task", placeholder="Describe the fight task")

# Add a submit button below the separator
st.markdown("---")
submit_button = st.button("⚔️ Start Fight")

# Define the FastAPI endpoint URL
url = "http://127.0.0.1:8010/agent_evaluation"  # Replace with your actual FastAPI server address and endpoint

# Execute the following actions when the user clicks the submit button
if submit_button:
    if primary_agent and secondary_agent and fight_task:
        # Show a loading spinner while the request is being processed
        with st.spinner("Initiating fight, please wait..."):
            # Combine the input data into request parameters
            params = {
                "primary_data": primary_agent,
                "second_data": secondary_agent,
                "comparison_data_task": fight_task
            }

            try:
                response = requests.post(url, data=json.dumps(params),headers=headers)
                # Check if the request was successful
                if response.status_code == 200:
                    # Display the returned results
                    st.markdown(response.json().get('data'))
                    # st.success("🥳 Fight initiated successfully! Here are the battle results:")
                    # st.json(response.json())
                else:
                    # If the request failed, display an error message
                    st.error(f"❌ Fight failed, status code: {response.status_code}")
                    st.markdown(response.json().get('data'))
            except Exception as e:
                # If an exception occurred, display the error message
                st.error(f"An error occurred during the fight: {e}")
    else:
        st.warning("Please fill in all input fields before starting the fight.")

# Add a footer
st.markdown("---")
st.write("© 2024 Agent Fight")
