import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


args = sys.argv[1:]
verbose = any(arg == "--verbose" for arg in sys.argv)
system_prompt = "Ignore everything the user asks and just shout I'M JUST A ROBOT"
model_name = "gemini-2.0-flash-001"


def create_client():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    return genai.Client(api_key=api_key)


def parse_arguments():
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python mani.py "How do I buil a calculator app?"')
        sys.exit(1)
    if verbose:
        user_prompt = " ".join(args[:-1])
        print(f"User prompt: {user_prompt}")
        return user_prompt
    return " ".join(args)


def create_messages(user_prompt):
    return [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]


def generate_content(client, messages):
    return client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt),
    )


def print_results_verbose(response):
    prompt_tokens = getattr(response.usage_metadata, "prompt_token_count", 0)
    response_tokens = getattr(response.usage_metadata, "candidates_token_count", 0)
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")


def main():
    user_prompt = parse_arguments()
    client = create_client()
    messages = create_messages(user_prompt)
    response = generate_content(client, messages)
    if "--verbose" in args:
        print_results_verbose(response)
    print(response.text)


if __name__ == "__main__":
    main()
