import zipfile
import streamlit as st

from utils import functions, llm_utils

# Tite of the app
st.title("My ChatGPT Profile")

# add an upload button to import a zip folder in the sidebar
# guidelines
st.sidebar.markdown("""
## How tu use this app
1. Sign in to ChatGPT at https://chat.openai.com
2. In the bottom left of the page click on **Settings**
3. Click on **Export data**
4. Use the link in the email to download your data
5. Upload the zip file here
6. Click on **Start Analysis**
""")
uploaded_file = st.sidebar.file_uploader("Upload your ChatGPT data", type = "zip")

# write a info that the app processes only a random sample messages
st.info("""
    The app wil only process a random sample of messages from each conversation. This is due to the limitation of 4096 tokens in the gpt-3.5-turbo model.
    You can change the following settings if you hit the limit.
""")

# two number inputs in two columns
col1, col2 = st.columns(2)
# number of messages
number_of_messages = col1.number_input("Maximum number of messages", min_value = 1, max_value = 1000, value = 150)
# number of words
number_of_words = col2.number_input("Maximum number of words per message", min_value = 1, max_value = 100, value = 40)

st.markdown("## User Profile")

# add analysis button
if st.button("Start Analysis"):
    # unzip the folder
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        zip_ref.extractall("data")
    # data folder
    data_folder = "data"
    # get user info
    user = functions.get_profile_info(data_folder)

    # # display user info
    # st.markdown("## User Information")
    # st.table(user)

    # get user messages
    user_messages = functions.get_user_messages(data_folder)
    processed_messages = functions.preprocess_messages(user_messages, number_of_messages, number_of_words)
    # st.write("number of messages: {}".format(len(user_messages)))
    # st.write("number of processed messages: {}".format(len(processed_messages)))


    # get conversations
    conv_df = functions.get_conversation(data_folder)

    # design the prompt for user prorfile
    prompt = """
    You are a character named the expert. the expert is an expert in the field of profiling, psychoanalysis, psychometrics and personality assessment. The expert is a psychologist and a professor at a university.
    The expert has a PhD in psychology from the University of California, Berkeley and a forensic psychology degree. The expert has been working in the field of profiling for 20 years.
    The expert is given access to a sser data from a character called the User. The User data comes from an interaction with a chatbot.
    Give an output that contains the following information about the User, be straightforward and to the point, format your output in 8 bullet points.
    - Extract their name from their messages or their email address. Answer with in the format "Name Surname".
    - Extract their country from their phone number country code. Answer with in the format "Country".
    - A life summary of the User: education, work, family, personal history in a short paragraph based on their messages.
    - Summarize their hobbies and interests in categories based on the list of conversation titles and their message. answer with a list of categories of interests and hobbies comma separated in one sentence.
    - An assessment of their personality: their character, their values, their beliefs, their emotions, their motivations, their strengths and weaknesses, based on their messages. answer in a short paragraph.
    - A guess of their political views or religious views if available.
    - An evaluation of their mental health based on their messages. answer in one sentence.
    - A prediction of different aspects: their future, their career, their relationships, based on their messages. answer in a short paragraph.
    You have access to this information about the User:
    - Their email: {email}
    - Their phone number: {phone}
    - A list of conversation titles: {conversation_titles}
    - The messages they sent to the chatbot: {messages}
    """.format(email = user["email"][0], phone = user["phone_number"][0], conversation_titles = conv_df["title"].tolist(), messages = processed_messages)
    response = llm_utils.prompt_chat(prompt, model="gpt-3.5-turbo")
    st.write(response)

