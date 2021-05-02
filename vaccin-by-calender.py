import requests
from prettytable import PrettyTable


pincode = "110044"
date = "03-05-2021"
api_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/"


t = PrettyTable(['Name', 'Pincode', 'Free/Paid', 'min_age_limit', 'vaccine', 'date', 'fees'])

resp = requests.get(url=api_url + "calendarByPin" + "?pincode={}".format(pincode) + "&date={}".format(date)).json()
for i in resp.get('centers'):
    for j in i.get('sessions'):
        if i['fee_type'] == "Paid":
            if 'vaccine_fees' in i:
                for k in i['vaccine_fees']:
                    t.add_row([i['name'], str(i['pincode']), i['fee_type'], str(j['min_age_limit']), j['vaccine'],
                               j['date'], str(k.get('fee'))])

        else:
            t.add_row([i['name'], str(i['pincode']), i['fee_type'], str(j['min_age_limit']), j['vaccine'],
                       j['date'], "Free"])

print(t)