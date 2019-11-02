import requests, json

"""
very simple dynamic DNS using cloudflare's API
api doc: https://api.cloudflare.com/ 

the script checks your current ip, if it does not match with the A record it will change it

"""

ext_ip = requests.get('https://api.ipify.org').text # gets your current IP address

auth_key = '<auth key>' # add your auth key, you need to generate it
zone_id = '<zone id>' # add your zone ID, you can find it in your account overview
record_id = '<dns record id>' # add your dns record ID, you can find it using check_ip_addr func

headers = {
    'X-Auth-Email': '<account email>',
    'X-Auth-Key': auth_key,
    'Content-Type': 'application/json',
}


def edit_dns_record():
    record_data = {"type": "A", "name": "@", "content": ext_ip, "ttl": 1, "proxied": True}
    data = json.dumps(record_data)

    response = json.loads(
        requests.put(f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}', headers=headers,
                     data=data).text)
    if response['success']:
        return True
    else:
        return response


def check_ip_addr():
    params = (
        ('type', 'A'),
        ('name', '<domain name>'), # add your domain name here
        ('page', '1')
    )

    response = json.loads(
        requests.get(f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records', headers=headers,
                     params=params).text)
    return response['result'][0]['content']


if not check_ip_addr() == ext_ip:
    print(edit_dns_record())

