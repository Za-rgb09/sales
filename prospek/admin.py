from django.contrib import admin
from .models import Prospek, FollowUp, Reminder


@admin.register(Prospek)
class ProspekAdmin(admin.ModelAdmin):
    list_display = (
        'nama',
        'nomor_hp',
        'unit_diminati',
        'status',
        'created_at',
    )
    list_filter = ('status',)
    search_fields = ('nama', 'nomor_hp', 'unit_diminati')


@admin.register(FollowUp)
class FollowUpAdmin(admin.ModelAdmin):
    list_display = ('prospek', 'metode', 'tanggal')
    list_filter = ('metode',)
    search_fields = ('prospek__nama',)


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('judul', 'prospek', 'tanggal', 'selesai')
    list_filter = ('selesai',)
    search_fields = ('judul', 'prospek__nama')