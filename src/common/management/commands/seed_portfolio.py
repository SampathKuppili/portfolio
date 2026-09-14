"""
Management command to seed the portfolio with demo data.
Idempotent — safe to run multiple times.

Usage:
    python manage.py seed_portfolio
"""

import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from blog.models import BlogPost, Category, Tag
from common.models import SiteSettings
from portfolio.models import (
    Certification,
    Education,
    Experience,
    ExperiencePoint,
    Profile,
    Project,
    Skill,
    SkillCategory,
    SocialLink,
    Technology,
)

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with demo portfolio data."

    def handle(self, *args, **options):
        self.stdout.write("Seeding portfolio data...")

        self._create_site_settings()
        admin_user = self._create_admin_user()
        profile = self._create_profile()
        self._create_social_links(profile)
        self._create_skills()
        self._create_experience()
        self._create_education()
        self._create_certifications()
        technologies = self._create_technologies()
        self._create_projects(technologies)
        self._create_blog(admin_user)

        self.stdout.write(self.style.SUCCESS("[OK] Portfolio seeded successfully!"))

    def _create_site_settings(self):
        SiteSettings.objects.get_or_create(
            site_name="DevPortfolio",
            defaults={
                'site_title': "Professional Python/Django Developer Portfolio",
                'meta_description': "Experienced Python/Django developer building clean, scalable web applications. View my projects, skills, and blog.",
                'is_active': True,
            },
        )
        self.stdout.write("  [OK] Site settings")

    def _create_admin_user(self):
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True,
            },
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write("  [OK] Admin user created (admin / admin123)")
        else:
            self.stdout.write("  [OK] Admin user (already exists)")
        return user

    def _create_profile(self):
        profile, _ = Profile.objects.get_or_create(
            name="Alex Johnson",
            defaults={
                'designation': "Senior Python/Django Developer",
                'short_bio': "Passionate about building clean, scalable web applications with Python and Django. 5+ years of experience delivering production-grade solutions.",
                'about': (
                    "I'm a Senior Python/Django Developer with over 5 years of experience building "
                    "robust web applications. I specialize in backend development with Django and Django REST Framework, "
                    "designing PostgreSQL databases, and creating clean RESTful APIs.\n\n"
                    "I'm passionate about writing clean, maintainable code and following best practices in software "
                    "development. I believe in continuous learning and sharing knowledge with the developer community.\n\n"
                    "When I'm not coding, I enjoy contributing to open-source projects, writing technical articles, "
                    "and mentoring junior developers."
                ),
                'email': 'alex@example.com',
                'phone': '+1 (555) 123-4567',
                'location': 'San Francisco, CA',
                'is_available': True,
                'is_active': True,
            },
        )
        self.stdout.write("  [OK] Profile")
        return profile

    def _create_social_links(self, profile):
        links = [
            ('github', 'https://github.com/alexjohnson', 1),
            ('linkedin', 'https://linkedin.com/in/alexjohnson', 2),
            ('twitter', 'https://twitter.com/alexjohnson', 3),
            ('stackoverflow', 'https://stackoverflow.com/users/12345/alexjohnson', 4),
        ]
        for platform, url, order in links:
            SocialLink.objects.get_or_create(
                profile=profile,
                platform=platform,
                defaults={'url': url, 'order': order, 'is_active': True},
            )
        self.stdout.write("  [OK] Social links")

    def _create_skills(self):
        categories = {
            'Backend': [
                ('Python', 90), ('Django', 88), ('Django REST Framework', 85),
                ('FastAPI', 70), ('Celery', 72),
            ],
            'Database': [
                ('PostgreSQL', 85), ('MySQL', 75), ('Redis', 70),
                ('SQLite', 80), ('MongoDB', 60),
            ],
            'Frontend': [
                ('HTML/CSS', 80), ('JavaScript', 72), ('Bootstrap', 75),
                ('Tailwind CSS', 70), ('HTMX', 65),
            ],
            'DevOps': [
                ('Docker', 75), ('Git', 88), ('Linux', 78),
                ('Nginx', 72), ('CI/CD', 68),
            ],
            'Tools': [
                ('VS Code', 90), ('Postman', 85), ('Jira', 75),
                ('Swagger', 80),
            ],
        }
        for idx, (cat_name, skills) in enumerate(categories.items()):
            category, _ = SkillCategory.objects.get_or_create(
                name=cat_name,
                defaults={'slug': cat_name.lower(), 'order': idx, 'is_active': True},
            )
            for skill_idx, (skill_name, proficiency) in enumerate(skills):
                Skill.objects.get_or_create(
                    category=category,
                    name=skill_name,
                    defaults={'proficiency': proficiency, 'order': skill_idx, 'is_active': True},
                )
        self.stdout.write("  [OK] Skills & categories")

    def _create_experience(self):
        experiences = [
            {
                'company_name': 'TechCorp Solutions',
                'job_title': 'Senior Python/Django Developer',
                'location': 'San Francisco, CA',
                'start_date': datetime.date(2022, 6, 1),
                'is_current': True,
                'description': 'Leading backend development for multiple client projects.',
                'order': 1,
                'points': [
                    'Architected and developed Django applications serving 100K+ users',
                    'Built RESTful APIs using Django REST Framework with comprehensive documentation',
                    'Designed and optimized PostgreSQL database schemas for high-traffic applications',
                    'Implemented CI/CD pipelines using GitHub Actions and Docker',
                    'Mentored junior developers and conducted code reviews',
                    'Integrated third-party APIs including Stripe, Twilio, and AWS services',
                ],
            },
            {
                'company_name': 'WebDev Agency',
                'job_title': 'Python Developer',
                'location': 'Remote',
                'start_date': datetime.date(2020, 3, 1),
                'end_date': datetime.date(2022, 5, 31),
                'is_current': False,
                'description': 'Full-stack Django development for various client projects.',
                'order': 2,
                'points': [
                    'Developed full-stack Django applications for e-commerce and SaaS platforms',
                    'Created automated testing suites achieving 90%+ code coverage',
                    'Implemented caching strategies with Redis reducing response times by 40%',
                    'Deployed applications using Docker containers on AWS EC2',
                    'Collaborated with frontend developers to build responsive UIs',
                ],
            },
            {
                'company_name': 'StartupHub',
                'job_title': 'Junior Python Developer',
                'location': 'Austin, TX',
                'start_date': datetime.date(2019, 1, 1),
                'end_date': datetime.date(2020, 2, 28),
                'is_current': False,
                'description': 'Entry-level backend development and API integration.',
                'order': 3,
                'points': [
                    'Built and maintained Django web applications',
                    'Wrote unit and integration tests using pytest',
                    'Assisted in database design and migration planning',
                    'Created internal tools and automation scripts',
                ],
            },
        ]

        for exp_data in experiences:
            points = exp_data.pop('points')
            exp, created = Experience.objects.get_or_create(
                company_name=exp_data['company_name'],
                job_title=exp_data['job_title'],
                defaults=exp_data,
            )
            if created:
                for idx, point_text in enumerate(points):
                    ExperiencePoint.objects.create(
                        experience=exp, description=point_text, order=idx,
                    )
        self.stdout.write("  [OK] Experience")

    def _create_education(self):
        Education.objects.get_or_create(
            degree="Bachelor of Science in Computer Science",
            institution="University of California, Berkeley",
            defaults={
                'field_of_study': 'Computer Science',
                'start_year': 2015,
                'end_year': 2019,
                'description': 'Focused on software engineering, algorithms, and web development. Graduated with honors.',
                'order': 1,
            },
        )
        self.stdout.write("  [OK] Education")

    def _create_certifications(self):
        certs = [
            ("AWS Certified Developer – Associate", "Amazon Web Services", datetime.date(2023, 3, 15), "AWS-DEV-12345"),
            ("Django for Professionals", "TestDriven.io", datetime.date(2022, 8, 1), "TDI-DFP-67890"),
            ("Python Institute PCEP", "Python Institute", datetime.date(2021, 5, 20), "PCEP-30-02-0012345"),
        ]
        for name, org, date, cred_id in certs:
            Certification.objects.get_or_create(
                name=name,
                issuing_organization=org,
                defaults={'issue_date': date, 'credential_id': cred_id},
            )
        self.stdout.write("  [OK] Certifications")

    def _create_technologies(self):
        tech_names = [
            'Python', 'Django', 'Django REST Framework', 'PostgreSQL', 'MySQL',
            'SQLite', 'Redis', 'Docker', 'Git', 'Linux', 'HTML', 'CSS',
            'JavaScript', 'Bootstrap', 'Tailwind CSS', 'Celery', 'Nginx',
            'AWS', 'HTMX', 'FastAPI',
        ]
        techs = {}
        for name in tech_names:
            tech, _ = Technology.objects.get_or_create(
                name=name,
                defaults={'slug': name.lower().replace(' ', '-').replace('/', '-')},
            )
            techs[name] = tech
        self.stdout.write("  [OK] Technologies")
        return techs

    def _create_projects(self, techs):
        projects = [
            {
                'title': 'E-Commerce Platform',
                'slug': 'ecommerce-platform',
                'short_description': 'A full-featured e-commerce platform built with Django, Stripe payments, and real-time inventory management.',
                'description': (
                    "A comprehensive e-commerce platform built from scratch using Django.\n\n"
                    "Features include product catalog with categories, shopping cart, "
                    "Stripe payment integration, order management, user authentication, "
                    "inventory tracking, and admin dashboard.\n\n"
                    "The application is containerized with Docker and deployed on AWS EC2 "
                    "with PostgreSQL database and Redis caching."
                ),
                'github_url': 'https://github.com/alexjohnson/ecommerce-platform',
                'live_url': 'https://demo-ecommerce.example.com',
                'is_featured': True,
                'order': 1,
                'techs': ['Django', 'PostgreSQL', 'Redis', 'Docker', 'JavaScript', 'Tailwind CSS'],
            },
            {
                'title': 'Task Management API',
                'slug': 'task-management-api',
                'short_description': 'RESTful API for task management with JWT authentication, real-time WebSocket notifications, and team collaboration.',
                'description': (
                    "A robust REST API built with Django REST Framework for managing tasks and projects.\n\n"
                    "Features JWT-based authentication, role-based permissions, task assignment, "
                    "project boards, file attachments, and real-time notifications via WebSockets.\n\n"
                    "Includes comprehensive API documentation with Swagger/OpenAPI."
                ),
                'github_url': 'https://github.com/alexjohnson/task-management-api',
                'is_featured': True,
                'order': 2,
                'techs': ['Django', 'Django REST Framework', 'PostgreSQL', 'Redis', 'Docker'],
            },
            {
                'title': 'Developer Blog',
                'slug': 'developer-blog',
                'short_description': 'A modern technical blog with markdown support, syntax highlighting, and SEO optimization.',
                'description': (
                    "A full-featured technical blog built with Django.\n\n"
                    "Features markdown support, syntax highlighting for code blocks, "
                    "categories and tags, full-text search, RSS feed, sitemap, "
                    "and SEO-optimized meta tags.\n\n"
                    "Responsive design with dark/light theme support."
                ),
                'github_url': 'https://github.com/alexjohnson/dev-blog',
                'live_url': 'https://blog.example.com',
                'is_featured': True,
                'order': 3,
                'techs': ['Django', 'PostgreSQL', 'HTML', 'CSS', 'JavaScript', 'HTMX'],
            },
            {
                'title': 'Real-Time Chat Application',
                'slug': 'real-time-chat',
                'short_description': 'WebSocket-based chat application with rooms, direct messages, and file sharing.',
                'description': (
                    "A real-time chat application built with Django Channels.\n\n"
                    "Features group chat rooms, direct messaging, file sharing, "
                    "message history, online status indicators, and typing notifications."
                ),
                'github_url': 'https://github.com/alexjohnson/realtime-chat',
                'is_featured': True,
                'order': 4,
                'techs': ['Django', 'Redis', 'JavaScript', 'Docker', 'PostgreSQL'],
            },
            {
                'title': 'Portfolio Website',
                'slug': 'portfolio-website',
                'short_description': 'This portfolio website — a professional Django-powered portfolio with blog, projects, and REST API.',
                'description': (
                    "A professional portfolio website built with Django.\n\n"
                    "Features a responsive design with dark/light theme, project showcase, "
                    "technical blog, contact form, REST API, and admin CMS.\n\n"
                    "Demonstrates clean Django architecture with service layers, "
                    "proper testing, and production-ready configuration."
                ),
                'github_url': 'https://github.com/alexjohnson/portfolio',
                'is_featured': True,
                'order': 5,
                'techs': ['Django', 'Django REST Framework', 'SQLite', 'Tailwind CSS', 'HTMX', 'JavaScript'],
            },
            {
                'title': 'Weather Dashboard',
                'slug': 'weather-dashboard',
                'short_description': 'Weather monitoring dashboard with city search, forecasts, and data visualization.',
                'description': (
                    "A weather dashboard that integrates with OpenWeatherMap API.\n\n"
                    "Features city search, current conditions, 5-day forecasts, "
                    "and historical data visualization with charts."
                ),
                'github_url': 'https://github.com/alexjohnson/weather-dashboard',
                'is_featured': False,
                'order': 6,
                'techs': ['Django', 'JavaScript', 'Bootstrap', 'PostgreSQL'],
            },
        ]

        for proj_data in projects:
            tech_names = proj_data.pop('techs')
            proj, created = Project.objects.get_or_create(
                slug=proj_data['slug'],
                defaults={**proj_data, 'is_active': True},
            )
            if created:
                for tech_name in tech_names:
                    if tech_name in techs:
                        proj.technologies.add(techs[tech_name])
        self.stdout.write("  [OK] Projects")

    def _create_blog(self, author):
        # Categories
        categories = {}
        for name in ['Django', 'Python', 'DevOps', 'Database', 'API Development']:
            cat, _ = Category.objects.get_or_create(
                name=name,
                defaults={'slug': name.lower().replace(' ', '-'), 'is_active': True},
            )
            categories[name] = cat

        # Tags
        tag_names = ['python', 'django', 'rest-api', 'postgresql', 'docker', 'testing', 'deployment', 'beginner', 'advanced', 'tutorial']
        tags = {}
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(
                name=name,
                defaults={'slug': name},
            )
            tags[name] = tag

        # Posts
        posts_data = [
            {
                'title': 'Building RESTful APIs with Django REST Framework',
                'slug': 'building-restful-apis-django-rest-framework',
                'category': categories['API Development'],
                'excerpt': 'A comprehensive guide to building production-ready RESTful APIs using Django REST Framework with serializers, viewsets, and authentication.',
                'content': (
                    "<h2>Introduction</h2>"
                    "<p>Django REST Framework (DRF) is a powerful toolkit for building Web APIs. "
                    "In this article, we'll walk through creating a complete RESTful API from scratch.</p>"
                    "<h2>Setting Up the Project</h2>"
                    "<p>First, install DRF:</p>"
                    "<pre><code>pip install djangorestframework</code></pre>"
                    "<p>Add it to your INSTALLED_APPS in settings.py:</p>"
                    "<pre><code>INSTALLED_APPS = [\n    ...\n    'rest_framework',\n]</code></pre>"
                    "<h2>Creating Serializers</h2>"
                    "<p>Serializers convert complex data types like querysets and model instances to native Python datatypes "
                    "that can then be rendered into JSON, XML, or other content types.</p>"
                    "<h2>Building Views</h2>"
                    "<p>DRF provides several ways to define views: function-based views, class-based views, "
                    "generic views, and viewsets. Choose based on your needs.</p>"
                    "<h2>Conclusion</h2>"
                    "<p>DRF is an excellent choice for building APIs in Django. Its built-in features for "
                    "authentication, serialization, and browsable API make development efficient and enjoyable.</p>"
                ),
                'tags': ['django', 'rest-api', 'python', 'tutorial'],
            },
            {
                'title': 'Django Query Optimization: Avoiding N+1 Queries',
                'slug': 'django-query-optimization-avoiding-n-plus-1',
                'category': categories['Django'],
                'excerpt': 'Learn how to identify and fix N+1 query problems in Django using select_related and prefetch_related.',
                'content': (
                    "<h2>The N+1 Problem</h2>"
                    "<p>One of the most common performance issues in Django applications is the N+1 query problem. "
                    "This happens when you access related objects in a loop without prefetching them.</p>"
                    "<h2>Using select_related</h2>"
                    "<p>Use <code>select_related</code> for ForeignKey and OneToOneField relationships. "
                    "It performs a SQL JOIN and includes related objects in a single query.</p>"
                    "<pre><code># Bad: N+1 queries\nfor post in BlogPost.objects.all():\n    print(post.author.username)\n\n"
                    "# Good: 1 query with JOIN\nfor post in BlogPost.objects.select_related('author'):\n    print(post.author.username)</code></pre>"
                    "<h2>Using prefetch_related</h2>"
                    "<p>Use <code>prefetch_related</code> for ManyToManyField and reverse ForeignKey relationships. "
                    "It performs separate lookups and joins them in Python.</p>"
                    "<h2>Monitoring Queries</h2>"
                    "<p>Use Django Debug Toolbar or logging to monitor your query count during development.</p>"
                ),
                'tags': ['django', 'python', 'advanced'],
            },
            {
                'title': 'Deploying Django with Docker and Nginx',
                'slug': 'deploying-django-docker-nginx',
                'category': categories['DevOps'],
                'excerpt': 'Step-by-step guide to containerizing your Django application with Docker and deploying it behind Nginx reverse proxy.',
                'content': (
                    "<h2>Why Docker?</h2>"
                    "<p>Docker ensures consistency between development and production environments. "
                    "Your application runs the same way everywhere.</p>"
                    "<h2>Creating the Dockerfile</h2>"
                    "<p>Start with a multi-stage Dockerfile for optimal image size:</p>"
                    "<pre><code>FROM python:3.12-slim\n\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\n\nCMD [\"gunicorn\", \"core.wsgi:application\", \"--bind\", \"0.0.0.0:8000\"]</code></pre>"
                    "<h2>Docker Compose</h2>"
                    "<p>Use Docker Compose to orchestrate Django, PostgreSQL, Redis, and Nginx:</p>"
                    "<h2>Nginx Configuration</h2>"
                    "<p>Configure Nginx as a reverse proxy to serve static files and forward requests to Gunicorn.</p>"
                    "<h2>Conclusion</h2>"
                    "<p>With Docker and Nginx, you have a production-ready deployment setup that's easy to maintain and scale.</p>"
                ),
                'tags': ['docker', 'deployment', 'django', 'tutorial'],
            },
        ]

        for post_data in posts_data:
            post_tags = [tags[t] for t in post_data.pop('tags')]
            category = post_data.pop('category')
            post, created = BlogPost.objects.get_or_create(
                slug=post_data['slug'],
                defaults={
                    **post_data,
                    'author': author,
                    'category': category,
                    'is_published': True,
                    'published_at': timezone.now(),
                },
            )
            if created:
                post.tags.set(post_tags)

        self.stdout.write("  [OK] Blog posts")

