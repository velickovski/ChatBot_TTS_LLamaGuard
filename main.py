from openai import OpenAI
from gtts import gTTS
import os
from fuzzywuzzy import fuzz

client = OpenAI(
    base_url="https://kfcfbfgr5u3vo2a8.us-east-1.aws.endpoints.huggingface.cloud/v1/",
    api_key="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"
)

def guard_check(content):
    chat_completion = client.chat.completions.create(
        model="tgi",
        messages=[
            {
                "role": "user",
                "content": content
            }
        ],
        stream=True,
        max_tokens=20
    )
    flag = True
    for message in chat_completion:
        if(message.choices[0].delta.content=="unsafe"):
            flag = False
    return flag


# Replace with your own OpenAI API key


ALLOWED_TOPICS = ["airplanes"]


def is_question_within_topic_fuzzy(question: str, allowed_topics: list):
    for topic in allowed_topics:
        if fuzz.partial_ratio(topic.lower(), question.lower()) > 70:
            return True
    return False


def chatbot(prompt):
    try:
        clients = OpenAI(api_key='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')
        response = clients.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"


def speak_text(text):
    tts = gTTS(text, lang='en', tld='com', slow=False)
    tts.save("response.mp3")
    os.system("mpg123 response.mp3")

def greeting():
    greeting_message = "Hi! How can I help you today?"
    print("Chatbot: "+greeting_message)
    speak_text(greeting_message)

if __name__ == "__main__":
    greeting()
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            speak_text("Goodbye!")
            break
        
        if (guard_check(user_input)):
            if (is_question_within_topic_fuzzy(user_input,ALLOWED_TOPICS)):
                response = chatbot(user_input)
                print(f"Chatbot: {response}")
                speak_text(response)
            else:
                print("Not in the topic for the day")
                speak_text("Not in the topic for the day")
        else:
            print("Not safe for our ChatBot!")
            speak_text("Not safe for our ChatBot")





