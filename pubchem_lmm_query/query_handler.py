import openai
import json
from openai import OpenAI
import logging
from config import tools
from pubchem_api_client import pug_rest_request
from response_processor import query_response

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    query = input("Enter a query: ")

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant who provides information that can be found on PubChem to users based on their queries. Use the supplied tools to assist the user by creating a query for PubChem's PUG-REST API."
        },
        {
            "role": "user",
            "content": query
        }
    ]

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
        )
    except Exception as e:
        logging.error(f"Error making OpenAI API call: {str(e)}")
        return


    tool_call = response.choices[0].message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)

    data = pug_rest_request(**arguments)

    client = OpenAI()
    output = query_response(query, data, client)
    print(output)

if __name__ == '__main__':
    main()


