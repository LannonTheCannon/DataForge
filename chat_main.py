import openai
from io import StringIO
from data import load_data
import time
import streamlit as st
from story_page import display_data_story

from pandasai import SmartDataframe
from pandasai.callbacks import BaseCallback
from pandasai.llm import OpenAI
from pandasai.responses.response_parser import ResponseParser

class StreamlitCallback(BaseCallback):
    def __init__(self, container) -> None:
        """Initialize callback handler."""
        self.container = container

    def on_code(self, response: str):
        self.container.code(response)


class StreamlitResponse(ResponseParser):
    def __init__(self, context) -> None:
        super().__init__(context)

    def format_dataframe(self, result):
        st.dataframe(result["value"])
        return

    def format_plot(self, result):
        st.image(result["value"])
        return

    def format_other(self, result):
        st.write(result["value"])
        return

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


def update_assistant_with_dataset(client, assistant_id, dataset_summary):
    try:
        client.beta.assistants.update(
            assistant_id=assistant_id,
            instructions=f"You are an AI assistant specializing in credit card fraud detection. "
                         f"Use the following dataset information to provide insights and answer questions:\n\n"
                         f"{dataset_summary}"
        )
        st.success("Assistant updated with dataset information.")
    except Exception as e:
        st.error(f"Error updating assistant: {str(e)}")


def get_assistant_response(client, assistant_id, thread_id, user_input):
    try:
        # Add the user's message to the thread
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )

        # Create a run
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

        # Retrieve the assistant's messages
        messages = client.beta.threads.messages.list(thread_id=thread_id)

        # Return the latest assistant message
        return messages.data[0].content[0].text.value
    except Exception as e:
        st.error(f"Error getting assistant response: {str(e)}")
        return "I'm sorry, but an error occurred while processing your request."


def display_ai_chat(df, client, assistant_id, thread_id):
    st.header("Chat with AI about the Dataset")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What would you like to know about the credit card fraud data?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = get_assistant_response(client, assistant_id, thread_id, prompt)
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

def display_pandas_chat():
    st.write("Chat with Credit Card Fraud Dataset")

    df = load_data("./data_pkl")

    with st.expander("Dataframe Preview"):
        st.write(df.tail(3))

    query = st.text_area("Chat with Dataframe")
    container = st.container()
    llm = OpenAI(api_token=st.secrets["OPENAI_API_KEY"])

    if query:
        query_engine = SmartDataframe(
            df,
            config={
                "llm": llm,
                "response_parser": StreamlitResponse,
                "callback": StreamlitCallback(container),
            },
        )

        answer = query_engine.chat(query)


def display_dashboard(df):
    st.header("Credit Card Fraud Dashboard")
    st.write("This is a placeholder for the dashboard. You can add visualizations here.")
    st.dataframe(df.head())


def display_data_explorer(df):
    st.header("Data Explorer")
    st.write("This is a placeholder for the data explorer. You can add more detailed data_pkl analysis here.")
    st.write(df.describe())


def sidebar():
    with st.sidebar:
        st.title("🤖 AI Credit Card Fraud Analysis")
        st.markdown("---")
        st.markdown("## Navigation")
        page = st.radio("Go to", ["Dashboard", "Story Telling", "Data Explorer", "AI Chat", "Pandas Chat"])
        st.markdown("---")
        st.markdown("## About")
        st.info(
            "This dashboard uses AI to analyze credit card fraud data. You can explore the data_pkl, chat with an AI assistant, and get insights on the dataset.")
    return page


def main():
    st.set_page_config(page_title="AI Credit Card Fraud Analysis Dashboard", layout="wide")

    client = openai.OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
    ASSISTANT_ID = 'asst_Gprcn49z0jmzvKpKaWeU7ZAw'
    THREAD_ID = "thread_0du078hnyl1z7AbIM7JyebsX"

    try:
        df = load_data("./data_pkl")
        if df.empty:
            st.error("The loaded dataset is empty. Please check your data_pkl source.")
            return
    except Exception as e:
        st.error(f"Error loading data_pkl: {str(e)}")
        return

    dataset_summary = prepare_dataset_summary(df)
    update_assistant_with_dataset(client, ASSISTANT_ID, dataset_summary)

    page = sidebar()

    if page == "Dashboard":
        display_dashboard(df)
    elif page == 'Story Telling':
        display_data_story()
    elif page == "Data Explorer":
        display_data_explorer(df)
    elif page == "AI Chat":
        display_ai_chat(df, client, ASSISTANT_ID, THREAD_ID)
    elif page == "Pandas Chat":
        display_pandas_chat()

if __name__ == "__main__":
    main()