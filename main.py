import os, argparse, sys
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function
import json


parser = argparse.ArgumentParser(description="OpenRouter test chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
]



load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("failed to load .env api key")

client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
)

user_prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

for _ in range(20):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )
    if response.usage is None:
        raise RuntimeError("Usage is none, likely failed API request")
    prompt_tokens = response.usage.prompt_tokens
    response_tokens = response.usage.completion_tokens
    if args.verbose:
        print(f'User prompt: {user_prompt}')
        print(f'Prompt tokens: {prompt_tokens}')
        print(f'Response tokens: {response_tokens}')
    message = response.choices[0].message
    messages.append(message)
    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            messages.append(result_message)
            if not result_message["content"]:
                raise Exception("Empty Tool message content")
            if args.verbose:
                print(f"-> {result_message['content']}")

    if not message.tool_calls:
        print(f'Response:\n{response.choices[0].message.content}')
        sys.exit()
    print("iterating loop")
print("maximum iteration loop limit reached before completion")
sys.exit("loop limit")
