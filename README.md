# ProfileGPT

ProfileGPT is an app that analyzes a user's profile as seen by ChatGPT, providing insights about the personality of the user.

The goal of this app is to raise awareness about personal data usage, and the importance of respecting GDPR regulations.

ProfileGPT aims to highlight the significance of safeguarding personal information and promoting responsible data sharing practices.

Information that can be extracted with ProfileGPT:

- **Personal Information** : ProfileGPT extracts the user's name from their messages or email address and identifies their country based on phone number country code, providing accurate personal information.
- **Life Summary** : ProfileGPT generates a short paragraph summarizing the user's education, work, family, and personal history based on their messages, giving a concise overview of their background.
- **Hobbies/Interests** : ProfileGPT categorizes the user's hobbies and interests based on the list of conversation titles and their messages, providing a list of categories.
- **Personality Assessment** : ProfileGPT assesses the user's personality traits, including their character, values, beliefs, emotions, motivations, strengths, and weaknesses, based on their messages, offering a deep understanding of their psychological profile.
- **Political/Religious Views** : ProfileGPT makes a guess on the user's political or religious views, if available from their messages, giving insights into their potential ideologies.
- **Mental Health Evaluation** : ProfileGPT evaluates the user's mental health based on their messages, providing a concise one-sentence assessment to gauge their well-being.
- **Predictions on Future Aspects**: ProfileGPT offers predictions on various aspects such as the user's future, career, and relationships based on their messages, providing valuable insights into potential future outcomes.

## Installation

To install ProfileGPT, follow these steps:


1. Clone the repository:

```
git clone 
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