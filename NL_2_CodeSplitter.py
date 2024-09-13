import streamlit as st
import openai
import os

# Set your OpenAI API key
openai.api_key = st.secrets.get("OPENAI_API_KEY")
if not openai.api_key:
    st.error('OpenAI API Key not found. Please set it in Streamlit secrets or as an environment variable.')
    st.stop()

# Set page configuration
st.set_page_config(page_title="Code Generator Assistant", page_icon="💻", layout="wide")

# CSS to style the app
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stTextInput > label {
        font-size: 18px;
        font-weight: 600;
    }
    .code-section {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("💻 Code Generator Assistant")
st.write("Turn your conversational requests into Python, DAX, and SQL code.")

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

def generate_code(user_input):
    prompt = f"""
You are an expert programmer proficient in Python (for data analysis using pandas), DAX (for PowerBI), and SQL (for PostgreSQL). 

Please generate code in all three languages that accomplishes the following request:

'{user_input}'

For each language, provide the code in separate sections titled 'Python Code', 'DAX Code', and 'SQL Code'.

Ensure that the code is well-commented, easy to understand, and formatted properly.

If any assumptions are needed, please state them in comments within the code.
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Use 'gpt-3.5-turbo' if 'gpt-4' is not available
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates code based on user requests."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,  # Set temperature to 0 for deterministic output
        )

        code_response = response['choices'][0]['message']['content']
        return code_response.strip()
    except Exception as e:
        st.error(f"Error generating code: {str(e)}")
        return None

# User input
user_input = st.text_input("Enter your request:", "")

if st.button("Generate Code") and user_input:
    with st.spinner("Generating code..."):
        code_output = generate_code(user_input)
        if code_output:
            st.session_state.history.append((user_input, code_output))
            # Display the generated code
            st.markdown("## Generated Code")
            # Split the code into sections based on the headings
            sections = code_output.split('\n')
            current_section = None
            code_text = ""
            for line in sections:
                if "Python Code" in line:
                    if code_text:
                        st.code(code_text.strip(), language=current_section.lower())
                    current_section = "Python"
                    st.markdown(f"### {current_section} Code")
                    code_text = ""
                elif "DAX Code" in line:
                    if code_text:
                        st.code(code_text.strip(), language=current_section.lower())
                    current_section = "DAX"
                    st.markdown(f"### {current_section} Code")
                    code_text = ""
                elif "SQL Code" in line:
                    if code_text:
                        st.code(code_text.strip(), language=current_section.lower())
                    current_section = "SQL"
                    st.markdown(f"### {current_section} Code")
                    code_text = ""
                else:
                    code_text += line + '\n'
            if code_text:
                st.code(code_text.strip(), language=current_section.lower())

# Display history
if st.session_state.history:
    st.markdown("---")
    st.markdown("## Conversation History")
    for i, (inp, outp) in enumerate(reversed(st.session_state.history)):
        with st.expander(f"Request {len(st.session_state.history) - i}: {inp}"):
            st.markdown(outp)
