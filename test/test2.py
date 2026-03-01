import requests
import json

for _ in range(10):

    resource = requests.get("https://wapi.wangyupu.com/api/nng")
    data = json.loads(resource.text)
    print(data['name'])