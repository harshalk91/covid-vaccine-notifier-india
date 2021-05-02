import requests
from prettytable import PrettyTable
import datetime

state_id = 21
district_id = 363
min_age = 18
date = date = (datetime.datetime.now().date()).strftime("%d-%m-%Y")
api_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/"

t = PrettyTable(['Name', 'Pincode', 'Free/Paid', 'min_age_limit', 'vaccine', 'date', 'available_capacity', 'fees'])

response = requests.get(url=api_url + "calendarByDistrict" + "?district_id={}".format(district_id) + "&date={}".format(date)).json()
for center in response.get('centers'):
    for session in center.get('sessions'):
        if session['min_age_limit'] == 45:
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