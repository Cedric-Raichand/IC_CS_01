import requests


def fetch_website(url):
    if not url.startswith("http"):
        url = "https://" + url

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        return response.text[:1000]  # return first 1000 chars as preview
    except requests.exceptions.RequestException as e:
        return f"Error fetching website: {e}"
