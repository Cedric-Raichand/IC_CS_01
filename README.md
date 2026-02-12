#  Web Application Vulnerability Scanner

A beginner-friendly Dynamic Application Security Testing (DAST) tool built with **Python + Flask** that automatically scans web applications for common security vulnerabilities.

This project was developed as part of the **Interncred Cybersecurity Internship – Task 1**.

---

## Features

### Core Security Checks

* Security Headers Analysis
* SQL Injection Detection
* Cross‑Site Scripting (XSS) Detection
* Automated Form Discovery
* Multi‑Page Crawling

### Reporting & Analysis

* Vulnerability Deduplication
* Risk Level Classification (LOW / MEDIUM / HIGH)
* Scan Timestamp Evidence
* Clean Web Dashboard Interface

---

## How It Works

1. User enters a website URL
2. Scanner crawls internal pages
3. Extracts forms and inputs
4. Injects safe testing payloads
5. Analyzes responses
6. Generates summarized security report

This simulates a simplified real‑world penetration testing workflow.

---

## Project Structure

```
webscanner/
│── app.py                # Flask application controller
│── crawler.py            # Discovers internal links
│── scanner.py            # Main scanning engine
│── sql_scanner.py        # SQL injection detection
│── xss_scanner.py        # XSS detection
│── report.py             # Risk scoring & summary
│── templates/
│    └── index.html       # User interface
│── requirements.txt
└── README.md
```

---

## Installation & Setup

### 1. Clone Repository

```
git clone <your-repository-url>
cd webscanner
```

### 2. Create Virtual Environment (Recommended)

```
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate    # Mac/Linux
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Run Application

```
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

## Recommended Testing Targets (Legal Practice Labs)

Use intentionally vulnerable applications only:

* [http://testphp.vulnweb.com](http://testphp.vulnweb.com)
* [http://demo.testfire.net](http://demo.testfire.net)
* [http://zero.webappsecurity.com](http://zero.webappsecurity.com)

---

## Example Output

The scanner provides:

* Vulnerability counts
* Risk level
* Missing security headers
* Vulnerable form locations
* Payload evidence
* Scan timestamp

---

## Risk Rating Logic

| Condition            | Risk   |
| -------------------- | ------ |
| No vulnerabilities   | LOW    |
| Only headers missing | MEDIUM |
| SQLi or XSS found    | HIGH   |

---

## Legal & Ethical Notice

This tool is created for **educational purposes only**.

Do NOT scan systems without permission.

Only test:

* Applications you own
* Authorized penetration testing targets
* Intentionally vulnerable labs

Unauthorized scanning may violate cybersecurity laws.

---

## Technologies Used

* Python 3
* Flask
* Requests
* BeautifulSoup
* HTML

---

## Future Improvements

* Authentication bypass detection
* CSRF detection
* Export PDF report
* Async scanning
* GUI dashboard charts

---

## Author

**Cedrick Dzodzodzi**
Interncred Cybersecurity Internship Program

---

## License

Educational Use Only
