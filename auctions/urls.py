from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),   #active listings
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    #path("active", views.active, name="active"),
    path("create", views.create, name="create"),   #create listing
    path("listing/<int:pk>/", views.listing, name="listing"), #listing page
    path("categories", views.categories,name="categories" ), #categories
    path("category/<str:category_name>/", views.category,name="category" ), #category
    path('handle_form1/<int:pk>/', views.handle_form1, name='handle_form1'),
    path('handle_form2/<int:pk>/', views.handle_form2, name='handle_form2'),
    path('handle_watchlist/<int:pk>/', views.handle_watchlist, name='handle_watchlist'),
    path("watchlist", views.watchlist, name="watchlist"), #watchlist
   
]
