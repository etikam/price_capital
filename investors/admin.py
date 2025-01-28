from django.contrib import admin
from .models import Investor, Investissement, Achat, GainRecord

# Register your models here.


@admin.register(GainRecord)
class GainRecordAdmin(admin.ModelAdmin):
    list_display = ('project', 'amount','created_at')
    list_filter = ('project','created_at')
    search_fields = ('project__uid', 'amount')
    



@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    list_display = ('investor_id', 'full_name', 'email', 'phone', 'available_budget', 'preferred_currency', 'investment_experience')
    search_fields = ('investor_id', 'first_name', 'last_name', 'email', 'phone')
    list_filter = ('preferred_currency', 'investment_experience', 'investment_type')
    ordering = ('-created_at',)


@admin.register(Investissement)
class InvestissementAdmin(admin.ModelAdmin):
    list_display = ('uid', 'investor', 'project', 'amount', 'currency', 'progress', 'payment_done', 'created_at')
    search_fields = ('uid', 'investor__first_name', 'investor__last_name', 'project__title')
    list_filter = ('progress', 'currency', 'payment_done')
    ordering = ('-created_at',)
    raw_id_fields = ('investor', 'project')


@admin.register(Achat)
class AchatAdmin(admin.ModelAdmin):
    list_display = ('uid', 'buyer', 'product', 'quantity', 'total_amount', 'order_status', 'created_at')
    search_fields = ('uid', 'buyer__first_name', 'buyer__last_name', 'product__product_name')
    list_filter = ('order_status',)
    ordering = ('-created_at',)
    raw_id_fields = ('buyer', 'product')


