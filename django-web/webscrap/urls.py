from django.urls import path
from . import views
from .views import login, loginView, logoutView


urlpatterns = [
	path('logout',views.logoutView,name='logout'),
    path('',views.loginView,name='login'),
    path('dashboard',views.dashboard, name='dashboard'),
    path('update_schedule/<int:task_id>', views.update_schedule, name='update_schedule'),
    path('delete_schedule/<int:task_id>', views.delete_schedule, name='delete_schedule'),
    path('skattefunn', views.skattefunn, name='skattefunn')
]
