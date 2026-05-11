# from google import genai
# from google.genai import types
import pandas as pd
import re
from pydantic import BaseModel, Field

class MatchResult(BaseModel): # Model should figure out what to put in these fields based on the descriptions
    website: str = Field(description="The website name.")
    privacy_law: str = Field(description="The privacy law (e.g., 'CCPA').")
    rating: str = Field(description="The compliance rating (e.g., 'fully compliant').")

def get_prompt(website, laws, policy):
    return (
        f"You are an expert in legal reasoning and privacy framework enforcement. "
        f"Given the following website privacy policy and the different privacy laws which this website claims to be in compliance with, "
        f"provide a rating of the website's degree of compliance for each privacy law. Your rating output must be ONLY either 'fully compliant,' "
        f"'mostly compliant,' 'marginally compliant,' and 'not compliant.' Do not add any other output to the rating field."
        f"\n\nWebsite: {website}\nPrivacy Laws: {laws}\nPolicy:{policy}"
    )

# TODO: parllelize and make rate-limit safe
# def call_llm()
#   if not frameworks:
#       return None
# client = genai.Client()

# response = client.models.generate_content(
#     model="gemini-3.1-pro-preview",
#     contents=prompt,
#     config=types.GenerateContentConfig(
#         thinking_config=types.ThinkingConfig(thinking_level="medium")
#     ),
#     "response_format": {"text": {"mime_type": "application/json", "schema": MatchResult.model_json_schema()}},
# )

data = pd.read_csv('data_05_11_2026.csv', header=1)
policy_cols = ['Privacy Policy', 'Overflow(1)', '2', '3', '4', '5', '6']
data['full_policy'] = data[policy_cols].fillna('').agg(' '.join, axis=1).str.strip()
def parse_frameworks(val):
    if pd.isna(val):
        return []
    return re.findall(r'\b[A-Z][A-Z0-9\-]{2,}\b', str(val))

compliance_col = "Claimed compliance w/ privacy laws (e.g., 'GDPR', 'CCPA')"
data['claimed_frameworks'] = data[compliance_col].apply(parse_frameworks)

results = []
for _, row in data.head(5).iterrows():
    print(f"Rating {row['Website']}...")
    print(f"\n\n====Prompt====\n\n {get_prompt(row['Website'], row['claimed_frameworks'], row['full_policy'])}")
    # rating = rate_compliance(row['Website'], row['full_policy'], row['claimed_frameworks'])
    rating = "fully compliant"
    results.append({
        'website': row['Website'],
        'claimed': row['claimed_frameworks'],
        'ratings': rating
    })

print("\nSUMMARY")
for res in results:
    print(res)