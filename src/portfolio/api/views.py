"""Portfolio API views — read-only endpoints."""

from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from portfolio import services
from portfolio.models import Project

from .serializers import (
    CertificationSerializer,
    EducationSerializer,
    ExperienceSerializer,
    ProfileSerializer,
    ProjectDetailSerializer,
    ProjectListSerializer,
    SkillCategorySerializer,
)


class ProfileAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        profile = services.get_active_profile()
        if not profile:
            return Response({"detail": "No active profile."}, status=404)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)


class SkillListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SkillCategorySerializer

    def get_queryset(self):
        return services.get_skills_by_category()


class ExperienceListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ExperienceSerializer

    def get_queryset(self):
        return services.get_experiences()


class EducationListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = EducationSerializer

    def get_queryset(self):
        return services.get_education()


class CertificationListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CertificationSerializer

    def get_queryset(self):
        return services.get_certifications()


class ProjectListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProjectListSerializer

    def get_queryset(self):
        return services.get_all_projects()


class ProjectDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProjectDetailSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return (
            Project.objects
            .filter(is_active=True)
            .prefetch_related('technologies', 'images')
        )
