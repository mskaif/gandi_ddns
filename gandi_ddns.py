import json
import requests


def update_DNS(domain, api_key, record_name, record_type):
    external_ip = requests.get('https://api.ipify.org').content.decode('utf8')
    # get external ip
    records = requests.get(
        url=f"https://api.gandi.net/v5/livedns/domains/{domain}/records",
        headers={"Authorization": f"Apikey {api_key}"},
    )
    for record in records.json():
        if (
                record["rrset_type"] ==  record_type and
                record["rrset_name"] ==  record_name and
                record["rrset_values"][0] == external_ip
        ):
            print("External ip stays the same. No further action")
            return
    # update external ip if there is change
    data = {
        "rrset_name": record_name,
        "rrset_type": record_type,
        "rrset_values": [external_ip],
        "rrset_ttl": 300
    }
    response = requests.post(
        url=f"https://api.gandi.net/v5/livedns/domains/{domain}/records",
        headers={"Authorization": f"Apikey {api_key}"},
        json=data
    )
    print(response.json()["message"])


with open("secrets.json") as f:
    secrets = json.load(f)

update_DNS(
    domain=secrets["domain"],
    api_key=secrets["apikey"],
    record_name=secrets["name"],
    record_type=secrets["type"],
)
