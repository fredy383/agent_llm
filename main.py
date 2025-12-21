import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    parser = argparse.ArgumentParser(description="Fredobot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt`

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("API Key not found")

    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    generation = client.models.generate_content(model='gemini-2.5-flash', contents=messages)

    if args.verbose == True:

        tokens_prompt = generation.usage_metadata.prompt_token_count
        tokens_answer = generation.usage_metadata.candidates_token_count

        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {tokens_prompt}")
        print(f"Response tokens: {tokens_answer}")

    print(generation.text)

if __name__ == "__main__":
    main()
