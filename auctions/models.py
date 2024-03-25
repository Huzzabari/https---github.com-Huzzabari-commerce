from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
#Your application should have at least three models in addition to the User model: one for auction listings, one for bids, and one for comments made on auction listings. 


class Category(models.Model):                              # category model I add to the auction form
    CATEGORY_CHOICES=[  
    ('Electronics', 'Electronics'),
    ('Clothing', 'Clothing'),
    ('Home & Garden', 'Home & Garden'),
    ('Toys & Games', 'Toys & Games'),
    ('Books & Magazines', 'Books & Magazines'),
    ('Sports & Outdoors', 'Sports & Outdoors'),
    ('Health & Beauty', 'Health & Beauty'),
    ('Collectibles', 'Collectibles'),
    ('Automotive', 'Automotive'),
    ('Miscellaneous', 'Miscellaneous')]
    name = models.CharField(max_length=30, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"Category:{self.name}"
#auction categories
    
class Auction(models.Model):
    title=models.CharField(max_length=30)  #title
    description=models.CharField(max_length=130)  #description
    starting_bid=models.PositiveIntegerField()  #starting bid
    highest_bid=models.PositiveBigIntegerField(default=0) #highest bid with defaults set to 0, so less thatn starting bid
    image_url=models.URLField(blank=True)   #image
    is_open=models.BooleanField(default=True)   #is the auction open or closed
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True) #category drop down
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  #links the user to the auction created


    def __str__(self):
        return f"ID: {self.id}, Title:{self.title}, Description:{self.description}, with a starting bid of {self.starting_bid}, a highest bid of {self.highest_bid}, an image url of {self.image_url}, and category:{self.category}"
#auction listings

class Bids(models.Model):                                                                                       # bid model that includes auction foreign key that links to auction id, bids, and user id
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bids=models.PositiveIntegerField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Auction:{self.auction} and Bids:{self.bids} from User:{self.user}"
#bids
    
class Comments(models.Model):                                                                           # comment model has auction id, comments, and user id
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    comments=models.CharField(max_length=130)
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Auction:{self.auction} and Comments:{self.comments} from User:{self.user}"
#comments


class UserProfile(models.Model):   #user profile model has the user id and then the watchlist                              
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    watchlist=models.ManyToManyField(Auction, blank=True)
    # your additional fields here
