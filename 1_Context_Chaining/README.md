# Context Chaining
[Full code:](context_chaining.py)

## Purpose
**Context Chaining** fundmental concept ဖြစ်ပါတယ်<br>
*Context*: မြန်မာလို 'စကားစပ်'လို့ အဓိပ္ပာယ်ရပါတယ်
မိမိနဲ့ လူတစ်ယောက် အကြောင်းအရာတစ်ခုကို ဆွေးနွေးနေတယ်ဆိုပါစို့
ဥပမာ "ဆီကားတွေက ဘယ်လိုကောင်းကြောင်း EV တွေကလည်း ဘယ်လိုကောင်းကြောင်း" တစ်ယောက်နဲ့ တစ်ယောက် ဆွေးနွေးပြောဆိုနေကြတယ်ဆိုပါတော့
မိမိက ဒီအကြောင်းအရာကို ပြောပြီးတဲ့အချိန် တစ်ဖက်လူကလည်း ဒီအကြောင်းအရာနဲ့ ဆက်စပ်တဲ့ စကားကိုပဲပြန်ပြောမှာဖြစ်ပါတယ်
တစ်ဖက်လူက "EV ကားတွေကတော့ နောင်တစ်ချိန်မှာ တော်တော်အသုံးများလာမှာကွ"လို့ပြောလိုက်တဲ့အချိန်မှာ မိမိက "ငါဒီနေ့ ငါးဟင်းနဲ့ ထမင်းစားပြီးပြီ"လို့ ပြောလိုက်ရင် တစ်ဖက်လူက ကြောင်သွားမှာပေ့ါ
အဲ့ဒါကို စကားအစပ်အဆက်လွတ်သွားတယ်လို့ခေါ်ပါတယ်
တစ်ဖက်က "EV ကား" အကြောင်းပြောနေတဲ့အချိန် ကိုယ်ကလည်း အဲ့ဒါနဲ့ဆက်စပ်တဲ့ စကားကိုပြန်ပြောရမှာဖြစ်ပါတယ် 
ဒါကိုပဲ 'Context' လို့ သုံးနှုန်းတာဖြစ်ပါတယ်


## Use Case
ဒီသင်ခန်းစာမှာတော့ AI တွေနဲ့ မိမိ(programming အရ)စကားပြောဆိုတဲ့အခါမှာ စကားအဆက်အစပ် မလွတ်သွားအောင် (အဆက်အစပ်ရှိနေအောင်) ဘယ်လို လက်ဆင့်ကမ်းသွားရမလဲဆိုတာ လေ့လာရမယ့် basic သင်ခန်းစာတစ်ခုဖြစ်ပါတယ်

Essential Lesson တစ်ခုဖြစ်လို့ ကျော်လို့မရပါဘူး
Complex Agent တွေရဲ့ First step တစ်ခုလို့ပြောလည်းမမှားပါဘူး
This pattern is essential for building complex agents that need to:

## Why We Use It
- prompt တစ်ခုတည်းနဲ့ မလုံလောက်တဲ့အခါ (သို့မဟုတ်) ရလာတဲ့ resultကို တဖန်စစ်ထုတ်ချင်တဲ့အခါ(filtering) တွေမှာ သုံးတာဖြစ်ပါတယ်
- (တစ်နည်း) အရမ်းကောင်းမွန်တိကျတဲ့ အဖြေတစ်ခုကိုလိုချင်တဲ့အချိန်မှာလည်းသုံးနိုင်ပါတယ်
- (တစ်နည်း) ပြဿနာတစ်ခုကို ရှာခိုင်းပြီး ထိုပြဿနာကို ထပ်မံ ဖြေရှင်းခိုင်းတဲ့အခါမှာလည်းသုံးပါတယ်
- and so on...
---

## Set ENV
Code ကို runနိုင်ဖို့အတွက် ပထမဦးဆုံး Environment setup လုပ်ထားဖို့လိုအပ်ပါတယ်

**Step 1: Create a `.env` file**
Project folder ထဲမှာ `.env` ဆိုတဲ့ file name နဲ့ file အသစ်တစ်ခုဆောက်ပါ
(windows မှာဆိုရင် new text file ယူပြီး `.env` လို့ rename ပေးလိုက်ပါ)

**Step 2: Add your OpenAI API Key**
`.env` file ထဲမှာ အောက်ပါအတိုင်း မိမိရဲ့ OpenAI API key ကိုထည့်ပါ

```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx
```

> **Note**: `sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx` နေရာမှာ မိမိရဲ့ ကိုယ်ပိုင် API key ကို [OpenAI Platform](https://platform.openai.com/api-keys) ကနေ copy ယူပြီး ထည့်ပေးရမှာဖြစ်ပါတယ်



## Code Explanation

### 1. Imports and Setup
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
