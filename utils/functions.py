import os
import json
import datetime
import random
import tiktoken
import pandas as pd

def get_ordered_random_sample(mylist, sample_size):
    if sample_size <= 0:
        sample_size = 1
    if sample_size > len(mylist):
        sample_size = len(mylist)
    sorted_sample = [
        mylist[i] for i in sorted(random.sample(range(len(mylist)), sample_size))
    ]
    return sorted_sample

def get_profile_info(data_folder):
    # get user file
    user_file = os.path.join(data_folder, "user.json")
    # read user file
    user = json.load(open(user_file))
    user_df = pd.DataFrame.from_records([user])
    user_df = user_df.drop(columns = ["chatgpt_plus_user", "id"])
    conv_df = get_conversation(data_folder)
    user_df["number_of_conversations"] = len(conv_df)
    return user_df

def get_conversation(data_folder):
    # get conversation file
    conversation_file = os.path.join(data_folder, "conversations.json")
    # read conversation file
    conversation = json.load(open(conversation_file))
    conv_df = pd.DataFrame.from_records(conversation)
    conv_df = conv_df.drop(columns = ["mapping", "moderation_results", "current_node", "plugin_ids", "id"])
    # convert from standard timestamp to datetime
    conv_df["create_time"] = conv_df["create_time"].apply(lambda x: datetime.datetime.fromtimestamp(x))
    conv_df["update_time"] = conv_df["update_time"].apply(lambda x: datetime.datetime.fromtimestamp(x))
    return conv_df

def get_user_messages(data_folder):
    # get conversation file
    conversation_file = os.path.join(data_folder, "conversations.json")
    # read conversation file
    conversations = json.load(open(conversation_file))
    user_messages = []
    for conversation in conversations:
        conv_messages = []
        mappings = conversation["mapping"]
        for mapping in mappings:
            if "message" in mappings[mapping]:
                if mappings[mapping]["message"]:
                    if mappings[mapping]["message"]["author"]["role"] == "user":
                        if "content" in mappings[mapping]["message"]:
                            conv_messages.append(mappings[mapping]["message"]["content"]["parts"][0])
        user_messages.append(conv_messages)
    return(user_messages)

def preprocess_messages(user_messages, total_desired_number_of_messages = 150, number_of_words_max_per_message = 40):
    # select a random sample of messages from each list of messages in user_messages
    # the goal is to have a random sample of 180 messages with the same proportion of messages from each conversation
    sampled_messages = []
    total_number_of_messages = 0
    for conversation in range(len(user_messages)):
        total_number_of_messages += len(user_messages[conversation])
    for conversation in range(len(user_messages)):
        conversation_messages = user_messages[conversation]
        # remove empty messages
        conversation_messages = [message for message in conversation_messages if message != ""]
        # keep only messages with less than number_of_words_max_per_message words or else keep only first number_of_words_max_per_message words
        conversation_messages = [message if len(message.split()) < number_of_words_max_per_message else " ".join(message.split()[:number_of_words_max_per_message]) for message in conversation_messages]
        # remove duplicate messages but keep order
        conversation_messages = sorted(set(conversation_messages), key=lambda x: conversation_messages.index(x))
        # get number of messages to sample
        number_of_messages = len(user_messages[conversation])
        number_of_messages_to_sample = int(number_of_messages / total_number_of_messages * total_desired_number_of_messages)
        # get first three messages and a random sample of the rest to get number_of_messages_to_sample messages
        if (number_of_messages_to_sample <= 3):
            if not (number_of_messages_to_sample == 0):
                sampled_conv_messages = conversation_messages[:number_of_messages_to_sample]
        else:
            sampled_conv_messages = conversation_messages[:3] + get_ordered_random_sample(conversation_messages[3:], number_of_messages_to_sample - 3)
        sampled_messages.append(sampled_conv_messages)
    # flatten the list of lists
    user_messages = [message for conversation in sampled_messages for message in conversation]
    # remove duplicate messages but keep order
    user_messages = sorted(set(user_messages), key=lambda x: user_messages.index(x))
    return user_messages

def get_number_of_tokens(messages, model_name):
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(messages))
    return num_tokens