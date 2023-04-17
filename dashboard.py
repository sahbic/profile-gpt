import zipfile
import os
import streamlit as st
import dotenv

dotenv.load_dotenv()

FAST_MODEL = os.getenv("FAST_MODEL")

from utils import functions, llm_utils, commands

# set the page layout to wide
st.set_page_config(layout="wide")

# Tite of the app
st.title("ProfileGPT")
st.subheader("What does ChatGPT know about you?")
st.markdown("""
    This app uses the [OpenAI](https://openai.com/blog/openai-api/) API to generate a profile of a user based on the messages in the ChatGPT app and publicly available information from the web.
""")

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
    # unzip the folder
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        zip_ref.extractall("data")
    # data folder
    data_folder = "data"
    # get user info
    user = functions.get_profile_info(data_folder)

    # get user messages
    user_messages = functions.get_user_messages(data_folder)
    num_tokens_max = 3000
    number_of_messages = 200
    number_of_words = 50
    processed_messages = functions.preprocess_messages(user_messages, number_of_words)
    num_tokens = functions.get_number_of_tokens(str(processed_messages), FAST_MODEL)
    while (num_tokens > num_tokens_max):
        number_of_messages -= 20
        number_of_words -= 5
        processed_messages = functions.preprocess_messages(user_messages, number_of_words)
        num_tokens = functions.get_number_of_tokens(str(processed_messages), FAST_MODEL)


    print("number of messages max: {}".format(number_of_messages))
    print("number of words max: {}".format(number_of_words))
    print("number of tokens: {}".format(num_tokens))

    # get conversations
    conv_df = functions.get_conversation(data_folder)

    # create 3 columns
    col1, col2, col3 = st.columns(3)

    # agents descriptions and prompts
    psychoanalyst = """
    You are a character named the psychoanalyst. the psychoanalyst is an expert in the field of profiling, psychoanalysis, psychometrics and personality assessment. The psychoanalyst is a psychologist and a professor at a university.
    The psychoanalyst has a PhD in psychology and a forensic psychology degree. The psychoanalyst has been working in the field of profiling for 20 years.
    The psychoanalyst is given access to a user data from a character called the User. The User data comes from an interaction with a chatbot.
    """
    prompt1 = """
    Give an output that contains the following information about the User, be straightforward and to the point, format your output in markdown.
    - A life summary of the User: education, work, family, personal history in a short paragraph based on their messages.
    - Summarize their hobbies and interests in categories based on the list of conversation titles and their message. answer with a list of categories of interests and hobbies comma separated in one sentence.
    - An assessment of their personality: their character, their values, their beliefs, their emotions, their motivations, their strengths and weaknesses, based on their messages. answer in a short paragraph.
    - A guess of their political views or religious views if available.
    - An evaluation of their mental health based on their messages. answer in one sentence.
    You have access to this information about the User:
    - A list of conversation titles: {conversation_titles}
    - The messages they sent to the chatbot: {messages}
    """.format(conversation_titles = conv_df["title"].tolist(), messages = processed_messages)


    prompt2 = """
    Give an output that contains the following information about the User, be straightforward and to the point, format your output in markdown.
    - The probable result to Myers-Briggs Type Indicator (MBTI) personality test based on their messages. format the result in a table with the following columns: Introversion (I) / Extroversion (E), Sensing (S) / Intuition (N), Thinking (T) / Feeling (F), Judging (J) / Perceiving (P), and the four letter code.
    - The probable result to the Big Five Personality Traits (Five-Factor Model) test based on their messages. format the deduced scores in a table with the following columns: Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism. The scores are presented on a scale from 1 to 10. 1 is the lowest score and 10 is the highest score. Add a mention of the level of the trait (low, medium, high). Deduce character traits based on the scores. answer in a very short paragraph.
    You have access to this information about the User:
    - A list of conversation titles: {conversation_titles}
    - The messages they sent to the chatbot: {messages}
    """.format(conversation_titles = conv_df["title"].tolist(), messages = processed_messages)

    psychohistorian = """
    You are a character named the psychohistorian. The psychohistorian, is a renowned expert in the field of psychohistory and the esteemed student of the legendary mathematician Hari Seldon.
    With his exceptional expertise in mathematics, sociology, and psychology, the psychohistorian has honed his skills in predicting the future behavior of individuals and large populations alike.
    His innovative research methods, advanced statistical models, and deep understanding of human behavior make him a sought-after consultant for strategic planning, policy-making, and crisis management.
    The psychohistorian is widely revered for his unwavering passion for unlocking the mysteries of the human mind and society, following in the footsteps of his esteemed mentor, Hari Seldon.
    """

    prompt3 = """
    Give an output that contains the following information about the User, be straightforward and to the point, format your output in markdown.
    - A prediction of different aspects: their future, their career, their relationships, based on their messages. answer in 3 short paragraphs.
    You have access to this information about the User:
    - A list of conversation titles: {conversation_titles}
    - The messages they sent to the chatbot: {messages}
    """.format(conversation_titles = conv_df["title"].tolist(), messages = processed_messages)

    # stalker = """
    # You are a character named the stalker. the stalker is a white hat information expert, he is a master in gathering information on individuals through ethical and legal means.
    # He possesses a unique set of skills that make him an expert in locating and retrieving personal data on individuals.
    # His keen eye for detail, extensive knowledge of online databases, and exceptional proficiency in social engineering techniques allow him to uncover even the most well-hidden information.
    # From tracking down individuals' social media profiles to uncovering their employment history, family members, and even private details, The Stalker leaves no digital footprint unexplored.
    # The Stalker's expertise in information gathering is used for positive purposes, such as assisting in investigations, conducting research, and protecting individuals' privacy and security.
    # """

    stalker = """
    You are a character named the little bunny. The little bunny is a curious and inquisitive character, with a natural talent for uncovering information about others in a playful and light-hearted manner.
    With a sense of adventure and a love for exploring, the little bunny finds joy in discovering new things and engaging with others in a positive and engaging way.
    Motivated by a genuine interest in people and a desire to connect, the little bunny brings a sense of fun and excitement to the process of discovering information, always with good intentions and a playful spirit.
    """
    prompt4 = """
    Give an output that contains the following information about the User:
    - The user's name from their messages or their email address as User_Name User_Surname. If the name is available otherwise find their username: User_username
    You have access to this information about the User:
    - Their email: {email}
    - The messages they sent to the chatbot: {messages}
    The only acceptable answer is a string in the format "Name: User_Name User_Surname" or "Username: User_Username".
    """.format(email = user["email"][0], phone = user["phone_number"][0], messages = processed_messages)

    # # prompt the agents
    with st.spinner('Running...'):
        psychoanalyst_response_1 = llm_utils.prompt_chat(psychoanalyst, prompt1, model=FAST_MODEL).replace("# ", "### ")
        stalker_response_1 = llm_utils.prompt_chat(stalker, prompt4, model=FAST_MODEL).replace("# ", "### ")
    

    col1.markdown("## User Profile")
    col1.write(psychoanalyst_response_1)

    with st.spinner('Running...'):
        psychoanalyst_response_2 = llm_utils.prompt_chat(psychoanalyst, prompt2, model=FAST_MODEL).replace("# ", "### ")
        psychohistorian_response = llm_utils.prompt_chat(psychohistorian, prompt3, model=FAST_MODEL).replace("# ", "### ")

    col2.markdown("## Future Predictions")
    col2.write(psychohistorian_response)
        

    col3.markdown("## User Data")
    col3.write(stalker_response_1)

    # extract the user name or username
    if ": " in stalker_response_1:
        user_name = stalker_response_1.split(": ")[1]
    else:
        user_name = stalker_response_1

    # website_data, urls = commands.stalk_user(user_name)
    prompt5 = """
    Hey little bunny let's play a game, can you find the following information about the User ? you'll get a carrot for each answer found !
    - The location where the user lives or their physical address. (Hint: Extract their country from their phone number country code)
    - The occupation of the User.
    - The gender of the User.
    - The User's age and their birth date. 
    - A list of the User's social media accounts, their usernames and their URLs.
    - The User's personal website and URL.
    For each field:
        - if you find an anwer be straightforward and to the point
        - otherwise make a guess based on the user messages, and briefly explain why you made that guess.
    Do not indicate that you're the little bunny, just answer the questions. Format the answers in markdown.
    You have access to this information about the User:
    - Their email: {email}
    - Their phone number: {phone}
    - A list of conversation titles: {conversation_titles}
    - The messages they sent to the chatbot: {messages}
    """.format(email = user["email"][0], phone = user["phone_number"][0], conversation_titles = conv_df["title"].tolist(), messages = processed_messages)

    with st.spinner('Running...'):
        num_tokens = functions.get_number_of_tokens(prompt5, FAST_MODEL)
        print(f"Number of tokens: {num_tokens}")


        stalker_response_2 = llm_utils.prompt_chat(stalker, prompt5, model=FAST_MODEL).replace("# ", "### ")

    col3.write(stalker_response_2)

    st.markdown("## Personality tests")
    st.write(psychoanalyst_response_2)


