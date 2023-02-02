import vonage


def send_sms(code, tel_number):
    print('working')
    client = vonage.Client(key="606ee033", secret="NyQK2dQVq70kCHgb")
    client.sms.send_message({
        "from": "Vonage APIs",
        "to": tel_number,
        "text": "Your code is %04d" % code,
    })
