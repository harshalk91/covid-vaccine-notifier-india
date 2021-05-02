import requests
from prettytable import PrettyTable
import datetime

min_age = 18
pincode = "530001"
date = date = (datetime.datetime.now().date()).strftime("%d-%m-%Y")
api_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/"

t = PrettyTable(['Name', 'Pincode', 'Free/Paid', 'min_age_limit', 'vaccine', 'date', 'available_capacity', 'fees'])

response = requests.get(url=api_url + "calendarByPin" + "?pincode={}".format(pincode) + "&date={}".format(date)).json()
for center in response.get('centers'):
    for session in center.get('sessions'):
        if session['min_age_limit'] == 18:
            if center['fee_type'] == "Paid":
                if 'vaccine_fees' in center:
                    for fee_list in center['vaccine_fees']:
                        t.add_row(
                            [center['name'], str(center['pincode']), center['fee_type'], str(session['min_age_limit']),
                             session['vaccine'],
                             session['date'], session['available_capacity'], str(fee_list.get('fee'))])

            else:
                t.add_row([center['name'], str(center['pincode']), center['fee_type'], str(session['min_age_limit']),
                           session['vaccine'],
                           session['date'], session['available_capacity'], "Free"])

print(t)
t.clear()