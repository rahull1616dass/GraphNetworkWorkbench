import requests

resp = requests.post("https://get-prediction-i5wplx5u5a-nw.a.run.app", files={'file': open('eight.png', 'rb')})

print(resp.json())
