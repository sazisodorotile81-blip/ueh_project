from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ServiceRequest, RequestStatusHistory, Opportunity, Application

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("UEH profile", {"fields": ("role", "business_name", "phone")}),)
    list_display = ("username", "email", "role", "is_staff")

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "category", "urgency", "status", "assigned_agent", "created_at")
    list_filter = ("status", "urgency", "category")
    search_fields = ("description", "client__username")

@admin.register(RequestStatusHistory)
class RequestStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ("service_request", "old_status", "new_status", "changed_by", "changed_at")
    readonly_fields = ("service_request", "old_status", "new_status", "changed_by", "note", "changed_at")

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ("title", "opportunity_type", "closing_date", "is_published")
    list_filter = ("opportunity_type", "is_published")

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("opportunity", "applicant", "status", "submitted_at")
    list_filter = ("status",)
