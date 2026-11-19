
from django.urls import path
from . import views

app_name = 'prospek'

urlpatterns = [
    path('', views.index, name='index'),
    path('tambah/', views.tambah, name='tambah'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('hapus/<int:id>/', views.hapus, name='hapus'),

    path('detail/<int:id>/', views.detail, name='detail'),

    path('reminder/', views.daftar_reminder, name='reminder'),
    path(
        'reminder/selesai/<int:id>/',
        views.selesaikan_reminder,
        name='selesaikan_reminder'
    ),

    path('export/', views.export_excel, name='export_excel'),
]
