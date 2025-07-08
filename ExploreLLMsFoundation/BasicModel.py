import os

from IPython.display import Markdown, display
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)  ##whats in env takes priority
openAIapiKey = os.getenv('OPENAI_API_KEY')
# print(openAIapiKey)

openai = OpenAI()  ##Connect to openAI library on cloud to access OpenAI modules
messages = [{"role": "user", "content": "what is 2+2?"}]  ##create list of disctionary

response = openai.chat.completions.create(
    model="gpt-4.1-nano",
    messages=messages
)
# print(messages)
# print(response.choices[0].message.content)

##Ask question to the openAI
question1 = "Provide a fine tuned question to get end to end agentic AI code and learning from beginer to master, provide question only"
messages = [{"role": "user", "content": question1}]
# print(question)

# ask it - this uses GPT 4.1 mini, still cheap but more powerful than nano
response = openai.chat.completions.create(
    model="gpt-4.1-mini",
    messages=messages)
answer1 = response.choices[0].message.content
print(answer1)

# Send this question other model and find the tuned answer
messages = [{"role": "user", "content": answer1}]
response = openai.chat.completions.create(
    model="gpt-4.1-mini",
    messages=messages
)
answer2 = response.choices[0].message.content
# print(answer2)
display(Markdown(answer2))
