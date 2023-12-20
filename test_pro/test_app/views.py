import requests
import base64
import hashlib
import json
from django.http import JsonResponse


def initiate_payment(request):
    # Define the URL for the PhonePe API endpoint
    url = "https://api-preprod.phonepe.com/apis/pg-sandbox/pg/v1/pay"

    # Prepare the payload for the request
    payload = {
        "merchantId": "PGTESTPAYUAT",
        "merchantTransactionId": "MT7850590068188104",
        "merchantUserId": "MUID123",
        "amount": 10000,
        "redirectUrl": "https://webhook.site/redirect-url",
        "redirectMode": "REDIRECT",
        "callbackUrl": "https://webhook.site/callback-url",
        "mobileNumber": "9999999999",
        "paymentInstrument": {"type": "PAY_PAGE"},
    }

    # Convert payload to JSON
    json_payload = json.dumps(payload)

    # Base64 encode the payload
    encoded_payload = base64.b64encode(json_payload.encode()).decode()

    # Calculate X-Verify header
    salt_key = "099eb0cd-02cf-4e2a-8aca-3e6c6aff0399"
    salt_index = 1
    combined_string = encoded_payload + "/pg/v1/pay" + salt_key
    hashed_value = hashlib.sha256(combined_string.encode()).hexdigest()
    x_verify_header = hashed_value + "###" + str(salt_index)

    # Prepare headers for the request
    headers = {"Content-Type": "application/json", "X-VERIFY": x_verify_header}

    try:
        # Make a POST request to the PhonePe API
        response = requests.post(
            url, data=json.dumps({"request": encoded_payload}), headers=headers
        )

        # Check the status of the response
        if response.status_code == 200:
            # Successful response
            return JsonResponse(response.json())

        # If the request was not successful, return the response status and text
        return JsonResponse(
            {
                "error": f"Request Failed. Response status: {response.status_code}. Response message: {response.text}"
            },
            status=response.status_code,
        )

    except requests.RequestException as e:
        # Handle exceptions if the request encounters an error
        return JsonResponse({"error": f"Request Exception: {e}"}, status=500)
    return HttpResponse(("Success"))
