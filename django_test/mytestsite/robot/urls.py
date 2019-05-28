from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_list, name='report_list'),
    path('<int:n_dias>/', views.report_list, name='report_list_n'),
    path('relatorio/<path:report_link>/', views.report_show, name='report_show'),
]