# query_generator.py
import urllib.parse

def generate_queries(title: str, address: str):
    """
    Return list of 4 encoded Google search URLs and the tab names.
    """
    base = "https://www.google.com/search?q="
    q_templates = [
        "is the restaurant {} at {} a franchise?",
        "owner of restaurant {} at {}",
        "social platforms of restaurant {} at {}",
        "inauguration or start date of {} at {}"
    ]

    queries = [tmpl.format(title, address) for tmpl in q_templates]
    encoded = [urllib.parse.quote_plus(q) for q in queries]
    final_urls = [f"{base}{e}" for e in encoded]
    tab_names = ["franchise_info", "owner_info", "social_platforms", "start_date"]
    return final_urls, queries, tab_names


def linkedin_owner_query(owner_name: str, title: str):
    """
    Create an encoded Google query for the owner's LinkedIn profile.
    """
    base = "https://www.google.com/search?q="
    q = f"linkedin profile of {owner_name} owner of the {title}"
    return f"{base}{urllib.parse.quote_plus(q)}"


def generate_one_time_queries(title: str, address: str):

    base = "https://www.google.com/search?q="
    q_templates = [
        "is the restaurant {} at {} a franchise?",
        "owner of restaurant {} at {}",
        "social platforms of restaurant {} at {}",
        "inauguration or start date of {} at {}",
    ]
    queries = [tmpl.format(title, address) for tmpl in q_templates]
    encoded = [urllib.parse.quote_plus(q) for q in queries]
    final_urls = [f"{base}{e}" for e in encoded]
    return final_urls