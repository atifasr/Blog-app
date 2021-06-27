"""defines urls for practice_page"""

from django.urls import path
from . import views
app_name='practice'

urlpatterns=[
    #homepage
    path('',views.index,name='index'),
    path('blog/',views.blog,name='blog'),
    path('entry/',views.entry,name='entry'),
    path('register/',views.register,name='register')
    #path('topics/<int:topic_id>/', views.topic, name='topic'),
]
