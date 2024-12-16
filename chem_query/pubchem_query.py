import requests

def pug_rest_request(domain: str, namespace: str, identifiers: str, operation: str, output_format: str = "JSON") -> dict:
    """
    Sends a request to the PubChem PUG-REST API based on the user's query.

    Arguments:
    domain (str): The type of entity being searched (e.g., 'substance', 'compound', 'protein').
    namespace (str): The attribute used for searching (e.g., 'name', 'cid', 'smiles').
    identifiers (str): Search terms, either a keyword (e.g., 'ethanol') or a comma-separated list of numbers (e.g., '7,0,2').
    operation (str): Specifies the type of information to return (e.g., 'cids', 'formula').
    output_format (str): The format for the returned data (default is 'JSON').

    Returns:
    dict: A dictionary containing the output variables as keys and their corresponding values.
    """
    # Base URL for PubChem PUG-REST API
    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"

    # Create endpoint url
    # Example: "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/ethanol/cids/JSON" would be used to find the CID of ethanol in JSON format
    endpoint = f"{base_url}/{domain}/{namespace}/{identifiers}/{operation}/{output_format}" 
    try:
        response = requests.get(endpoint)    

        if response.status_code == 200: # if request is successful
            data = response.json()  # Parse JSON response
            results = data.get("IdentifierList", {})
            
            if results:
                print(f"Found {len(results)} {domain}(s) matching '{identifiers}':") # Example: Found 1 compound(s) matching 'ethanol' 
                return results  # returns output dictionary. Example: {'CID': [702]}
            else:
                print(f"No results found for query: {identifiers}")
        else: # if request is not successful
            print(f"Error: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example use
# domain = "compound"
# namespace = "name"
# identifiers = "ethanol"
# operation = "cids"
# output_format = "JSON"

# ethanol_cids = pug_rest_request(domain, namespace, identifiers, operation, output_format=output_format)
# print(ethanol_cids)