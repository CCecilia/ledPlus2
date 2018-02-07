from django.conf.urls.static import static
from django.conf import settings
from django.urls import path

from . import views

app_name = 'webapp'

urlpatterns = [
    path('', views.HtmlRendering.index, name='index'),
    path('dashboard/', views.HtmlRendering.dashboard, name='dashboard'),
    path('sale/new/', views.HtmlRendering.newSale, name='newSale'),
    path('sale/all/', views.HtmlRendering.sales, name='sales'),
    path('sale/<int:sale_id>/details/', views.HtmlRendering.saleDetails, name='saleDetails'),
    path('sale/<int:sale_id>/edit/', views.HtmlRendering.saleEdit, name='saleEdit'),
    path('register/', views.UserViews.register, name='register'),
    path('login/', views.UserViews.login, name='login'),
    path('logout/', views.UserViews.logout, name='logout'),
    path('sale/update/', views.SaleViews.update, name='updateSale'),
    path('sale/upload/image/', views.SaleViews.uploadBillImage, name='uploadBillImage'),
    path('sale/get/data/', views.SaleViews.getData, name='getData'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
