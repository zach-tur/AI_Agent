import os
import sys

from dotenv import load_dotenv

from google import genai
from google.genai import types


from call_function import available_functions, call_function
from prompts import system_prompt
from config import MAX_ITERS

args = sys.argv[1:]
verbose = any(arg == "--verbose" for arg in sys.argv)
model_name = "gemini-2.0-flash-001"


def create_client():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    return genai.Client(api_key=api_key)


def parse_arguments():
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python mani.py "How do I build a calculator app?"')
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


def generate_content(client, messages, verbose):
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )

        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.function_calls:
            function_responses = []
            for function_call in response.function_calls:
                function_call_result = call_function(function_call, verbose)
                if (
                    function_call_result
                    and function_call_result.parts
                    and len(function_call_result.parts) > 0
                    and function_call_result.parts[0].function_response
                ):
                    if verbose:
                        response_data = function_call_result.parts[
                            0
                        ].function_response.response
                        if response_data and "result" in response_data:
                            print(f"-> {response_data['result']}")
                        elif response_data and "error" in response_data:
                            print(f"-> {response_data['error']}")

                    function_responses.append(function_call_result.parts[0])
            messages.append(types.Content(role="user", parts=function_responses))

            return None
        else:
            return response.text

    except Exception as e:
        print(f"Error: {e}")


def print_results_verbose(response):
    prompt_tokens = getattr(response.usage_metadata, "prompt_token_count", 0)
    response_tokens = getattr(response.usage_metadata, "candidates_token_count", 0)
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")


def main():
    user_prompt = parse_arguments()
    client = create_client()
    messages = create_messages(user_prompt)
    verbose = "--verbose" in sys.argv

    for i in range(MAX_ITERS):
        try:
            result = generate_content(client, messages, verbose)

            if result:
                print("Final response:")
                print(result)
                if verbose:
                    print_results_verbose(result)
                break

        except Exception as e:
            print(f"Error calling API: {e}")
            return


if __name__ == "__main__":
    main()
