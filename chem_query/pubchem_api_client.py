import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
            if data:
                return data
            else:
                logging.info(f"No results found for query: {identifiers}")
        else: # if request is not successful
            logging.info(f"Error: {response.status_code} - {response.text}")


    except Exception as e:
        logging.error(f"An error occurred: {e}")
