from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register, name="register"),

    path('my_profile', views.my_profile, name="my_profile"),

    path('activity', views.activity, name='get_activity'),

    path('edit_profile', views.edit_profile, name="edit_profile"),
    path('edit_profile_picture', views.edit_profile_picture, name="edit_profile_picture"),
    path('make_post', views.make_post, name="make_post"),


    path('unlike/<int:post_id>', views.unlike, name="unlike"),
    path('like/<int:post_id>', views.like, name="like"),

    path('my_profile/unlike/<int:post_id>', views.unlike, name="unlike"),
    path('my_profile/like/<int:post_id>', views.like, name="like"),
    path('profile/unlike/<int:post_id>', views.unlike, name="unlike"),
    path('profile/like/<int:post_id>', views.like, name="like"),
    path('comments', views.comment, name="comment"),
    path('save/<int:post_id>', views.save, name="save"),
    path('unsave/<int:post_id>', views.unsave, name="unsave"),
    path('follow/<str:username>', views.follow, name="follow"),
    path('unfollow/<str:username>', views.unfollow, name="unfollow"),

    path('<str:username>', views.profile, name='profile'),
  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)