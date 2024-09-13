import streamlit as st
import openai
import os
import pandas as pd
import time
from io import StringIO
from data import load_data  # Import the load_data function you provided

# Set your OpenAI API key
openai.api_key = st.secrets.get("OPENAI_API_KEY")
if not openai.api_key:
    st.error('OpenAI API Key not found. Please set it in Streamlit secrets or as an environment variable.')
    st.stop()

# Set page configuration
st.set_page_config(page_title="Code Generator Assistant", page_icon="💻", layout="wide")


# Helper function to summarize dataset
def prepare_dataset_summary(df):
    buffer = StringIO()
    df.info(buf=buffer)
    info_string = buffer.getvalue()

    summary = f"""
    Dataset Summary:

    Number of rows: {len(df)}
    Number of columns: {len(df.columns)}

    Column descriptions:
    {info_string}

    Basic statistics:
    {df.describe().to_string()}

    Sample data (first 5 rows):
    {df.head().to_string()}
    """
    return summary


# Function to get assistant response (Python, DAX, SQL code generation)
def generate_code(client, assistant_id, thread_id, user_input):
    try:
        # Add the user's message to the thread
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=f"Generate Python, DAX, and SQL code for the following request:\n\n'{user_input}'"
        )

        # Create a run for the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )

        # Wait for the run to complete
        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run_status.status == 'completed':
                break
            time.sleep(1)

        # Retrieve the assistant's response
        messages = client.beta.threads.messages.list(thread_id=thread_id)

        # Return the latest assistant message containing the generated code
        return messages.data[0].content[0].text.value
    except Exception as e:
        st.error(f"Error generating code: {str(e)}")
        return None

# Function to display AI chat with code generation
def display_ai_chat(df, client, assistant_id, thread_id):
    st.header("Chat with AI about the Dataset")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What code would you like to generate based on the dataset?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = generate_code(client, assistant_id, thread_id, prompt)
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})


# Function to display the dashboard
def display_dashboard(df):
    st.header("Credit Card Fraud Dashboard")
    st.write("Sample Data Preview:")
    st.dataframe(df.head())


# Function to display a more detailed data explorer
def display_data_explorer(df):
    st.header("Data Explorer")
    st.write(df.describe())


# Sidebar for navigation
def sidebar():
    with st.sidebar:
        st.title("🤖 AI Code & Data Explorer")
        st.markdown("---")
        st.markdown("## Navigation")
        page = st.radio("Go to", ["Dashboard", "Data Explorer", "AI Chat"])
        st.markdown("---")
        st.markdown("## About")
        st.info(
            "This dashboard uses AI to analyze credit card fraud data and generate Python, DAX, and SQL code from conversational input."
        )
    return page


# Main function
def main():
    # Initialize OpenAI client
    client = openai.OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

    # Define your assistant and thread IDs
    ASSISTANT_ID = 'asst_Gprcn49z0jmzvKpKaWeU7ZAw'  # Replace with your actual assistant ID
    THREAD_ID = "thread_0du078hnyl1z7AbIM7JyebsX"  # Replace with your actual thread ID

    # Load dataset
    df = load_data("./data_pkl")
    if df.empty:
        st.error("The loaded dataset is empty or not found. Please check your data folder.")
        return

    # Sidebar navigation
    page = sidebar()

    # Display appropriate page
    if page == "Dashboard":
        display_dashboard(df)
    elif page == "Data Explorer":
        display_data_explorer(df)
    elif page == "AI Chat":
        display_ai_chat(df, client, ASSISTANT_ID, THREAD_ID)


if __name__ == "__main__":
    main()
