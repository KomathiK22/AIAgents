import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic
from IPython.display import Markdown, display

load_dotenv(override=True)

# Print the key prefixes to help with any debugging

openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')
deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:50]}")
else:
    print("OpenAI API Key not set")

if anthropic_api_key:
    print(f"Anthropic API Key exists and begins {anthropic_api_key[:50]}")
else:
    print("Anthropic API Key not set (and this is optional)")

if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:50]}")
else:
    print("Google API Key not set (and this is optional)")

if deepseek_api_key:
    print(f"DeepSeek API Key exists and begins {deepseek_api_key[:50]}")
else:
    print("DeepSeek API Key not set (and this is optional)")

if groq_api_key:
    print(f"Groq API Key exists and begins {groq_api_key[:50]}")
else:
    print("Groq API Key not set (and this is optional)")

request="Come up with the best problems faced in common by  All Retail supply chain major companies which can be automated and built using AI Agents"
request+="Give usecase example with problem statement"
message=[{"role":"user","content":request}]

##OPEN AI for forming question
openai = OpenAI()
response = openai.chat.completions.create(
    model="gpt-4o-mini",
    messages=message,
)
question = response.choices[0].message.content
print(question)


################################################################################3
#List of Models, Answers,Messages
competitors = []
answers = []
messages = [{"role": "user", "content": question}]


# OPENAI
model_name = "gpt-4o-mini"
response = openai.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content
display(Markdown(answer))
competitors.append(model_name)
answers.append(answer)


# Anthropic has a slightly different API, and Max Tokens is required
model_name = "claude-3-7-sonnet-latest"
claude = Anthropic()
response = claude.messages.create(model=model_name, messages=messages, max_tokens=1000)
answer = response.content[0].text
display(Markdown(answer))
competitors.append(model_name)
answers.append(answer)

#GEMINI
model_name = "gemini-2.0-flash"
gemini = OpenAI(api_key=google_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
response = gemini.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content
display(Markdown(answer))
competitors.append(model_name)
answers.append(answer)



## GROQ
# groq = OpenAI(api_key=groq_api_key, base_url="https://api.groq.com/openai/v1")
# model_name = "llama-3.3-70b-versatile"
# response = groq.chat.completions.create(model=model_name, messages=messages)
# answer = response.choices[0].message.content
# display(Markdown(answer))
# competitors.append(model_name)
# answers.append(answer)


##OLLAMA
# ollama = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
# model_name = "llama3.2"
# response = ollama.chat.completions.create(model=model_name, messages=messages)
# answer = response.choices[0].message.content
# display(Markdown(answer))
# competitors.append(model_name)
# answers.append(answer)

# So where are we?
print(competitors)
print(answers)


# It's nice to know how to use "zip"
for competitor, answer in zip(competitors, answers):
    print(f"Competitor: {competitor}\n\n{answer}")


# Let's bring this together - note the use of "enumerate"
together = ""
for index, answer in enumerate(answers):
    together += f"# Response from competitor {index+1}\n\n"
    together += answer + "\n\n"

    print(together)


judge = f"""You are judging a competition between {len(competitors)} competitors.
Each model has been given this question:

{question}

Your job is to evaluate each response and bring up the first 5 high priority based problems to solve using AI,for challenging and highly influential Interview performance and landing up in high paying job in USA 
 Respond with JSON, and only JSON, with the following format:
{{"results": ["best competitor number", "second best competitor number", "third best competitor number", ...]}}

Here are the responses from each competitor:

{together}

display with the Topic,Time, Resources and best Plan, with the ranked order of the competitors, nothing else. Do not include markdown formatting or code blocks.
Now respond with the JSON with the ranked order of the competitors, nothing else. Do not include markdown formatting or code blocks."""


print(judge)
judge_messages = [{"role": "user", "content": judge}]

# Judgement time!
openai = OpenAI()
response = openai.chat.completions.create(
    model="o3-mini",
    messages=judge_messages,
)
results = response.choices[0].message.content
print(results)


# OK let's turn this into results!
results_dict = json.loads(results)
ranks = results_dict["results"]
for index, result in enumerate(ranks):
    competitor = competitors[int(result)-1]
    print(f"Rank {index+1}: {competitor}")


##Call each model and build an AI Agent to solve each problem and the business usecase in priority wise
model_name="gpt-4o-mini"
aiagent=f"""You are an AI Agent , you will build best accurate, robust and extensible  AI agents to fix each of the problems mentioned in the {results}."
         Make sure the agents are built in a way that they can read, write to db, or API call or form input to call API by making input using swagger URLs)"""
message={"role":"user","content":aiagent}
response = openai.chat.completions.create(
    model=model_name,
    messages=message,
)
aiagents = response.choices[0].message.content
print(aiagents)

