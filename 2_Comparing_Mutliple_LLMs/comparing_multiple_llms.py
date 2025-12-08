# !pip install openai anthropic IPython
# for jupyter notebook 👆

import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic
from IPython.display import Markdown, display
import time
import pandas as pd

load_dotenv(override=True)

openai_api_key = os.getenv('OPENAI_API_KEY')
# anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')
# deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')

# Checking keys
if openai_api_key:
	print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
	print("OpenAI API Key not set")

# if anthropic_api_key:
#     print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
# else:
#     print("Anthropic API Key not set (and this is optional)")

if google_api_key:
	print(f"Google API Key exists and begins {google_api_key[:2]}")
else:
	print("Google API Key not set (and this is optional)")

# if deepseek_api_key:
#     print(f"DeepSeek API Key exists and begins {deepseek_api_key[:3]}")
# else:
#     print("DeepSeek API Key not set (and this is optional)")

if groq_api_key:
	print(f"Groq API Key exists and begins {groq_api_key[:4]}")
else:
	print("Groq API Key not set (and this is optional)")

# Making a Question!
request = "Please come up with a challenging, nuanced question that I can ask a number of LLMs to evaluate their intelligence. Make output in markdown format design"
request += "Answer only with the question, no explanation."
messages = [{"role": "user", "content": request}]

# Setup question and display with markdown + timer
openai = OpenAI()

q_start_time = time.time()
response = openai.chat.completions.create(
	model="gpt-5-nano",
	messages=messages,
)
question = response.choices[0].message.content

q_end_time = time.time()
duration = q_end_time - q_start_time
display(Markdown(question))
print(f"\nTime taken for API call for question: **{duration:.4f} seconds**")

# Setup for the competition!
competitors = []
answers = []
durations = []
question += "Don't make too long answer and arrange the output in Markdown format. No continuation of the chat, stop after the answer."
messages = [{"role": "user", "content": question}]

# Competitor1
model_name = "gpt-5-mini"

c1_start_time = time.time()

response = openai.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

c1_end_time = time.time()
c1_duration = c1_end_time - c1_start_time

print(f"\nTime taken for {model_name} API call: **{c1_duration:.4f} seconds**")
display(Markdown(answer))

competitors.append(model_name)
answers.append(answer)
durations.append(c1_duration)

# for Anthropic(Claude) and Deepseek
# Anthropic has a slightly different API, and Max Tokens is required

# model_name = "claude-sonnet-4-5"

# claude = Anthropic()
# response = claude.messages.create(model=model_name, messages=messages, max_tokens=1000)
# answer = response.content[0].text

# display(Markdown(answer))
# competitors.append(model_name)
# answers.append(answer)


# Deepseek
# deepseek = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com/v1")
# model_name = "deepseek-chat"

# response = deepseek.chat.completions.create(model=model_name, messages=messages)
# answer = response.choices[0].message.content

# display(Markdown(answer))
# competitors.append(model_name)
# answers.append(answer)


# Competitor 2
gemini = OpenAI(api_key=google_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
model_name = "gemini-2.5-flash"

c2_start_time = time.time()

response = gemini.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

c2_end_time = time.time()
c2_duration = c2_end_time - c2_start_time

print(f"Time taken for {model_name}: **{c2_duration:.4f} seconds**\n")
display(Markdown(answer))

competitors.append(model_name)
answers.append(answer)
durations.append(c2_duration)

# Competitor 3
groq = OpenAI(api_key=groq_api_key, base_url="https://api.groq.com/openai/v1")
model_name = "openai/gpt-oss-120b"

c3_start_time = time.time()

response = groq.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content

c3_end_time = time.time()
c3_duration = c3_end_time - c3_start_time

print(f"Time taken for {model_name}: **{c3_duration:.4f} seconds**\n")
display(Markdown(answer))

competitors.append(model_name)
answers.append(answer)
durations.append(c3_duration)

print(competitors)
print(durations)

# FINAL JUDGING STATE
# Combine all answers nicely
together = "\n\n".join(
	f"### Competitor {i + 1}: **{competitors[i]}**\n{answer}"
	for i, answer in enumerate(answers)
)

print(together)
# for jupyter_notebook => display(Markdown(together))


# — JUDGE PROMPT —
start_time = time.time()

judge_prompt = f"""Question asked:
{question.strip()}

Evaluate these {len(competitors)} responses for accuracy, clarity, reasoning, and overall quality.

Responses:
{together}

Return a clean Markdown response with:
1. Ranked list from best to worst
2. Short 1-sentence explanation for the winner
3. Final winner announcement

Use this exact format:
## Ranking
1. ...
2. ...

## Winner Explanation
...

## Final Winner
**Winner: ...**"""

response = openai.chat.completions.create(
	model="gpt-5",
	messages=[{"role": "user", "content": judge_prompt}],
)

judgement = response.choices[0].message.content
judge_duration = time.time() - start_time

# ── DISPLAY RESULT ──
display(Markdown("# LLM Competition Judgement"))
display(Markdown(f"**Judging time: {judge_duration:.2f} seconds**"))
display(Markdown(judgement))

# ── SAVE TO FILE WITH DURATION ──
with open("final_judgement.md", "w", encoding="utf-8") as f:
	f.write(f"# LLM Competition Judgement\n\n")
	f.write(f"**Judged in {judge_duration:.2f} seconds**\n\n")
	f.write(judgement)