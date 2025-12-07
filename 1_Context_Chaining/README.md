# Context Chaining

## Purpose
The purpose of this lesson is to demonstrate the fundamental concept of **Context Chaining** in Agentic AI. It illustrates how to connect multiple AI interactions into a coherent sequence, where the output of one step becomes the input (context) for the next. This mimics a thought process or a workflow.

## Use Case
This pattern is essential for building complex agents that need to:
- **Refine Ideas**: Generate a broad concept first, then critique or detail it in a subsequent step.
- **Process Data**: Extract information in step one, then format or summarize it in step two.
- **Plan and Execute**: Create a plan, then generate the code or content to execute that plan.

## Why We Use It
A single prompt is often insufficient for complex tasks. It can become too long, confusing for the model, or yield inconsistent results. **Chaining** breaks the problem down into manageable steps, allowing for:
- Better accuracy and focus at each stage.
- The ability to inspect intermediate results (like saving the business idea before finding pain points).
- Modular design where steps can be tweaked independently.

---

## Code Explanation

### 1. Imports and Setup
We start by importing necessary libraries. `dotenv` is used to securely load API keys, `os` for environment variables, `OpenAI` for the client, and `time` to track performance.

```python
from dotenv import load_dotenv
import os
from openai import OpenAI
import time

load_dotenv(override=True)

openai_api_key = os.getenv("OPENAI_API_KEY")
```

### 2. Environment Verification
This block checks if the API key is successfully loaded. It prints a masked version of the key to confirm presence without exposing the full secret, which is a good security practice.

```python
if openai_api_key:
    print(f"YEAH, API KEY FOUND START WITH '{openai_api_key[:8]}'")
else:
    print("NO KEY FOUND.")

openai = OpenAI()
```

### 3. First Link in the Chain (Idea Generation)
Here we execute the first step of our chain.
- We define a task: "Pick a business idea in web3".
- We send this to the model (`gpt-5-nano` is used here as an example placeholder for a high-capability model).
- The result (`response1`) contains the raw business idea.

```python
# --- First API call and File Write ---
start_time_1 = time.time() 

question1 = "Pick a business idea in web3 (crypto) that might be worth exploring for an Agentic AI opportunity."

message_params = [{
    "role": "user",
    "content": f"{question1}, no more continue for the chat. Don't continue conversation after the answer."
}]

response1 = openai.chat.completions.create(
    model="gpt-5-nano",
    messages=message_params
).choices[0].message.content
```

### 4. Saving Intermediate State
We save the output of the first step to a file. This is crucial for debugging and auditing agent flows. It allows you to see exactly what the first agent produced before the second agent takes over.

```python
with open("output/business_idea.txt", "w", encoding="utf-8") as file:
    file.write(response1)
    print("done finding business!\nProcessing to next answer...")

end_time_1 = time.time()
duration_1 = end_time_1 - start_time_1
```

### 5. Second Link in the Chain (Analysis & Solution)
**This is the core of Context Chaining.**
- Note the usage of `response1` inside `question2`.
- We are explicitly feeding the *previous output* into the *current prompt*.
- The model is asked to "Read the {response1}" and find pain points.
- This creates a dependency: Step 2 cannot exist without the context provided by Step 1.

```python
# --- Second API call ---
start_time_2 = time.time()

question2 = f"Read the {response1} and search for the pain point in that industry and solve with something challenging that might be ripe for Agentic AI solution."

message_params2 = [{
    "role": "user",
    "content": f"{question2}, no more continue for the chat. don't continue conversation after the answer."
}]

response2 = openai.chat.completions.create(
    model="gpt-5-nano",
    messages=message_params2
).choices[0].message.content

with open("output/pain_point_&_solution.txt", "w", encoding="utf-8") as file:
    file.write(response2)
    print("done finding solution")
```

### 6. Performance Metrics
Finally, we calculate and print how long each step took. This is vital for production agents where latency matters. It helps identify which link in the chain is the bottleneck.

```python
# --- Results Output ---
total_duration = duration_1 + duration_2

print("\n--- Durations ---")
print(f"first_call: {duration_1:.2f} seconds")
print(f"second_call: {duration_2:.2f} seconds")
print(f"Total Combined Duration: {total_duration:.2f} seconds")
```
