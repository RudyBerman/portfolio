import openai
import json
from pubchem_query import pug_rest_request

tools = [
  {
      "type": "function",
      "function": {
          "name": "pug_rest_request",
          "description": "Sends request to PubChem's PUG-REST API. Call this whenever you need to provide chemical information about a given entity (such as a substance, compound, gene, protein, assay, etc), for example when a customer asks 'can you tell me the compound ID of ethanol' or 'give me the gene symbol of the human brca2 gene'",
          "parameters": {
              "type": "object",
              "properties": {
                  "domain": {
                      "type": "string",
                      "description": "The type of entity being searched (e.g., 'substance', 'compound', 'protein').",
                  },
                  "namespace": {
                      "type": "string",
                      "description": "The attribute used for searching (e.g., 'name', 'cid', 'smiles').",
                  },
                  "identifiers": {
                      "type": "string",
                      "description": "Search terms, either a keyword (e.g., 'ethanol') or a comma-separated list of numbers (e.g., '7,0,2').",
                  },
                  "operation": {
                      "type": "string",
                      "description": "Specifies the type of information to return (e.g., 'cids', 'formula').",
                  },
                  "output_format": {
                      "type": "string",
                      "description": "The format for the returned data (default is 'JSON').",
                  },
              },
              "required": ["domain", "namespace", "identifiers", "operation"],
              "additionalProperties": False,
          },
      }
  }
]

query = input("Ask a chem question: ")

messages = [
  {
      "role": "system",
      "content": "You are a helpful assistant who provides information that can be found on PubChem to user's based on their queries. Use the supplied tools to assist the user by creating a query for PubChem's PUG-REST API."
  },
  {
      "role": "user",
      "content": query
  }
]

response = openai.chat.completions.create(
  model="gpt-4o",
  messages=messages,
  tools=tools,
)

tool_call = response.choices[0].message.tool_calls[0]
arguments = json.loads(tool_call.function.arguments)
print(arguments, type(arguments))

out = pug_rest_request(**arguments)
print("OUTPUT:", out)