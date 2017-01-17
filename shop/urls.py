from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^cart$', views.ShowCartView.as_view(), name='cart'),
    url(r'^subscription_cart$', views.ShowSubscriptionCartView.as_view(), name='subscription_cart'),
    url(r'^checkout$', views.CheckoutView.as_view(), name='checkout'),
    url(r'^subscribe', views.SubscribeView.as_view(), name='subscribe'),
]
