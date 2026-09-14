"""Portfolio API serializers."""

from rest_framework import serializers

from portfolio.models import (
    Certification,
    Education,
    Experience,
    ExperiencePoint,
    Profile,
    Project,
    ProjectImage,
    Skill,
    SkillCategory,
    SocialLink,
    Technology,
)


class SocialLinkSerializer(serializers.ModelSerializer):
    platform_display = serializers.CharField(source='get_platform_display', read_only=True)

    class Meta:
        model = SocialLink
        fields = ['id', 'platform', 'platform_display', 'url', 'icon_class', 'order']


class ProfileSerializer(serializers.ModelSerializer):
    social_links = SocialLinkSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'name', 'designation', 'profile_image', 'short_bio',
            'about', 'email', 'phone', 'location', 'resume',
            'is_available', 'social_links',
        ]


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'proficiency', 'order']


class SkillCategorySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = SkillCategory
        fields = ['id', 'name', 'slug', 'order', 'skills']


class ExperiencePointSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExperiencePoint
        fields = ['id', 'description', 'order']


class ExperienceSerializer(serializers.ModelSerializer):
    points = ExperiencePointSerializer(many=True, read_only=True)
    duration = serializers.CharField(read_only=True)

    class Meta:
        model = Experience
        fields = [
            'id', 'company_name', 'job_title', 'location',
            'start_date', 'end_date', 'is_current', 'description',
            'duration', 'points',
        ]


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = [
            'id', 'degree', 'institution', 'field_of_study',
            'start_year', 'end_year', 'description',
        ]


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = [
            'id', 'name', 'issuing_organization', 'issue_date',
            'credential_id', 'credential_url', 'certificate_image',
        ]


class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = ['id', 'name', 'slug', 'icon_class']


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'caption', 'order']


class ProjectListSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'short_description', 'thumbnail',
            'technologies', 'github_url', 'live_url', 'is_featured',
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    technologies = TechnologySerializer(many=True, read_only=True)
    images = ProjectImageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'title', 'slug', 'short_description', 'description',
            'thumbnail', 'technologies', 'images', 'github_url', 'live_url',
            'start_date', 'end_date', 'is_featured',
        ]
