from dotenv import load_dotenv
import os
from openai import OpenAI
import time

load_dotenv(override=True)

openai_api_key = os.getenv("OPENAI_API_KEY")

if openai_api_key:
    print(f"YEAH, API KEY FOUND START WITH '{openai_api_key[:8]}'")
else:
    print("NO KEY FOUND.")

openai = OpenAI()

# --- First API call and File Write ---
start_time_1 = time.time() # Start timer for the first process

# First API call
question1 = "Pick a business idea in web3 (crypto) that might be worth exploring for an Agentic AI opportunity."

message_params = [{
    "role": "user",
    "content": f"{question1}, no more continue for the chat. Don't continue conversation after the answer."
}]

response1 = openai.chat.completions.create(
    model="gpt-5-nano",
    messages=message_params
).choices[0].message.content

with open("output/business_idea.txt", "w", encoding="utf-8") as file:
    file.write(response1)
    print("done finding business!\nProcessing to next answer...")

end_time_1 = time.time()
duration_1 = end_time_1 - start_time_1

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

end_time_2 = time.time()
duration_2 = end_time_2 - start_time_2

# --- Results Output ---
total_duration = duration_1 + duration_2

print("\n--- Durations ---")
print(f"first_call: {duration_1:.2f} seconds")
print(f"second_call: {duration_2:.2f} seconds")
print(f"Total Combined Duration: {total_duration:.2f} seconds")

# you can use the model "gpt-5-nano" but it takes around 30 seconds.
# But the results are so far different, gpt-5-nano got more context, text format and perfect for bigger solution.