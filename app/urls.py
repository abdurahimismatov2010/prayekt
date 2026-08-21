from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('mahsulot/', views.mahsulot, name='mahsulot'),
    path('blog/', views.blog, name='blog'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('savat/', views.svat, name='savat'),
    path('detail/<int:pk>/', views.mahsulot_detail, name='form'),
    path('c_p/', views.c_p, name='c'),
    path('f_p/', views.f_p, name='f'),
    path('r_p/', views.r_p, name='r'),
]