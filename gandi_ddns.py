import json
import requests
from messenger import Messenger

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
                record["rrset_name"] ==  record_name
        ):
            exisiting_external_ip = record["rrset_values"][0]
            break
    if exisiting_external_ip == external_ip:
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
    Messenger(
        "DNS update is successful.\n" +
        f"\n External IP changed from {exisiting_external_ip} to {external_ip}"
    ).sendEmail(
        title="Grandi DNS Update report",
        receiver_email=secrets["email"],
        sender_email=secrets["email"],
        sender_pwd=secrets["email_psd"],
        sender_host=secrets["email_server"],
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
