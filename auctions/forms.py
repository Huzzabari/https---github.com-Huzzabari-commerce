from django import forms

class AuctionForm(forms.Form):                                                                          # auctionform contains a title
    title=forms.CharField(label='Title', max_length=30)
    description=forms.CharField(label='Description', max_length=130, widget=forms.Textarea)             # description that is turned into a textarea for the user
    starting_bid=forms.DecimalField()                                                                   # starting bid
    image_url=forms.CharField(label='Image url', max_length=500)                                        # image_url
    category=forms.ChoiceField(choices=[                                                                # choice of categories
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
    auction_id = forms.IntegerField(widget=forms.HiddenInput())                              # auction id that is hidden and is an int field
    comments=forms.CharField(label="Comment", max_length=130, widget=forms.Textarea)         # comments that are turned into a textarea field 
    user=forms.IntegerField(widget=forms.HiddenInput())                                       # user id that is hidden

class BidForm(forms.Form):
    auction_id = forms.IntegerField(widget=forms.HiddenInput())                            # auction id that is hidden and is an int field  
    new_bid=forms.DecimalField()                                                            # new bid the user is putting into the form
    user=forms.IntegerField(widget=forms.HiddenInput())                                    # user id that is hidden

class WatchForm(forms.Form):
    auction_id = forms.IntegerField(widget=forms.HiddenInput())                            # auction id that is hidden and is an int field                                                            # new bid the user is putting into the form
    