import os
from dotenv import load_dotenv
from google import genai


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.",
)

prompt_tokens = getattr(response.usage_metadata, "prompt_token_count", 0)
response_tokens = getattr(response.usage_metadata, "candidates_token_count", 0)


def print_tokens():
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")


def main():
    print("Hello from ai-agent!")
    print(response.text)
    print_tokens()


if __name__ == "__main__":
    main()
