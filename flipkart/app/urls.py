from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("req_password/", views.req_password, name="req_password"),
    path("reset_password/<uemail>/", views.reset_password, name="reset_password"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("searchproduct/", views.searchproduct, name="searchproduct"),
    path("electronics_search/", views.electronics_search, name="electronics_search"),
    path("cloths_search/", views.cloths_search, name="cloths_search"),
    path("shoes_search/", views.shoes_search, name="shoes_search"),
    path("serchby_pricerange/", views.serchby_pricerange, name="serchby_pricerange"),
    path("productdetails/<int:productid>", views.productdetails, name="productdetails"),
    path("showcarts/", views.showcarts, name="showcarts"),
    path("addtocart/<productid>/", views.addtocart, name="addtocart"),
    path("removecart/<productid>/", views.removecart, name="removecart"),
    path("updateqty/<int:qv>/<productid>", views.updateqty, name="updateqty"),
    path("checkout_single/<int:productid>", views.checkout_single, name="checkout_single"),
    path("checkout/", views.checkout, name="checkout"),
    path("addprofile/", views.addprofile, name="addprofile"),
    path("addaddress/", views.addaddress, name="addaddress"),
    path('add_to_wishlist/<int:productid>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('removefromwishlist/<int:productid>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('view_wishlist/', views.view_wishlist, name='view_wishlist'),
]
