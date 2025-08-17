#!/usr/bin/env python3

# Script to fix patient_message to message in medical AI tests

import re

# Read the file
with open('/app/backend_test.py', 'r') as f:
    content = f.read()

# Replace patient_message with message in medical AI test contexts
# Look for patterns like "patient_message": "..." within medical AI test methods
pattern = r'"patient_message":\s*"([^"]*)"'
replacement = r'"message": "\1"'

# Replace all occurrences
new_content = re.sub(pattern, replacement, content)

# Write back to file
with open('/app/backend_test.py', 'w') as f:
    f.write(new_content)

print("Fixed patient_message to message in medical AI tests")