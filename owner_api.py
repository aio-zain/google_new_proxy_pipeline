# owner_api.py
import requests

OWNER_API_URL = "http://44.231.228.32:8057/get_owner_names_from_json"
REQUEST_TIMEOUT = 10  # use 10s per your function

def fun_send_to_api(owner_dict):
    """
    Send owner data to API endpoint using the exact method you provided.
    Returns the parsed JSON response (or None on failure).
    """
    url = OWNER_API_URL
    try:
        response = requests.post(url, json=owner_dict, timeout=REQUEST_TIMEOUT)
        print(f"API Status Code: {response.status_code}")
        try:
            j = response.json()
            print(f"API Response: {j}")
            return j
        except Exception:
            print(f"API Response Text: {response.text}")
            return None
    except Exception as e:
        print(f"❌ API request failed: {e}")
        return None


def parse_owner_names_from_response(api_response):
    """
    Given the API JSON response, extract and return a list of owner names.
    Expected shape: {'title':.., 'address':.., 'owner_names': [...]}
    Returns empty list if nothing found.
    """
    if not api_response:
        return []
    if isinstance(api_response, dict):
        if "owner_names" in api_response and isinstance(api_response["owner_names"], list):
            return [str(x).strip() for x in api_response["owner_names"] if x and str(x).strip()]
        # fallback heuristics
        for key in ("owners", "owners_list"):
            if key in api_response and isinstance(api_response[key], list):
                return [str(x).strip() for x in api_response[key] if x and str(x).strip()]
    return []
