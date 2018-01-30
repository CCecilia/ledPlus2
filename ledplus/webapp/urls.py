from django.urls import path

from . import views

app_name = 'webapp'

urlpatterns = [
    path('', views.HtmlRendering.index, name='index'),
    path('dashboard/', views.HtmlRendering.dashboard, name='dashboard'),
    path('sales/new/', views.HtmlRendering.newSale, name='newSale'),
    path('register/', views.UserViews.register, name='register'),
    path('login/', views.UserViews.login, name='login'),
    path('sale/update/', views.SaleViews.update, name='updateSale'),
]
