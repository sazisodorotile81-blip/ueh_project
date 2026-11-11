from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers
from .models import User, ServiceRequest, RequestStatusHistory, Opportunity, Application

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "role", "business_name", "phone"]
        read_only_fields = ["id", "role"]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name", "business_name", "phone"]
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data, role=User.Role.CLIENT)
        user.set_password(password)
        user.save()
        return user

class ServiceRequestSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source="client.username", read_only=True)
    assigned_agent_name = serializers.CharField(source="assigned_agent.username", read_only=True)
    class Meta:
        model = ServiceRequest
        fields = "__all__"
        read_only_fields = ["client", "created_at", "updated_at", "resolved_at"]
    def validate_description(self, value):
        value = value.strip()
        if len(value) < 10:
            raise serializers.ValidationError("Please provide at least 10 characters.")
        return value
    def validate(self, attrs):
        request = self.context.get("request")
        if request and request.method in ("POST", "PUT", "PATCH"):
            user = request.user
            if "assigned_agent" in attrs and user.role not in (User.Role.ADMIN,) and not user.is_staff:
                raise serializers.ValidationError({"assigned_agent": "Only an admin can assign an agent."})
            if "status" in attrs and user.role == User.Role.CLIENT:
                raise serializers.ValidationError({"status": "Clients cannot change request status."})
        return attrs
    def update(self, instance, validated_data):
        new_status = validated_data.get("status")
        old_status = instance.status
        if new_status == ServiceRequest.Status.RESOLVED and not instance.resolved_at:
            validated_data["resolved_at"] = timezone.now()
        updated = super().update(instance, validated_data)
        if new_status and new_status != old_status:
            RequestStatusHistory.objects.create(
                service_request=updated,
                changed_by=self.context["request"].user,
                old_status=old_status,
                new_status=new_status,
            )
        return updated

class OpportunitySerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source="created_by.username", read_only=True)
    class Meta:
        model = Opportunity
        fields = "__all__"
        read_only_fields = ["created_by", "created_at"]

class ApplicationSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(source="applicant.username", read_only=True)
    opportunity_title = serializers.CharField(source="opportunity.title", read_only=True)
    class Meta:
        model = Application
        fields = "__all__"
        read_only_fields = ["applicant", "submitted_at", "reviewed_at"]
    def validate_motivation(self, value):
        if len(value.strip()) < 20:
            raise serializers.ValidationError("Motivation must be at least 20 characters.")
        return value.strip()
    def validate(self, attrs):
        request = self.context.get("request")
        if request and request.method == "PATCH" and request.user.role != User.Role.ADMIN and not request.user.is_staff:
            raise serializers.ValidationError("Only administrators can review applications.")
        return attrs
    def update(self, instance, validated_data):
        if "status" in validated_data:
            validated_data["reviewed_at"] = timezone.now()
        return super().update(instance, validated_data)
