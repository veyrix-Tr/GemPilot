import os
import argparse
from dotenv import load_dotenv
from google.genai import Client, types
from constants import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = Client(api_key=api_key)


parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", default=False, help="Enable verbose mode")
args = parser.parse_args()

def main():

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0
            ),
        )

        if args.verbose:
            print("User prompt: ", args.user_prompt)
            if response.usage_metadata:
                print("Prompt tokens: ", response.usage_metadata.prompt_token_count)
                print("Response tokens: ", response.usage_metadata.candidates_token_count)
        
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        
        function_results = []
        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result=call_function(function_call, args.verbose)
                if not function_call_result.parts:
                    raise Exception("Function call result has no parts")

                function_call_response = function_call_result.parts[0].function_response
                if not function_call_response:
                    raise Exception("Function call response is empty")
                if not function_call_response.response:
                    raise Exception("Function call response has no response")

                # function_results list contains function_call_result.parts (which is a list), but types.Content expects parts to be a list of Part objects, not a list of lists
                function_results.extend(function_call_result.parts)
                if args.verbose:
                    print(f"-> {function_call_result.parts.function_response.response}")
            
            messages.append(types.Content(role="user", parts=function_results))

        else:
            print("Final response:\n", response.text)
            break
    else:
        print("Error: Maximum iterations reached without final response")
        exit(1)


if __name__ == "__main__":
    main()