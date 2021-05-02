from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, BaseLoader
import smtplib
import os

SENDER_EMAIL = os.environ.get('sender_email')
SENDER_PASSWORD = os.environ.get('sender_password')
SERVER = os.environ.get('smtp_server')

SUBJECT = 'Vaccination Details'
HTML = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <style type="text/css">
      table {
        background: white;
        border-radius:3px;
        border-collapse: collapse;
        height: auto;
        max-width: 900px;
        padding:5px;
        width: auto;
        animation: float 5s infinite;
      }
      th {
        color:#D5DDE5;;
        background:#1b1e24;
        border-bottom: 4px solid #9ea7af;
        font-size:14px;
        font-weight: 300;
        padding:10px;
        width: auto;
        text-align:center;
        vertical-align:middle;
      }
      tr {
        border-top: 1px solid #C1C3D1;
        border-bottom: 1px solid #C1C3D1;
        border-left: 1px solid #C1C3D1;
        color:#666B85;
        font-size:16px;
        font-weight:normal;
      }
      tr:hover td {
        background:#4E5066;
        color:#FFFFFF;
        border-top: 1px solid #22262e;
      }
      td {
        background:#FFFFFF;
        padding:10px;
        text-align:left;
        vertical-align:middle;
        font-weight:300;
        font-size:13px;
        border-right: 1px solid #C1C3D1;
      }
    </style>
  </head>
  <body>
    Hi,<br> <br>
    Here is the list vaccination centers in your district<br><br>
    <table>
      <thead>
        <tr style="border: 1px solid #1b1e24;">
          <th>Name</th>
          <th>Pincode</th>
          <th>Free/Paid</th>
          <th>Min Age Limit</th>
          <th>Vaccine</th>
          <th>Date</th>
          <th>Available Capacity</th>
          <th>Fees</th>
          <th>Slots</th>
        </tr>
      </thead>
      <tbody>
      {% for error_details in errors %}
          {{ error_details }}
      {% endfor %}
      </tbody>
    </table>
    <br>
    <a href='mailto:harshalk.91@gmail.com'>harshalk.91@gmail.com</a>.<br> <br>
    Thank you!
  </body>
</html>
"""


def _generate_message(html_out, receiver_email) -> MIMEMultipart:
    message = MIMEMultipart("alternative", None, [MIMEText(html_out, 'html')])
    message['Subject'] = SUBJECT
    message['From'] = SENDER_EMAIL
    message['To'] = receiver_email
    return message


# Sending email
def send_message(vaccine_details, receiver_email):
    template = Environment(loader=BaseLoader).from_string(HTML)
    template_vars = {"errors": vaccine_details}
    html_out = template.render(template_vars)
    message = _generate_message(html_out, receiver_email)
    server = smtplib.SMTP(SERVER)
    server.ehlo()
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
    server.quit()