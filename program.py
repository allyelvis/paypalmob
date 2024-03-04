from flask import Flask, request
from paypalrestsdk import Payment, configure

app = Flask(__name__)

# Configure PayPal SDK
configure({
  "mode": "sandbox", # sandbox or live
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET" })

@app.route('/pay', methods=['POST'])
def pay():
    # Extract payment details from mobile money service
    # This part depends on the mobile money service you are using
    payment_details = request.get_json()

    # Create a new PayPal payment
    payment = Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "transactions": [{
            "amount": {
                "total": payment_details['amount'],
                "currency": payment_details['currency']},
            "description": payment_details['description']}],
        "redirect_urls":{
            "return_url":"http://localhost:5000/payment/execute",
            "cancel_url":"http://localhost:5000/payment/cancel"}})

    # Create payment on PayPal
    if payment.create():
        print('Payment created successfully')
    else:
        print(payment.error)

    return 'OK'

if __name__ == '__main__':
    app.run(debug=True)
