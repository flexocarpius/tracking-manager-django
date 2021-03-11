from django import forms


class ProductForm(forms.Form):
    product_id = forms.IntegerField(required=False)
    name = forms.CharField(label='Product name', max_length=100)
    description = forms.CharField(label='Product description', max_length=500)
    price = forms.FloatField(label='Product price')
    quantity = forms.IntegerField(label='Product quantity')
    small_img = forms.CharField(
        label='Small image', max_length=500, required=False)
    large_img = forms.CharField(
        label='Small image', max_length=500, required=False)
