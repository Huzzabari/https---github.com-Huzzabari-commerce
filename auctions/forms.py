from django import forms

class AuctionForm(forms.Form):
    title=forms.CharField(label='Title', max_length=30)
    description=forms.CharField(label='Description', max_length=130, widget=forms.Textarea)
    starting_bid=forms.DecimalField()
    image_url=forms.CharField(label='Image url', max_length=500)
    category=forms.ChoiceField(choices=[  
    ('Electronics', 'Electronics'),
    ('Clothing', 'Clothing'),
    ('Home & Garden', 'Home & Garden'),
    ('Toys & Games', 'Toys & Games'),
    ('Books & Magazines', 'Books & Magazines'),
    ('Sports & Outdoors', 'Sports & Outdoors'),
    ('Health & Beauty', 'Health & Beauty'),
    ('Collectibles', 'Collectibles'),
    ('Automotive', 'Automotive'),
    ('Miscellaneous', 'Miscellaneous')])


class CommentForm(forms.Form):
    auction_id = forms.IntegerField(widget=forms.HiddenInput())
    comments=forms.CharField(label="Comment", max_length=130, widget=forms.Textarea)
    user=forms.IntegerField(widget=forms.HiddenInput())

class BidForm(forms.Form):
    auction_id = forms.IntegerField(widget=forms.HiddenInput())
    new_bid=forms.DecimalField()
    user=forms.IntegerField(widget=forms.HiddenInput())