from django.contrib import admin
from .models import Plan, Restrict, Subscription

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_filter = ('user', 'plan_name', 'price', 'article_read_limit', 'recurring_freq', 'is_recurring')
    list_display = ['id', 'user', 'plan_name', 'price', 'article_read_limit', 'recurring_freq', 'is_recurring']

@admin.register(Restrict)
class RestrictAdmin(admin.ModelAdmin):
    list_filter = ('user', 'plan', 'read_date')
    list_display = ['id', 'user', 'plan', 'read_date']

@admin.register(Subscription)
class RestrictAdmin(admin.ModelAdmin):
    list_filter = ('user', 'plan', 'customer_id', 'payment_id', 'status', 'created_at', 'expire_at')
    list_display = ['id', 'user', 'plan', 'customer_id', 'payment_id', 'status', 'created_at', 'expire_at']
