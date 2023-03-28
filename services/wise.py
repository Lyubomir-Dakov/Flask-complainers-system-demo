import requests
from decouple import config
from uuid import uuid4

TARGET_CURRENCY = "BGN"


class WiseService:
    def __init__(self):
        self.base_url = config("WISE_URL")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config('WISE_TOKEN')}",
        }
        self.profile_id = config("WISE_PROFILE_ID")

    def create_quote(self, amount):
        url = f"{self.base_url}/v3/profiles/{self.profile_id}/quotes"
        body = {
            "sourceCurrency": "EUR",
            "targetCurrency": TARGET_CURRENCY,
            "sourceAmount": amount,
        }

        response = requests.post(url, json=body, headers=self.headers)
        return response.json()["id"]

    def create_recipient(self, full_name, iban):
        url = f"{self.base_url}/v1/accounts"
        body = {
            "currency": TARGET_CURRENCY,
            "type": "IBAN",
            "profile": self.profile_id,
            "ownedByCustomer": True,
            "accountHolderName": full_name,
            "details": {
                "legalType": "PRIVATE",
                "iban": iban
            }
        }
        response = requests.post(url, json=body, headers=self.headers)
        return response.json()["id"]

    def create_transfer(self, recipient_account_id, quote_id, custom_transaction_id):
        url = f"{self.base_url}/v1/transfers"
        body = {
            "targetAccount": recipient_account_id,
            "quoteUuid": quote_id,
            "customerTransactionId": custom_transaction_id,
            "details": {}
        }
        response = requests.post(url, json=body, headers=self.headers)
        return response.json()["id"]

    def fund_transfer(self, transfer_id):
        url = f"{self.base_url}/v3/profiles/{self.profile_id}/transfers/{transfer_id}/payments"
        body = {"type": "BALANCE"}
        response = requests.post(url, json=body, headers=self.headers)
        return response.json()

    def cancel_transfer(self, transfer_id):
        url = f"{self.base_url}/v1/transfers/{transfer_id}/cancel"
        response = requests.put(url, json={}, headers=self.headers)
        return response.json()


# if __name__ == "__main__":
#     service = WiseService()
#     # quote_id = service.create_quote(200)
#     # recipient_account_id = service.create_recipient("Lubo Test", "BG80BNBG96611020345678")
#     # custom_transaction_id = str(uuid4())
#     # transfer_id = service.create_transfer(recipient_account_id, quote_id, custom_transaction_id)
#     # completed_transfer = service.fund_transfer(transfer_id)
#     canceled_transfer = service.cancel_transfer(51801554)
#
#     # print(quote_id)
#     # print(recipient_account_id)
#     # print(transfer_id)
#     # print(completed_transfer)
