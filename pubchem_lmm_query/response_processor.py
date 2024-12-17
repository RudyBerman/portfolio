from openai import OpenAI
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def query_response(initial_query: str, data: dict, client: OpenAI) -> str:
    """
    Processes the response from a PubChem API query and generates a natural language summary.

    Arguments:
    initial_query (str): The user's original query, typically asking for information about a chemical entity.
    data (dict): The data returned from the PubChem PUG-REST API request, formatted as a dictionary.
    client (OpenAI): An instance of the OpenAI client used to generate the natural language response.

    Returns:
    str: A natural language response to the user's initial query based on the API results.
    """

    system_prompt = """You are an expert scientist, and your job is to communicate technical information clearly and concisely.
    You will be provided with a user's initial search query, and the results of that query in the form of a dictionary.
    You should summarise the information within the dictionary that is relevant to the user's query."""

    output_query = f"User's query: {initial_query}. Results: {data}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": output_query}
    ]

    try:
        stream = client.chat.completions.create(
            messages=messages,
            model="gpt-4o", 
            stream=True,
        )

        response_text = ""
        for chunk in stream:
            response_text += chunk.choices[0].delta.content or ""
        
        return response_text.strip()

    except Exception as e:
        logging.error(f"Error in query_response: {str(e)}")
        return "An error occurred while processing your request."




