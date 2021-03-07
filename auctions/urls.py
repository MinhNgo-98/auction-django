from django.urls import path
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add_listing", views.add_listing, name="add_listing"),
    path("add_comment/<int:listing_id>", views.add_comment, name="add_comment"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("all_listings", views.all_listings, name="all_listings"),
    path("add_to_watchlist/<int:listing_id>",
         views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:listing_id>",
         views.remove_from_watchlist, name="remove_from_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("submit_bid/<int:listing_id>", views.submit_bid, name="submit_bid"),
    path("close_bid/<int:listing_id>", views.close_bid, name="close_bid"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category, name="category")
]
