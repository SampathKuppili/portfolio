"""
Management command to clear demo/seed data.
Usage: python manage.py clear_demo_data
"""

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from blog.models import BlogPost, Category, Tag
from common.models import SiteSettings
from contact.models import ContactMessage
from portfolio.models import (
    Certification,
    Education,
    Experience,
    Profile,
    Project,
    Skill,
    SkillCategory,
    Technology,
)

User = get_user_model()


class Command(BaseCommand):
    help = "Clear all demo/seed data from the database."

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Skip confirmation prompt.',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            answer = input("This will DELETE all portfolio data. Type 'yes' to confirm: ")
            if answer.lower() != 'yes':
                self.stdout.write("Aborted.")
                return

        BlogPost.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        ContactMessage.objects.all().delete()
        Project.objects.all().delete()
        Technology.objects.all().delete()
        Certification.objects.all().delete()
        Education.objects.all().delete()
        Experience.objects.all().delete()
        Skill.objects.all().delete()
        SkillCategory.objects.all().delete()
        Profile.objects.all().delete()
        SiteSettings.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("[OK] All demo data cleared."))

