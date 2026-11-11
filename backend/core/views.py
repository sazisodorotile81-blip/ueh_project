from django.db.models import Count
from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, ServiceRequest, Opportunity, Application
from .serializers import RegisterSerializer, UserSerializer, ServiceRequestSerializer, OpportunitySerializer, ApplicationSerializer
from .permissions import IsAdminRole, RequestObjectPermission, OpportunityPermission, ApplicationPermission

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user

class ServiceRequestViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticated, RequestObjectPermission]
    def get_queryset(self):
        user = self.request.user
        qs = ServiceRequest.objects.select_related("client", "assigned_agent")
        if user.is_staff or user.role == User.Role.ADMIN:
            return qs
        if user.role == User.Role.AGENT:
            return qs.filter(assigned_agent=user)
        return qs.filter(client=user)
    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

class OpportunityViewSet(viewsets.ModelViewSet):
    serializer_class = OpportunitySerializer
    permission_classes = [OpportunityPermission]
    def get_queryset(self):
        user = self.request.user
        qs = Opportunity.objects.select_related("created_by").annotate(application_count=Count("applications"))
        if user.is_staff or user.role == User.Role.ADMIN:
            return qs
        qs = qs.filter(is_published=True)
        opportunity_type = self.request.query_params.get("type")
        search = self.request.query_params.get("search")
        if opportunity_type:
            qs = qs.filter(opportunity_type=opportunity_type.upper())
        if search:
            qs = qs.filter(title__icontains=search)
        return qs
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def apply(self, request, pk=None):
        opportunity = self.get_object()
        if request.user.role != User.Role.CLIENT:
            return Response({"detail": "Only MSME clients can apply."}, status=403)
        serializer = ApplicationSerializer(data={
            "opportunity": opportunity.pk,
            "motivation": request.data.get("motivation", "")
        }, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save(applicant=request.user)
        return Response(serializer.data, status=201)

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, ApplicationPermission]
    http_method_names = ["get", "patch", "head", "options"]
    def get_queryset(self):
        user = self.request.user
        qs = Application.objects.select_related("opportunity", "applicant")
        if user.is_staff or user.role == User.Role.ADMIN:
            return qs
        return qs.filter(applicant=user)

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if user.is_staff or user.role == User.Role.ADMIN:
            return Response({
                "role": user.role,
                "open_requests": ServiceRequest.objects.filter(status="OPEN").count(),
                "in_progress_requests": ServiceRequest.objects.filter(status="IN_PROGRESS").count(),
                "resolved_requests": ServiceRequest.objects.filter(status="RESOLVED").count(),
                "applications_per_opportunity": list(Opportunity.objects.annotate(total=Count("applications")).values("id", "title", "total")),
                "total_applications": Application.objects.count(),
            })
        if user.role == User.Role.AGENT:
            qs = ServiceRequest.objects.filter(assigned_agent=user)
        else:
            qs = ServiceRequest.objects.filter(client=user)
        return Response({
            "role": user.role,
            "open_requests": qs.filter(status="OPEN").count(),
            "in_progress_requests": qs.filter(status="IN_PROGRESS").count(),
            "resolved_requests": qs.filter(status="RESOLVED").count(),
            "my_applications": Application.objects.filter(applicant=user).count(),
        })
