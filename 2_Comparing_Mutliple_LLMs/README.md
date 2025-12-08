# Comparing Multiple LLMs
[FULL CODE .ipynb](comparing_multiple_llms.ipynb)

## Purpose
**Comparing Multiple LLMs** is a method used to test and evaluate different Large Language Models against each other automatically.<br><br>
*Concept*: Just like a competition or a benchmark test.<br>
Imagine you want to know which AI model is smarter or faster at answering a difficult question.<br>
Instead of asking them one by one manually, we write a script to:
1. Generate a tough question.
2. Ask that question to multiple AIs simultaneously.
3. Have a "Judge" AI decide who gave the best answer.

## Use Case
This lesson demonstrates how to build an **automated evaluation pipeline** where you can pitting different LLMs (like GPT-5, Gemini, Claude, and Open Source models) against each other to see which one performs best for a specific query.<br>
- Jupyter notebook users can run this cell by cell.
- Python script users can run it all at once.

## Why We Use It
- **Benchmarking**: To compare speed (latency) and quality of different models.
- **Selection**: To choose the best model for a specific task based on empirical evidence.
- **Automation**: To avoid the tedious process of manually copying and pasting questions and answers to judge them.
- **Cost/Performance Analysis**: To see if a cheaper/faster model (like an open-source one via Groq) can beat a proprietary one.

## Set ENV
To run this code, you need to set up your environment variables first.

**Step 1:**
Create a new file named `.env` in your project root folder.

**Step 2:**
Add your API keys to the `.env` file as shown below:

```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_API_KEY=AIzaSyD-xxxxxxxxxxxxxxxxxxxxxxxx
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
# ANTHROPIC_API_KEY=sk-ant-xxxxxxxx (Optional)
# DEEPSEEK_API_KEY=sk-xxxxxxxx (Optional)
```
> **Note**: You need to obtain these keys from their respective providers (OpenAI, Google AI Studio, Groq Cloud, etc.).

## Code Explanation

### 1. Imports and Setup
```python
import os
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Markdown, display
import time

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')
```
- **Libraries**: We import necessary libraries for API access, environment variables, and display formatting.
- **load_dotenv**: Loads the API keys from your `.env` file.
- **Variables**: Stores the keys in variables for easy access.

---

### 2. Environment Verification
```python
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
```
- Simply checks if the API keys were loaded successfully.
- Prints a partial key to confirm (useful for debugging).

---

### 3. Generating the Question
```python
request = "Please come up with a challenging, nuanced question..."
messages = [{"role": "user", "content": request}]

openai = OpenAI()
response = openai.chat.completions.create(
    model="gpt-5-nano",
    messages=messages,
)
question = response.choices[0].message.content
```
- We ask a "smaller" fast model (`gpt-5-nano`) to generate a **challenging question** for the competition.
- This ensures the test is fresh and dynamic every time you run it.

---

### 4. The Competition (Competitors)
We then loop through different providers to get their answers.

**Competitor 1: GPT-5 Mini**
```python
model_name = "gpt-5-mini"
response = openai.chat.completions.create(model=model_name, messages=messages)
answer = response.choices[0].message.content
```
- Uses standard OpenAI API.

**Competitor 2: Gemini (via OpenAI Compatibility)**
```python
gemini = OpenAI(api_key=google_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
model_name = "gemini-2.5-flash"
response = gemini.chat.completions.create(...)
```
- Uses Google's Gemini model but via the OpenAI-compatible endpoint. This allows us to use the same `OpenAI` client code structure!

**Competitor 3: Open Source Model (via Groq)**
```python
groq = OpenAI(api_key=groq_api_key, base_url="https://api.groq.com/openai/v1")
model_name = "openai/gpt-oss-120b"
response = groq.chat.completions.create(...)
```
- Uses Groq's super-fast inference engine to run a large open-source model.

---

### 5. Final Judging State
```python
together = "\n\n".join(
    f"### Competitor {i + 1}: **{competitors[i]}**\n{answer}"
    for i, answer in enumerate(answers)
)
```
- Combines all the answers into a single string formatted in Markdown.
- This creates a document that looks like:
    - Competitor 1: [Answer]
    - Competitor 2: [Answer]
    - ...

---

### 6. The Judge
```python
judge_prompt = f"""Question asked: {question}
Evaluate these responses...
Return a clean Markdown response with:
1. Ranked list
2. Explanation
3. Final Winner"""

response = openai.chat.completions.create(
    model="gpt-5",
    messages=[{"role": "user", "content": judge_prompt}],
)
```
- **The Judge**: We use a highly capable model (`gpt-5`) to act as the judge.
- It reads the original question and all the competitors' answers.
- It decides who won based on accuracy, clarity, and reasoning.

---

### 7. Results and Saving
```python
with open("final_judgement.md", "w", encoding="utf-8") as f:
    f.write(judgement)
```
- Displays the judgment output.
- Saves the final result to `final_judgement.md` so you can review it later.

## Performance Metrics
The script also tracks:
- **Duration**: How long each model took to answer.
- **Judge Duration**: How long it took to evaluate the results.

This helps you balance **speed vs. quality** in your own applications.

---

## [Back to Menu](../README.md)
