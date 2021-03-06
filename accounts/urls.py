from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.registerPage, name='register'),

    path('user/', views.userPage, name='user-page'),
    path('products/', views.products, name='products'),
    path('customers/<str:pk_test>/', views.customers, name='customers'),

    path('account/', views.accountSettings, name='account'),

    path('create_order/<str:pk>/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>/', views.deleteOrder, name='delete_order')
]
