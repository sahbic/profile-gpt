import os
import openai
import dotenv

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Overly simple abstraction until we create something better
def prompt_chat(prompt, model=None, temperature=None, max_tokens=None)->str:
    """Create a chat completion using the OpenAI API"""
    messages = [{"role": "user", "content": prompt}, ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message["content"]