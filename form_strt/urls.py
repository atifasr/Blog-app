"""Define urls for Form"""


from django import urls
from django.urls import path
from . import views
app_name = 'form_strt'


urlpatterns = [
    # homepage
    path('', views.disp_, name='form_data'),
    path('create/', views.create, name='create'),
    path('update/<int:val_id>/', views.update, name='update'),
    path('delete/<int:val_id>/', views.delete_, name='delete_'),
    # path('disp/', views.disp_data, name='disp-data'),
]
