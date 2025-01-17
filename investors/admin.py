from django.contrib import admin

# Register your models here.


from .models import GainRecord

@admin.register(GainRecord)
class GainRecordAdmin(admin.ModelAdmin):
    list_display = ('project', 'amount','created_at')
    list_filter = ('project','created_at')
    search_fields = ('project__uid', 'amount')