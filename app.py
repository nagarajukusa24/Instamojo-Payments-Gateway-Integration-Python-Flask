from flask import Flask, render_template, request,redirect,url_for
from instamojo_wrapper import Instamojo

# API_KEY = "14b253a611b21ca727a1f52777017b5a"
API_KEY = "test_77bff43356a50c5ce9b9ebf1943"
# AUTH_TOKEN = "4a543dfceff4f83b1824210914e689dc"
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

    # print(type(response.text))
    # print(type(res))

    # print(res)
    # return res
    id = res["payment_requests"][0]["id"]

    payment_url = "https://test.instamojo.com/api/1.1/payment-requests/" + id
    res_paymentid = requests.get(payment_url, headers = headers)
    # return payhash
    # print(type(payhash))
    res1 = json.loads(res_paymentid.text)
    # return payment_url
    # payment_id = res1["payment_request"]["payments"]["payment_id"]
    # res2 = res1["payment_request"]

    # print(type(res1))
    # return res1["payment_request"]["payments"]
    # res2 = res1["payment_request"]
    # res3 = json.loads(res2)
    # print(type(res3))

    # return res3
    # return res2

    ##########################Before Verification###########################
    # return res1["payment_request"]["buyer_name"] => Name of the patient
    # return res1["payment_request"]["buyer_email"]
    # return res1["payment_request"]["payments"][0]["created_at"]
    # return res1["payment_request"]["payments"][0]["amount"]   
    # return res1["payment_request"]["payments"][0]["status"]
    # return res1["payment_request"]["payments"][0]["buyer_phone"]
    # return res1["payment_request"]["payments"][0]["payment_id"] => Payment Id : MOJO Captured
    # return payment_id

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
    # return payment_url
    # return resp1["payment_request"]["Payment"][0]["buyer_name"]
    #return resp1["payment_request"]["payment"]["payment_id"] #.payment['payment_id']
    #return resp1["payment_request"]["payment"]["buyer_name"] 
    # return resp1["payment_request"]["payment"]["buyer_phone"]
    # return resp1["payment_request"]["payment"]["buyer_email"]
    # return resp1["payment_request"]["payment"]["amount"] 
    # return resp1["payment_request"]["payment"]["created_at"]   

    apayment_id = resp1["payment_request"]["payment"]["payment_id"]
    apatient_name = resp1["payment_request"]["payment"]["buyer_name"]
    apatient_email = resp1["payment_request"]["payment"]["buyer_email"]
    apatient_phone = resp1["payment_request"]["payment"]["buyer_phone"]
    apatient_amount = resp1["payment_request"]["payment"]["amount"]
    apatient_created = resp1["payment_request"]["payment"]["created_at"]
    ###############################################################

    # print response.text
    # return response.text
    # return response['payment_requests']['id']
    # return response['payment_requests']['longurl']
    return render_template('success.html', 
            apayment_id = apayment_id,
            apatient_name = apatient_name,
            apatient_email = apatient_email,
            apatient_phone = apatient_phone,
            apatient_amount = apatient_amount,
            apatient_created = apatient_created
        )

    # response = api.payment_requests_list()

    # for payment_request in response['payment_requests']:
        # return payment_request['payment_id']
    # return response['payment_request']['id']
    # return response['payment_requests']['payment']['status']

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