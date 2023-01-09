import requests

resp = requests.post(
    "https://get-prediction-i5wplx5u5a-oa.a.run.app", # http://localhost:5000 ",
    json={"text": "I love you", "task_type": "node_classification"},
    headers={"Content-Type": "application/json"},
)

print(resp.json())