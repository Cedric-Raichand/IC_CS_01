import requests
from bs4 import BeautifulSoup
from sql_scanner import scan_sql_injection



def check_security_headers(headers):
    security_headers = {
        "Content-Security-Policy": "Missing CSP protection (XSS risk)",
        "Strict-Transport-Security": "Missing HSTS (HTTPS downgrade risk)",
        "X-Frame-Options": "Missing Clickjacking protection",
        "X-Content-Type-Options": "Missing MIME sniffing protection",
        "Referrer-Policy": "Missing Referrer Policy"
    }

    results = {}

    for header, message in security_headers.items():
        if header in headers:
            results[header] = "Present"
        else:
            results[header] = message

    return results


def fetch_website(url):
    if not url.startswith("http"):
        url = "http://" + url  # use http for vuln test sites

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)

        # Check security headers
        header_results = check_security_headers(response.headers)

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

        sql_results = scan_sql_injection(url, forms)

        return {
            "url": url,
            "security_headers": header_results,
            "links": links[:10],
            "forms": forms,
            "sql_vulnerabilities": sql_results
        }


    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
