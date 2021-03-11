from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersGetRequest
from paypalcheckoutsdk.payments import CapturesRefundRequest, CapturesGetRequest


client_id = 'AaxEQsFlC-UPhukx6A3QBUrEmTCMT_OStCz4F5hX-wNV6n1ebfKHhXZDeDH-x66FKRcvqp5XDHjiVyDV'
client_secret = 'EEiAjkIl6KKlknQ5Ss9R8856pdsg3kpPh6lNOIiDkvBerIidNs1sZloXBAOOKrtN0MgzWWyqtEaO2c-h'


class OrdersBusiness():
    def __init__(self):
        # Creating an environment
        self.environment = SandboxEnvironment(
            client_id=client_id,
            client_secret=client_secret
        )
        self.client = PayPalHttpClient(self.environment)

    def is_order_valid(self, total, order_id):
        try:
            request = OrdersGetRequest(order_id)
            response = self.client.execute(request)

            if response is not None \
                    and response.result.status == 'COMPLETED' \
                    and len(response.result.purchase_units) > 0 \
                    and float(response.result.purchase_units[0].amount.value) == total:
                return True

            return False
        except Exception:
            return False

    def is_payment_valid(self, total, paypal_order_id):
        try:
            request = CapturesGetRequest(paypal_order_id)
            response = self.client.execute(request)

            if response is not None and (response.result.status == 'COMPLETED' or response.result.status == 'REFUNDED'):
                return True

            return False
        except Exception:
            return False

    def get_transaction_from_capture(self, paypal_order_id):
        request = OrdersGetRequest(paypal_order_id)
        response = self.client.execute(request)

        if response:
            return response.result.purchase_units[0].payments.captures[0].id

    def refund_payment(self, transaction_id):
        request = CapturesRefundRequest(transaction_id)
        response = self.client.execute(request)

        if response is not None and response.result.status == 'COMPLETED':
            return True

        return False
