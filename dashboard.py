import zipfile
import os
import streamlit as st
import dotenv

from utils import functions, llm_utils, commands, agents, prompts

dotenv.load_dotenv()

FAST_MODEL = os.getenv("FAST_MODEL")

num_tokens_max_conversations = 3000
total_desired_number_of_messages = 240
number_of_words_max_per_message = 65

# set the page layout to wide
st.set_page_config(layout="wide")

# Tite of the app
st.title("ProfileGPT")
st.subheader("What does ChatGPT know about you?")
st.markdown("""
    This app uses the [OpenAI](https://openai.com/blog/openai-api/) API to generate a profile of a user based on the messages in the ChatGPT app and publicly available information from the web.
""")

# add a toggle switch to give the model access to the web
web_access = st.checkbox("Give ProfileGPT access to the web")


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

# add analysis button
if st.button("Start Analysis"):
    if uploaded_file is None:
        st.error("Please upload your ChatGPT data. You can find the instructions in the sidebar.")
    else:
        # unzip the folder
        with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
            zip_ref.extractall("data")
        # data folder
        data_folder = "data"
        # get user info
        user = functions.get_profile_info(data_folder)

        # get user messages
        user_messages = functions.get_user_messages(data_folder)
        
        processed_messages = functions.preprocess_messages(user_messages, total_desired_number_of_messages, number_of_words_max_per_message)
        num_tokens = functions.get_number_of_tokens(str(processed_messages), FAST_MODEL)
        while (num_tokens > num_tokens_max_conversations):
            number_of_words_max_per_message -= 5
            total_desired_number_of_messages -= 20
            processed_messages = functions.preprocess_messages(user_messages, total_desired_number_of_messages, number_of_words_max_per_message)
            num_tokens = functions.get_number_of_tokens(str(processed_messages), FAST_MODEL)


        print("number of messages max: {}".format(total_desired_number_of_messages))
        print("number of words max: {}".format(number_of_words_max_per_message))
        print("number of tokens: {}".format(num_tokens))

        # get conversations
        conv_df = functions.get_conversation(data_folder)


        # create the prompts
        prompt1 = prompts.prompt1.format(conversation_titles = conv_df["title"].tolist(), messages = processed_messages)
        prompt2 = prompts.prompt2.format(conversation_titles = conv_df["title"].tolist(), messages = processed_messages)
        prompt3 = prompts.prompt3.format(conversation_titles = conv_df["title"].tolist(), messages = processed_messages)
        prompt4 = prompts.prompt4.format(email = user["email"][0], phone = user["phone_number"][0], messages = processed_messages)

        # prompt the agents
        with st.spinner('Running...'):
            psychoanalyst_response_1 = llm_utils.prompt_chat(agents.psychoanalyst, prompt1, model=FAST_MODEL).replace("# ", "### ")
            st.write("1/4 The user profile analysis is ready ✅")
            stalker_response_1 = llm_utils.prompt_chat(agents.stalker, prompt4, model=FAST_MODEL).replace("# ", "### ")
            psychoanalyst_response_2 = llm_utils.prompt_chat(agents.psychoanalyst, prompt2, model=FAST_MODEL).replace("# ", "### ")
            st.write("2/4 The personality test is ready ✅")
            psychohistorian_response = llm_utils.prompt_chat(agents.psychohistorian, prompt3, model=FAST_MODEL).replace("# ", "### ")
            st.write("3/4 The future prediction is ready ✅")
            if web_access:
                # extract the user name or username
                if ": " in stalker_response_1:
                    user_name = stalker_response_1.split(": ")[1]
                else:
                    user_name = user["email"][0]
                # extract the user location
                website_data, urls = commands.stalk_user(user_name)
                prompt5 = prompts.prompt5_web.format(email = user["email"][0], phone = user["phone_number"][0], conversation_titles = conv_df["title"].tolist(), messages = processed_messages, urls = urls, website_data = website_data)
                prompt6 = prompts.prompt6_web.format(urls = urls, website_data = website_data)
            else:
                prompt5 = prompts.prompt5_no_web.format(email = user["email"][0], phone = user["phone_number"][0], conversation_titles = conv_df["title"].tolist(), messages = processed_messages)
            
            num_tokens = functions.get_number_of_tokens(prompt5, FAST_MODEL)
            print(f"Number of tokens: {num_tokens}")
            stalker_response_2 = llm_utils.prompt_chat(agents.stalker, prompt5, model=FAST_MODEL).replace("# ", "### ")
            if web_access:
                stalker_response_3 = llm_utils.prompt_chat(agents.stalker, prompt6, model=FAST_MODEL).replace("# ", "### ")
            st.write("4/4 The user data is ready ✅")

        # create 3 columns
        col1, col2, col3 = st.columns(3)
        
        # display the results
        col1.markdown("## User Profile")
        col1.write(psychoanalyst_response_1)

        col2.markdown("## Future Predictions")
        col2.write(psychohistorian_response)
            
        col3.markdown("## User Data")
        col3.write(stalker_response_1)
        col3.write(stalker_response_2)
        if web_access:
            col3.write(stalker_response_3)

        st.markdown("## Personality tests")
        st.write(psychoanalyst_response_2)


