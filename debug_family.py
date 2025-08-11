#!/usr/bin/env python3

import requests
import json
from datetime import datetime

# Test the family profile completion issue
base_url = "https://530c05ea-1599-4fd0-83d4-3b33fe32d971.preview.emergentagent.com/api"
test_user_id = f"debug_family_{datetime.now().strftime('%H%M%S')}"

# Create family profile with only family_structure
profile_data = {
    "user_id": test_user_id,
    "family_structure": {
        "family_role": "Parent",
        "number_of_members": 3,
        "primary_caregiver": True
    }
}

print("Creating family profile with only family_structure...")
response = requests.post(f"{base_url}/profiles/family", json=profile_data)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"Profile completion: {data.get('profile_completion', 'N/A')}%")
    print(f"Family structure: {data.get('family_structure', 'N/A')}")
    print(f"Family members: {data.get('family_members', 'N/A')}")
    print(f"Household management: {data.get('household_management', 'N/A')}")
    print(f"Care coordination: {data.get('care_coordination', 'N/A')}")
    
    # Clean up
    requests.delete(f"{base_url}/profiles/family/{test_user_id}")
else:
    print(f"Error: {response.text}")