from django.urls import path
from product.views import Home,ProductDetail,AddCart,ShowCart,update_cart_quantity,remove_from_cart,Shop,VegFruit,GrainOil,DairyProduct,ContactUs,cart

urlpatterns = [
    path('',Home,name="Home"),
    path('shop/',Shop,name="shop"),
    path('vege-fruit/',VegFruit,name='vege_fruit'),
    path('grain-oil/',GrainOil,name='grain_oil'),
    path('dairy-product/',DairyProduct,name='dairyproduct'),
    path('contact-us/',ContactUs,name='contactus'),
    path('details/<int:pk>',ProductDetail.as_view(),name="Detail"),

    # path('add-to-cart/<int:product_id>/',AddCart,name="Add_Cart"),
    # path('cart/',cart,name="Show_Cart"),


    ## new code :

    path('add-to-cart/<int:product_id>/', AddCart, name="Add_Cart"),
    path('cart/', cart, name="Show_Cart"),





    path('update-cart/<int:cart_id>/', update_cart_quantity, name='update_cart_quantity'),
    path('remove-from-cart/<int:cart_id>/',remove_from_cart, name='remove_from_cart'),
   
]