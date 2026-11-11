from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator

class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = "CLIENT", "MSME Client"
        AGENT = "AGENT", "UEH Support Agent"
        ADMIN = "ADMIN", "UEH Admin"
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CLIENT)
    business_name = models.CharField(max_length=160, blank=True)
    phone = models.CharField(max_length=30, blank=True)

class ServiceRequest(models.Model):
    class Category(models.TextChoices):
        FUNDING = "FUNDING", "Funding support"
        BUSINESS = "BUSINESS", "Business advice"
        COMPLIANCE = "COMPLIANCE", "Compliance"
        MARKETING = "MARKETING", "Marketing"
        OTHER = "OTHER", "Other"
    class Urgency(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        RESOLVED = "RESOLVED", "Resolved"
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="service_requests")
    assigned_agent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_requests")
    category = models.CharField(max_length=20, choices=Category.choices)
    description = models.TextField(validators=[MinLengthValidator(10)])
    urgency = models.CharField(max_length=10, choices=Urgency.choices, default=Urgency.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"Request #{self.pk} - {self.category}"

class Opportunity(models.Model):
    class Type(models.TextChoices):
        FUNDING = "FUNDING", "Funding"
        TENDER = "TENDER", "Tender"
        TRAINING = "TRAINING", "Training"
    title = models.CharField(max_length=180)
    opportunity_type = models.CharField(max_length=12, choices=Type.choices)
    description = models.TextField(validators=[MinLengthValidator(20)])
    eligibility = models.TextField(blank=True)
    closing_date = models.DateField(null=True, blank=True)
    is_published = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="posted_opportunities")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class RequestStatusHistory(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name="status_history")
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="request_status_changes")
    old_status = models.CharField(max_length=20, choices=ServiceRequest.Status.choices)
    new_status = models.CharField(max_length=20, choices=ServiceRequest.Status.choices)
    note = models.CharField(max_length=300, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["changed_at"]

class Application(models.Model):
    class Status(models.TextChoices):
        SUBMITTED = "SUBMITTED", "Submitted"
        UNDER_REVIEW = "UNDER_REVIEW", "Under review"
        APPROVED = "APPROVED", "Approved"
        DECLINED = "DECLINED", "Declined"
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    motivation = models.TextField(validators=[MinLengthValidator(20)])
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED)
    admin_notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["opportunity", "applicant"], name="one_application_per_client_opportunity")]
