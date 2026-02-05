import re

def validate_code_safety(code: str) -> bool:
    """
    Performs a regex-based pre-flight check to block dangerous patterns.
    Returns True if safe, False if a violation is detected.
    """
    if not code:
        return False

    # Blocked patterns (Imports and Function calls)
    dangerous_patterns = [
        r"import\s+os",
        r"from\s+os\s+import",
        r"import\s+subprocess",
        r"from\s+subprocess\s+import",
        r"import\s+sys", # often used for sys.modules manipulation
        r"import\s+shutil",
        r"os\.system",
        r"os\.popen",
        r"os\.spawn",
        r"os\.exec",
        r"subprocess\.run",
        r"subprocess\.Popen",
        r"subprocess\.call",
        r"subprocess\.check_output",
        r"eval\(",
        r"exec\(",
        r"open\(", # simplistic block, might be too aggressive but safe for PVE
        r"__import__",
        r"globals\(",
        r"locals\(",
        r"input\(" # blocking interactive input
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, code):
            print(f"Security Violation Detected: Matches pattern '{pattern}'")
            return False

    return True
