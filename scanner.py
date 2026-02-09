import requests
from bs4 import BeautifulSoup


def fetch_website(url):
    if not url.startswith("http"):
        url = "http://" + url  # try http first


    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)

        soup = BeautifulSoup(response.text, "html.parser")

        links = []
        for link in soup.find_all("a", href=True):
            links.append(link["href"])

        forms = []
        for form in soup.find_all("form"):
            form_details = {}
            form_details["action"] = form.get("action")
            form_details["method"] = form.get("method", "get").lower()

            inputs = []
            for input_tag in form.find_all("input"):
                input_type = input_tag.get("type", "text")
                input_name = input_tag.get("name")
                inputs.append({"type": input_type, "name": input_name})

            form_details["inputs"] = inputs
            forms.append(form_details)

        return {
            "url": url,
            "links": links[:10],  # limit so page not too long
            "forms": forms
        }

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
