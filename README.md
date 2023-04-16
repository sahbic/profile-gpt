# ProfileGPT

## What does ChatGPT know about you ?

ProfileGPT is an app that analyzes a user's profile and personality as seen by ChatGPT.

The goal of this tool is to raise awareness about personal data usage, and the importance of responsible AI.

Example of information that can be extracted with ProfileGPT:

- **Personal Information**
- **Life Summary** : a summary the user's education, work, family, and personal history.
- **Hobbies/Interests** : a list of hobbies and interests.
- **Personality Assessment** : an assessment of the user's personality, offering a deep understanding of their psychological profile.
- **Political/Religious Views** : a guess on the user's political or religious views, if available from their messages.
- **Mental Health Evaluation** : ProfileGPT evaluates the user's mental health.
- **Predictions on Future Aspects**: ProfileGPT offers predictions on various aspects of the user's future.

## Installation

To install ProfileGPT, follow these steps:

1. Clone the repository:

```
git clone https://github.com/sahbic/profile-gpt.git
```

2. Navigate to the project directory:

```
cd 'profile-gpt'
```

3. Install the required dependencies:

```
pip install -r requirements.txt
```

4. Rename `.env.example` to `.env` and fill in your `OPENAI_API_KEY`.

## How tu use this app

1. Sign in to ChatGPT at https://chat.openai.com
2. In the bottom left of the page click on **Settings**
3. Click on **Export data**
4. Use the link in the email to download your data
5. Upload the zip file using **Browse files** button
6. Click on **Start Analysis**