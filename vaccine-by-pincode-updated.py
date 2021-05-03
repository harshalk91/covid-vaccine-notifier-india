import requests
import datetime
import notifier
import os
import json

min_age = 18
date = (datetime.datetime.now().date()).strftime("%d-%m-%Y")
api_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/"

temp_list = []
temp_list.clear()
vaccine_by_pincode = []
final_list = []

with open(os.getcwd() + "{}".format("/config.json"), 'r') as receipient_preferences:
    email_pincodes = json.loads(receipient_preferences.read())

for i in email_pincodes.get('preferences'):
    email = i.get("email")
    for pincode in i.get("pincodes"):
        if pincode in temp_list:
            continue
        else:
            temp_list.append(pincode)
            response = requests.get(
                url=api_url + "calendarByPin" + "?pincode={}".format(pincode) + "&date={}".format(date)).json()
            for center in response.get('centers'):
                for session in center.get('sessions'):
                    if session['min_age_limit'] >= min_age: #and session['available_capacity'] > 0:
                        if center['fee_type'] == "Paid":
                            if 'vaccine_fees' in center:
                                for fee_list in center['vaccine_fees']:
                                    vaccine_by_pincode.append("\n <tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td>"
                                                              "<td>{}</td><td>{}</td><td>{}</td><td>{}</td> <td>{}</td></tr>".format(
                                        center['name'],
                                        str(center['pincode']),
                                        center['fee_type'],
                                        str(session['min_age_limit']),
                                        session['vaccine'],
                                        session['date'],
                                        session['available_capacity'],
                                        str(fee_list.get('fee')),
                                        str(session['slots'])))
                            else:
                                vaccine_by_pincode.append("\n <tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td>"
                                                          "<td>{}</td><td>{}</td><td>{}</td><td>{}</td> <td>{}</td></tr>".format(
                                    center['name'],
                                    str(center['pincode']),
                                    center['fee_type'],
                                    str(session['min_age_limit']),
                                    session['vaccine'],
                                    session['date'],
                                    session['available_capacity'],
                                    "Paid",
                                    str(session['slots'])))
                        else:
                            vaccine_by_pincode.append("\n <tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td>"
                                                      "<td>{}</td><td>{}</td><td>{}</td><td>{}</td> <td>{}</td></tr>".format(
                                center['name'],
                                str(center['pincode']),
                                center['fee_type'],
                                str(session['min_age_limit']),
                                session['vaccine'],
                                session['date'],
                                session['available_capacity'],
                                "Free",
                                str(session['slots'])))

    if not vaccine_by_pincode:
        print("No vaccination centers available")
    else:
        final_list.append({
            "email": i.get('email'),
            "centers": vaccine_by_pincode
        })

if not vaccine_by_pincode:
    print("No vaccination Centers available in your area")
else:
    for data in final_list:
        print("sending email to {}".format(data['email']))
        notifier.send_message(vaccine_details=data['centers'], receiver_email=data['email'])

vaccine_by_pincode.clear()
final_list.clear()
