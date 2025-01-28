from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import MoralPerson, PhysicalPerson, User


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    list_display = ("email", "is_staff", "is_active", "is_superuser")
    search_fields = ("email",)
    ordering = ("email",)


@admin.register(PhysicalPerson)
class PhysicalPersonAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "telephone", "user")


@admin.register(MoralPerson)
class MoralPersonAdmin(admin.ModelAdmin):
    list_display = ("company_name", "telephone", "user")
