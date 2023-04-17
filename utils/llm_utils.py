import os
import openai
import dotenv

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def create_chat_completion(prompt, model=None, temperature=None, max_tokens=None)->str:
    """Create a chat completion using the OpenAI API"""
    messages = [
        {"role": "user", "content": prompt}, 
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message["content"]


def prompt_chat(agent_description, prompt, model=None, temperature=None, max_tokens=None)->str:
    messages = [
        {"role": "system", "content": agent_description},
        {"role": "user", "content": prompt}, 
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message["content"]