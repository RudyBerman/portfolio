# Configuring tools object to be used for funcion calls.
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