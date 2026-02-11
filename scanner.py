import requests
from bs4 import BeautifulSoup
from sql_scanner import scan_sql_injection
from xss_scanner import scan_xss


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
        url = "http://" + url

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        }

        response = requests.get(url, headers=headers, timeout=8)

        # Security header analysis
        header_results = check_security_headers(response.headers)

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract links
        links = []
        for link in soup.find_all("a", href=True):
            links.append(link["href"])

        # Extract forms
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
        xss_results = scan_xss(url, forms)

        return {
            "url": url,
            "security_headers": header_results,
            "links": links[:10],
            "forms": forms,
            "sql_vulnerabilities": sql_results,
            "xss_vulnerabilities": xss_results
        }

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
