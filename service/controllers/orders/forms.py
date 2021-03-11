from django import forms


class OrderForm(forms.Form):
    order_id = forms.IntegerField()
    shipping_address = forms.CharField(max_length=50)
