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
    path('register/', views.UserViews.register, name='register'),
    path('login/', views.UserViews.login, name='login'),
    path('logout/', views.UserViews.logout, name='logout'),
    path('sale/update/', views.SaleViews.update, name='updateSale'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
