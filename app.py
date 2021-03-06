from flask import Flask, render_template, request,redirect,url_for
from instamojo_wrapper import Instamojo

# API_KEY = "INSERT API KEYS HERE"
API_KEY = "test_77bff43356a50c5ce9b9ebf1943"
# AUTH_TOKEN = "INSERT AUTH KEYS"
AUTH_TOKEN = "test_d07e27b5dcb0a5ca5eeffb30efb"
api = Instamojo(api_key=API_KEY,auth_token=AUTH_TOKEN,endpoint='https://test.instamojo.com/api/1.1/') #endpoint='https://test.instamojo.com/api/1.1/'

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/success')
def success():
    import requests

    headers = { "X-Api-Key": "test_77bff43356a50c5ce9b9ebf1943", "X-Auth-Token": "test_d07e27b5dcb0a5ca5eeffb30efb"}

    response = requests.get("https://test.instamojo.com/api/1.1/payment-requests/", headers=headers)

    import json

    res=json.loads(response.text)
    id = res["payment_requests"][0]["id"]

    payment_url = "https://test.instamojo.com/api/1.1/payment-requests/" + id
    res_paymentid = requests.get(payment_url, headers = headers)
    res1 = json.loads(res_paymentid.text)


    ##########################Before Verification###########################


    bpayment_id = res1["payment_request"]["payments"][0]["payment_id"]
    bpatient_name = res1["payment_request"]["payments"][0]["buyer_name"]
    bpatient_email = res1["payment_request"]["payments"][0]["buyer_email"]
    bpatient_phone = res1["payment_request"]["payments"][0]["buyer_phone"]
    bpatient_amount = res1["payment_request"]["payments"][0]["amount"]  
    bpatient_status = res1["payment_request"]["payments"][0]["status"]
    bpatinet_created = res1["payment_request"]["payments"][0]["created_at"]
    ###########################End of Payment Details##################

    ################Verification payment####################
    payment_id = res1["payment_request"]["payments"][0]["payment_id"]
    payment_url = payment_url + "/" + payment_id
    resp = requests.get(payment_url, headers=headers)
    resp1 = json.loads(resp.text)

    apayment_id = resp1["payment_request"]["payment"]["payment_id"]
    apatient_name = resp1["payment_request"]["payment"]["buyer_name"]
    apatient_email = resp1["payment_request"]["payment"]["buyer_email"]
    apatient_phone = resp1["payment_request"]["payment"]["buyer_phone"]
    apatient_amount = resp1["payment_request"]["payment"]["amount"]
    apatient_created = resp1["payment_request"]["payment"]["created_at"]
    ###############################################################


    return render_template('success.html', 
            apayment_id = apayment_id,
            apatient_name = apatient_name,
            apatient_email = apatient_email,
            apatient_phone = apatient_phone,
            apatient_amount = apatient_amount,
            apatient_created = apatient_created
        )

@app.route('/pay',methods=['POST','GET'])
def pay():
    if request.method == 'POST':
        name = request.form.get('name')
        purpose = request.form.get('purpose')
        email = request.form.get('email')
        amount = request.form.get('amount')        
        response = api.payment_request_create(
        amount=amount,
        purpose=purpose,
        buyer_name=name,
        send_email=True,
        email=email,
        # payid = response['payment_request']['id'],
        # redirect_url=("http://localhost:5000/success",payid=payid)
        # redirect(url_for('/success', payid='payid'))
        redirect_url="http://localhost:5000/success"  
        )
        # print(payid)/
        return redirect(response['payment_request']['longurl'])     
    else:      
        return redirect('/')

    
if __name__ == '__main__':
   app.run(debug=True)
