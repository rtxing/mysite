import requests
from mysite import settings

def send_otp(mobile, otp):
    """
    Send OTP via SMS.
    """
    url = f"https://2factor.in/API/V1/ccdd7d9d-42b5-11ef-8b60-0200cd936042/SMS/+91" + str(mobile) + "/"+  str(otp) + "/"
    payload = ""
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.get(url, data=payload, headers=headers)
    print(response.content)
    return bool(response.ok)