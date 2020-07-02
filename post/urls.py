from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='home'),
    path('signup/',views.signUp,name='signup'),
    path('createblog/',views.createblog,name='createblog'),
    path('showblogs/',views.showblogs,name='blogs'),
    path('myblogs/',views.myblogs,name='myblogs'),
    path('logout/',views.logout_view,name='logout')

]