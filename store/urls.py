from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.loginPage.as_view(), name="login"),
    path("logout/", views.logoutUser.as_view(), name="logout"),
    path("register/", views.registerPage.as_view(), name="register"),
    path("", views.store, name="store"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("add-item/<str:pk>", views.addItem, name="add-item"),
    path("remove-item/<str:pk>", views.removeItem, name="remove-item"),
    path('search_view/', views.search_view, name='search_view'),
]
