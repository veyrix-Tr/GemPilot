import os
import argparse
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
args = parser.parse_args()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=args.user_prompt
)

def main():
    # print(response)
    if response.usage_metadata:
        print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
        print("Response tokens: ", response.usage_metadata.candidates_token_count)
    print("Response: \n",response.text)



if __name__ == "__main__":
    main()
