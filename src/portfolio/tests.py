"""Tests for portfolio models, views, and services."""

from datetime import date

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import (
    Certification, Education, Experience, ExperiencePoint,
    Profile, Project, ProjectImage, Skill, SkillCategory,
    SocialLink, Technology,
)

User = get_user_model()


class ProfileModelTest(TestCase):
    def test_create_profile(self):
        profile = Profile.objects.create(
            name="Test User",
            designation="Developer",
            short_bio="A test bio.",
            about="Full about text.",
            email="test@example.com",
        )
        self.assertEqual(str(profile), "Test User")
        self.assertTrue(profile.is_active)

    def test_social_link_unique_constraint(self):
        profile = Profile.objects.create(
            name="Test", designation="Dev", short_bio="Bio", about="About", email="t@t.com",
        )
        SocialLink.objects.create(profile=profile, platform='github', url='https://github.com/test')
        with self.assertRaises(Exception):
            SocialLink.objects.create(profile=profile, platform='github', url='https://github.com/test2')

    def test_social_link_str(self):
        profile = Profile.objects.create(
            name="Test", designation="Dev", short_bio="Bio", about="About", email="t@t.com",
        )
        link = SocialLink.objects.create(profile=profile, platform='github', url='https://github.com/test')
        self.assertIn("GitHub", str(link))


class SkillModelTest(TestCase):
    def test_skill_category_auto_slug(self):
        cat = SkillCategory.objects.create(name="Backend Dev")
        self.assertEqual(cat.slug, "backend-dev")

    def test_skill_str(self):
        cat = SkillCategory.objects.create(name="Backend", slug="backend")
        skill = Skill.objects.create(category=cat, name="Python", proficiency=90)
        self.assertEqual(str(skill), "Python (Backend)")


class ExperienceModelTest(TestCase):
    def test_experience_str(self):
        exp = Experience.objects.create(
            company_name="TestCo", job_title="Dev", start_date=date(2023, 1, 1),
        )
        self.assertEqual(str(exp), "Dev at TestCo")

    def test_experience_points(self):
        exp = Experience.objects.create(
            company_name="TestCo", job_title="Dev", start_date=date(2023, 1, 1),
        )
        point = ExperiencePoint.objects.create(experience=exp, description="Did things", order=0)
        self.assertEqual(exp.points.count(), 1)
        self.assertEqual(str(point), "Did things")


class ProjectModelTest(TestCase):
    def test_project_with_technologies(self):
        tech = Technology.objects.create(name="Django", slug="django")
        project = Project.objects.create(
            title="Test Project", slug="test-project",
            short_description="Short desc", description="Full desc",
        )
        project.technologies.add(tech)
        self.assertEqual(project.technologies.count(), 1)
        self.assertEqual(str(project), "Test Project")

    def test_technology_auto_slug(self):
        tech = Technology.objects.create(name="Django REST Framework")
        self.assertEqual(tech.slug, "django-rest-framework")


class EducationModelTest(TestCase):
    def test_education_str(self):
        edu = Education.objects.create(
            degree="BSc CS", institution="MIT", start_year=2020, end_year=2024,
        )
        self.assertIn("MIT", str(edu))


class CertificationModelTest(TestCase):
    def test_certification_str(self):
        cert = Certification.objects.create(
            name="AWS Dev", issuing_organization="AWS", issue_date=date(2023, 1, 1),
        )
        self.assertIn("AWS", str(cert))


# ---- View Tests ----

class PortfolioViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.profile = Profile.objects.create(
            name="Test", designation="Dev", short_bio="Bio", about="About", email="t@t.com",
        )
        cls.tech = Technology.objects.create(name="Python", slug="python")
        cls.project = Project.objects.create(
            title="Project", slug="test-proj",
            short_description="Desc", description="Full desc",
            is_active=True, is_featured=True,
        )
        cls.project.technologies.add(cls.tech)

    def setUp(self):
        self.client = Client()

    def test_homepage(self):
        response = self.client.get(reverse('portfolio:home'))
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.client.get(reverse('portfolio:about'))
        self.assertEqual(response.status_code, 200)

    def test_skills_page(self):
        response = self.client.get(reverse('portfolio:skills'))
        self.assertEqual(response.status_code, 200)

    def test_experience_page(self):
        response = self.client.get(reverse('portfolio:experience'))
        self.assertEqual(response.status_code, 200)

    def test_education_page(self):
        response = self.client.get(reverse('portfolio:education'))
        self.assertEqual(response.status_code, 200)

    def test_certifications_page(self):
        response = self.client.get(reverse('portfolio:certifications'))
        self.assertEqual(response.status_code, 200)

    def test_project_list(self):
        response = self.client.get(reverse('portfolio:project_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Project")

    def test_project_detail(self):
        response = self.client.get(reverse('portfolio:project_detail', kwargs={'slug': 'test-proj'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Project")

    def test_project_tech_filter(self):
        response = self.client.get(reverse('portfolio:project_list') + '?tech=python')
        self.assertEqual(response.status_code, 200)

    def test_project_404(self):
        response = self.client.get(reverse('portfolio:project_detail', kwargs={'slug': 'nonexistent'}))
        self.assertEqual(response.status_code, 404)
