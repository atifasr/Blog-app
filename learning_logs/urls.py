"""defines urls for learning_logs"""

from os import P_DETACH
from django.urls import path
from . import views
app_name = 'learning_logs'

urlpatterns = [
    # homepage
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('get_form/', views.give_data, name='get_form'),
    path('login/', views.login_form, name='login-form'),
    path('dashboard/', views.posts_, name='dash-board'),
    path('add_page/', views.add_page, name='add_page'),
    path('logout/', views.log_out, name='log-out'),
    path('comment/<int:entry_id>/', views.comment_add, name='comment'),
    path('update_post/<int:topic_id>/', views.update_post, name='update-post'),
    path('like/<int:entry_id>',views.add_like,name='add-like'),
    path('all_likes/<int:entry_id>',views.all_likes,name='all-likes'),
    path('categories', views.get_categories, name='get-categories'),
    path('posts/', views.posts_, name='get-posts'),
    path('topics/<str:art_name>/', views.topic_a, name='topics'),
    path('send_email/', views.send_email, name='send-email'),


]
