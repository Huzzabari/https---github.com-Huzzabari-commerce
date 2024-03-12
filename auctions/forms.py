from django import forms

class AuctionForm(forms.Form):
    title=forms.CharField(label='title', max_length=30)
    description=forms.CharField(label='description', max_length=130)
    starting_bid=forms.DecimalField()
    image_url=forms.CharField(label='image url', max_length=500)
    category=forms.CharField(label='category', max_length=30)