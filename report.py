def generate_report(scan_result):
    if "error" in scan_result:
        return {"error": scan_result["error"]}

    sql_count = len(scan_result.get("sql_vulnerabilities", []))
    xss_count = len(scan_result.get("xss_vulnerabilities", []))

    missing_headers = [
        h for h, v in scan_result.get("security_headers", {}).items()
        if v != "Present"
    ]
    header_count = len(missing_headers)

    # Determine overall risk
    if sql_count > 0:
        risk = "HIGH"
    elif xss_count > 0:
        risk = "HIGH"
    elif header_count > 2:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return {
        "target": scan_result.get("url"),
        "sql_injection": sql_count,
        "xss": xss_count,
        "missing_headers": header_count,
        "risk": risk
    }
