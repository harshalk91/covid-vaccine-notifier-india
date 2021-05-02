import requests
from prettytable import PrettyTable
import datetime
import notifier

min_age = 18
pincodes = ["411001", "411011", "411030", "411058", "411038", "411052"]
date = (datetime.datetime.now().date()).strftime("%d-%m-%Y")
api_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/"
RECEIVER_EMAILS = ['harshalk.91@gmail.com', 'harshal.kulkarni1991@gmail.com']
vaccine_by_pincode = []

for pincode in pincodes:
    response = requests.get(
        url=api_url + "calendarByPin" + "?pincode={}".format(pincode) + "&date={}".format(date)).json()
    for center in response.get('centers'):
        for session in center.get('sessions'):
            if session['min_age_limit'] == min_age:
                if center['fee_type'] == "Paid":
                    if 'vaccine_fees' in center:
                        for fee_list in center['vaccine_fees']:
                            vaccine_by_pincode.append("\n <tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td>"
                                                      "<td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr> ".format(
                                center['name'],
                                str(center['pincode']),
                                center['fee_type'],
                                str(session['min_age_limit']),
                                session['vaccine'],
                                session['date'],
                                session['available_capacity'],
                                str(fee_list.get('fee'))))

                else:
                    vaccine_by_pincode.append("\n <tr> <td>{}</td>  <td>{}</td>  <td>{}</td>  <td>{}</td>  "
                                              "<td>{}</td>  <td>{}</td>  <td>{}</td>  <td>{}</td>  </tr> ".format(
                        center['name'],
                        str(center['pincode']),
                        center['fee_type'],
                        str(session['min_age_limit']),
                        session['vaccine'],
                        session['date'],
                        session['available_capacity'],
                        "Free"))


for receiver in RECEIVER_EMAILS:
    notifier.send_message(vaccine_details=vaccine_by_pincode, receiver_email=receiver)

'''
for center in response.get('centers'):
    for session in center.get('sessions'):
        if session['min_age_limit'] >= 18:
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
'''