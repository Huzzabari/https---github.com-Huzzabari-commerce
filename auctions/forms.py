from django import forms

class AuctionForm(forms.Form):
    title=forms.CharField(label='title', max_length=30)
    description=forms.CharField(label='description', max_length=130, widget=forms.Textarea)
    starting_bid=forms.DecimalField()
    image_url=forms.CharField(label='image url', max_length=500)
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