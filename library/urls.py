from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('register/', views.register, name='register'),
    path('wel/', views.wel, name='wel'),
    path('profile/', views.profile, name='profile'),
    path('base/', views.base, name='base'),
    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('adminpage/', views.adminpage, name='adminpage'),
    path('adminlogout/', views.adminlogout, name='adminlogout'),
    path('newadmin/', views.newadmin, name='newadmin'),
    path('addbook/', views.addbook, name='addbook'),
    path('removebook/', views.removebook, name='removebook'),
    path('editbook/', views.editbook, name='editbook'),
    path('notice/', views.notice, name='notice'),
    path('studentaddbook/', views.studentaddbook, name='studentaddbook'),
    path('bookissue/', views.bookissue, name='bookissue'),
    path('issuedbook/', views.issuedbook, name='issuedbook'),
    path('returnbook/', views.returnbook, name='returnbook'),
    path('requestbook/', views.requestbook, name='requestbook'),
    path('booklist/', views.booklist, name='booklist'),
    path('removebynumber/', views.removebynumber, name='removebynumber'),
    path('deletebynumber/', views.deletebynumber, name='deletebynumber'),
    path('deletepost/', views.deletepost, name='deletepost'),
    path('deletepostbypopup/', views.deletepostbypopup, name='deletepostbypopup'),
    path('verifyrequest/', views.verifyrequest, name='verifyrequest'),
    path('studentrequest/', views.studentrequest, name='studentrequest'),
    path('statusrequest/', views.statusrequest, name='statusrequest'),
    path('deleterequest/', views.deleterequest, name='deleterequest'),
    path('payfine/', views.payfine, name='payfine'),


    ]