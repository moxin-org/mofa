
import json
import streamlit as st
import requests
import yaml

headers = {
    "accept": "application/json",
    "Content-Type": "application/json"
}

# Set the title and page configuration for the Streamlit app
st.set_page_config(page_title="Agent Fight", page_icon="🤖", layout="wide")
st.title("🤖 Agent Fight")

# Add a description and a separator
st.write("""
    Welcome to Agent Fight! Use this tool to send your agents' data to the backend API for a battle simulation.
""")
st.markdown("---")

# Set the path to the YAML file
yaml_file_path = "//agent-hub/content-evaluation/content_evaluation/content_evaluation_agent.yml"

# Load the YAML file
with open(yaml_file_path, "r") as file:
    yaml_data = yaml.safe_load(file)

# Extract the agents from the YAML data
agents = yaml_data.get("AGENT", {})

# Create a form for editing each key-value pair in the agents
st.subheader("Edit Agents Prompt")

# Dictionary to hold edited values
edited_agents = {}

# Display each key-value pair in a text input for editing
for key, value in agents.items():
    edited_agents[key] = st.text_input(key, value=value)

# Display a submit button below the input fields
if st.button("Save Changes"):
    # Update the YAML data with the edited agents
    yaml_data["AGENT"] = edited_agents

    # Save the updated YAML file
    with open(yaml_file_path, "w") as file:
        yaml.dump(yaml_data, file, default_flow_style=False)

    st.success("Changes saved successfully!")

st.markdown("---")

# Arrange the input fields for fight details
col1, col2 = st.columns(2)

with col1:
    primary_agent = st.text_input("Primary Agent", placeholder="Enter primary agent data")

with col2:
    secondary_agent = st.text_input("Secondary Agent", placeholder="Enter secondary agent data")

fight_task = st.text_input("Fight Task", placeholder="Describe the fight task")

st.markdown("---")

submit_button = st.button("⚔️ Start Fight")

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
                "comparison_data_task": fight_task,
                "yaml_data": yaml.dump(edited_agents, default_flow_style=False)  # Include the edited agents data in the request
            }

            try:
                response = requests.post(url, data=json.dumps(params), headers=headers)
                # Check if the request was successful
                if response.status_code == 200:
                    st.markdown(response.json().get('data'))
                else:
                    st.error(f"❌ Fight failed, status code: {response.status_code}")
                    st.markdown(response.json().get('data'))
            except Exception as e:
                st.error(f"An error occurred during the fight: {e}")
    else:
        st.warning("Please fill in all input fields before starting the fight.")

# Add a footer
st.markdown("---")
st.write("© 2024 Agent Fight")