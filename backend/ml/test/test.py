import requests

# Import a json file named test_payload.json. Post this request as json
import json
with open('test_payload.json') as f:
    test_payload = json.load(f)

resp = requests.post(
    "http://localhost:5000", #  https://get-prediction-i5wplx5u5a-oa.a.run.app",
    json=test_payload,
    headers={"Content-Type": "application/json"},
)

print(resp.json())