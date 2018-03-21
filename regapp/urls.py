from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import(our, signup, login_view, logout_view, update_profile, change_password, view_profile, account_activation_sent, activate)
from django.contrib.auth.views import(
    password_reset, password_reset_done, password_reset_confirm, password_reset_complete)
    
urlpatterns = [
    #url(r'^$', views.index, name='index'),
    #url(r'^register_user/$', views.UserFormView.as_view(), name='UserForm'),
    url(r'^$', our, name='our'),
    url(r'^signup/$', signup, name='signup'),
    url(r'^updateProfile/$', update_profile, name='update_profile'),
    url(r'^change-password/$', change_password, name='change_password'),
    url(r'^profile/$', view_profile, name='view_profile'),
    url(r'^login/$', login_view, name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^reset-password/$', password_reset, name='password_reset'),
    url(r'^reset-password/done$', password_reset_done, name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset-password/complete$', password_reset_complete, name='password_reset_complete'),
    url(r'^account_activation_sent/$', account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[a-zA-Z0-9\-_]+?\.[a-zA-Z0-9\-_]+?\.([a-zA-Z0-9\-_]+))/$',
        activate, name='activate'),
   # url(r'^addcart/(?P<product_id>\d+)/(?P<user_id>\d+)/$', add_cart, name='add_cart'),
   # url(r'^viewcart/$', view_cart, name='view_cart'),
    #url(r'^removeitem/(?P<item_id>\d+)/$', remove_item, name='remove_item'),
    
    
    
]   
