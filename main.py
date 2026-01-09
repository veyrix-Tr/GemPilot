import os
import argparse
from dotenv import load_dotenv
from google.genai import Client, types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", default=False, help="Enable verbose mode")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=messages
)

def main():
    # print(response)
    if args.verbose:
        print("User prompt: ", args.user_prompt)
        if response.usage_metadata:
            print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
            print("Response tokens: ", response.usage_metadata.candidates_token_count)
    print("Response: \n",response.text)



if __name__ == "__main__":
    main()
