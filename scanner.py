import requests
from bs4 import BeautifulSoup
from sql_scanner import scan_sql_injection
from xss_scanner import scan_xss
from crawler import get_all_links

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive"
}


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


# Remove duplicate findings
def unique_vulnerabilities(vulns):
    seen = set()
    unique = []

    for v in vulns:
        key = (v.get("action"), v.get("method"), v.get("payload"))
        if key not in seen:
            seen.add(key)
            unique.append(v)

    return unique


def extract_forms(url):
    forms = []

    try:
        response = requests.get(url, headers=HEADERS, timeout=8)
        soup = BeautifulSoup(response.text, "html.parser")

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

    except requests.exceptions.RequestException:
        pass

    return forms


def fetch_website(url):
    if not url.startswith("http"):
        url = "http://" + url

    try:
        response = requests.get(url, headers=HEADERS, timeout=8)
        header_results = check_security_headers(response.headers)

        # Crawl website
        discovered_links = get_all_links(url)
        all_pages = [url] + discovered_links[:5]

        all_forms = []
        sql_vulns = []
        xss_vulns = []

        for page in all_pages:
            forms = extract_forms(page)
            all_forms.extend(forms)

            sql_vulns.extend(scan_sql_injection(page, forms))
            xss_vulns.extend(scan_xss(page, forms))

        # Clean duplicates
        sql_vulns = unique_vulnerabilities(sql_vulns)
        xss_vulns = unique_vulnerabilities(xss_vulns)

        return {
            "url": url,
            "security_headers": header_results,
            "links": all_pages,
            "forms": all_forms,
            "sql_vulnerabilities": sql_vulns,
            "xss_vulnerabilities": xss_vulns
        }

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
