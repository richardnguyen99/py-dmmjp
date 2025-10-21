#!/usr/bin/env python3
"""
Pre-commit hook to detect and replace API keys and affiliate keys in files.

This hook scans all staged files for sensitive credentials defined in environment
variables and replaces them with obscured strings to prevent accidental exposure.
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple


def get_secret_patterns() -> List[Tuple[str, str, str]]:
    """
    Get secret patterns from environment variables.

    Returns:
        List of tuples (secret_value, secret_name, replacement_string)
    """

    patterns = []

    api_key = os.environ.get("APP_ID")
    if api_key and len(api_key) > 0:
        patterns.append((api_key, "APP_ID", "***REDACTED_APP_ID***"))

    affiliate_key = os.environ.get("AFF_ID")
    if affiliate_key and len(affiliate_key) > 0:
        patterns.append((affiliate_key, "AFF_ID", "***REDACTED_AFF_ID***"))

    return patterns


def check_file_for_secrets(
    file_path: str, patterns: List[Tuple[str, str, str]]
) -> Tuple[bool, List[str]]:
    """
    Check a file for secret patterns and replace them if found.

    Args:
        file_path: Path to the file to check
        patterns: List of (secret_value, secret_name, replacement) tuples

    Returns:
        Tuple of (secrets_found, list_of_findings)
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

    except (UnicodeDecodeError, IOError):
        return False, []

    secrets_found = False
    findings = []
    modified_content = content

    for secret_value, secret_name, replacement in patterns:
        if secret_value in content:
            secrets_found = True

            line_number = 0
            for line_num, line in enumerate(content.splitlines(), 1):
                if secret_value in line:
                    line_number = line_num
                    findings.append(
                        f"  Line {line_number}: Found {secret_name} in {file_path}"
                    )
                    break

            modified_content = modified_content.replace(secret_value, replacement)

    if secrets_found:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(modified_content)

    return secrets_found, findings


def main(filenames: List[str]) -> int:
    """
    Main function to check files for secrets.

    Args:
        filenames: List of files to check

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    patterns = get_secret_patterns()

    if not patterns:
        raise ValueError("No secret patterns found.")

    all_findings = []

    for filename in filenames:
        if not Path(filename).is_file():
            continue

        print(f"Check file: {filename}...", end=" ")
        secrets_found, findings = check_file_for_secrets(filename, patterns)

        if secrets_found:
            all_findings.extend(findings)
            print("\033[91msecret found\033[0m")
        else:
            print("\033[92mno secret found\033[0m")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
