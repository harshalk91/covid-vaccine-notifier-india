import requests
import datetime
import notifier

state_id = 21
district_id = 363
min_age = 18
date = (datetime.datetime.now().date()).strftime("%d-%m-%Y")
api_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/"
RECEIVER_EMAILS = ['harshalk.91@gmail.com', 'harshal.kulkarni91@gmail.com']
vaccine_by_district = []

response = requests.get(
    url=api_url + "calendarByDistrict" + "?district_id={}".format(district_id) + "&date={}".format(date)).json()
for center in response.get('centers'):
    for session in center.get('sessions'):
        if session['min_age_limit'] == min_age:
            if center['fee_type'] == "Paid":
                if 'vaccine_fees' in center:
                    for fee_list in center['vaccine_fees']:
                        vaccine_by_district.append("\n <tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td>"
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
                vaccine_by_district.append("\n <tr> <td>{}</td>  <td>{}</td>  <td>{}</td>  <td>{}</td>  "
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
    notifier.send_message(vaccine_details=vaccine_by_district, receiver_email=receiver)
