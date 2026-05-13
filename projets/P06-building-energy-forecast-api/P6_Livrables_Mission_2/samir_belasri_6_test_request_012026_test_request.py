import json
import requests

URL = "http://127.0.0.1:3000/predict"

payload = {
    "req": {   # BentoML attend la clé 'req' car la signature est predict(self, req: PredictRequest)
        "items": [
            {
                "PropertyGFATotal": 12000.0,
                "YearBuilt": 1998,
                "NumberofFloors": 6,
                "PrimaryPropertyType": "Office",
            }
        ]
    }
}

r = requests.post(URL, json=payload, timeout=30)
print("Status:", r.status_code)
print(json.dumps(r.json(), indent=2))

