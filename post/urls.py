from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='home'),
    path('signup/',views.signUp,name='signup'),
    path('createblog/',views.createblog,name='createblog'),
    path('showblogs/',views.showblogs,name='blogs'),
    path('myblogs/',views.myblogs,name='myblogs'),
    path('addcomment/<int:id>/',views.addcomment,name='addcomment'),
    path('details/<int:id>',views.detail_view,name='details'),
    path('like/<int:id>',views.like_view,name='like'),
    path('dislike/<int:id>',views.dislike_view,name='dislike'),
    path('modify/<int:id>',views.modify_view,name='modify_view'),
    path('modified/',views.modified,name='modified'),
    path('quick_view/',views.quick_view,name='quick_view'),
    path('historybyblog/<int:id>',views.historybyblog_view,name='historybyblog_view'),
    path('historybyauth/<str:data>',views.historybyauth_view,name='historybyauth_view'),
    path('logout/',views.logout_view,name='logout')

]