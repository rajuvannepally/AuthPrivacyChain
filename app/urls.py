from django.urls import path
from . import views
from django.conf.urls import url
urlpatterns = [
path('',views.user_login,name="user_login"),
path('register/',views.register,name="register"),
path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
path('logout/', views.logout, name='logout'),
path('aditor_login/',views.aditor_login,name="aditor_login"),
path('aditor_logout/', views.aditor_logout, name='aditor_logout'),
path('dashboard/', views.dashboard, name='dashboard'),
path('upload_file/', views.upload_file, name='upload_file'),
path('cloud_login/', views.cloud_login, name='cloud_login'),
path('cloud_dashboard/', views.cloud_dashboard, name='cloud_dashboard'),
path('clogout/', views.clogout, name='clogout'),
path('files/', views.files, name='files'),
path('user_detail/', views.user_detail, name='user_detail'),
path('send_cloud/', views.send_cloud, name='send_cloud'),
path('upload/<int:pk>', views.upload, name='upload'),
path('up_files/', views.up_files, name='up_files'),
path('cloud_files/', views.cloud_files, name='cloud_files'),
path('download_file/<int:pk>', views.download_file, name='download_file'),
path('chart/', views.chart, name='chart'),
url(r'^ajax/chart_ajax/$', views.chart_ajax, name='chart_ajax'),
]