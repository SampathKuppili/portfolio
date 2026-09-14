# ⚡ DevPortfolio — Modern Developer Portfolio & Tech Blog

A state-of-the-art, high-performance developer portfolio and tech blog platform built with **Django 6**, **Django REST Framework**, **GSAP**, and **Lenis Smooth Scroll**. Features a contemporary glassmorphic aesthetic with organic liquid flow animations, rich interactive showcases, and full dark-mode support.

---

## ✨ Features & Highlights

### 🎨 Visual & Motion Design
- **Liquid Morphing Backgrounds:** Floating, organic SVG blobs with smooth morphing animations.
- **Lenis Momentum Scrolling:** Buttery-smooth, physics-based scrolling synced seamlessly with GSAP ScrollTrigger.
- **Glassmorphism & Glow Effects:** Frosted glass visual hierarchy, mouse-tracking hover glows, and gradient accent borders.
- **Custom Cursor & Micro-Interactions:** Dual-ring interactive cursor with magnetic buttons and 3D card tilt effects.
- **Default Dark Theme:** Dark-first design system with high-contrast typography and instant light/dark toggle persisted via `localStorage`.

### 💼 Portfolio Management
- **Project Showcase:** Display featured & categorized projects with tech stack badges, live demos, and repository links.
- **Skill Proficiency Tracker:** Categorized technical skills with visual proficiency meters and liquid shimmer progress bars.
- **Career Timeline:** Interactive vertical timeline highlighting work experience, education, and achievements.
- **Live Statistics:** Animated counter metrics for completed projects, years of experience, and code metrics.

### ✍️ Tech Blog
- **Full Blogging Engine:** Categorized posts with tag support, estimated reading time, author metadata, and search.
- **Interactive Comments:** Nested comment discussions on blog posts.
- **SEO Ready:** Dynamic title tags, meta descriptions, OpenGraph tags, canonical links, and automated XML sitemaps (`/sitemap.xml`).

### 📬 Contact & API Engine
- **Contact Form:** Dynamic message form with validation and backend storage.
- **Django REST Framework (DRF):** Built-in API endpoints for headless access to projects, skills, blog posts, and contact inquiries with filtering support.

---

## 🛠️ Technology Stack

| Layer | Technologies Used |
| :--- | :--- |
| **Backend** | Python 3.12+, Django 6.0, Django REST Framework, Django Filter, Pillow, Python-Dotenv |
| **Frontend** | HTML5, Modern Vanilla CSS3, JavaScript (ES6+), FontAwesome 6 |
| **Animation & Motion** | GSAP 3 (ScrollTrigger), Lenis Smooth Scroll (`@studio-freight/lenis`) |
| **UI Components** | Crispy Forms (Bootstrap 5 pack), Custom Glassmorphism System |
| **Database** | SQLite (Default / Development), PostgreSQL Ready |

---

## 📁 Project Architecture

```text
portfolio-1/
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
└── src/                        # Main Django source code
    ├── manage.py               # Django CLI management utility
    ├── core/                   # Main project settings, URLs, ASGI/WSGI
    ├── common/                 # Base models, mixins, context processors & site settings
    ├── portfolio/              # Projects, skills, experience & certification models/views
    ├── blog/                   # Blog post, category, tag & comment engine
    ├── contact/                # Contact form handling & message storage
    ├── accounts/               # Custom user profile & authentication
    ├── templates/              # HTML5 Django templates
    └── static/                 # Static assets
        ├── css/                # Main stylesheet (Glassmorphism, animations, dark mode)
        ├── js/                 # Main JS (GSAP ScrollTrigger, Lenis, magnetic buttons, cursor)
        └── images/             # Static graphics and icons
```

---

## 🚀 Getting Started

Follow these steps to get the project up and running on your local machine.

### 1. Prerequisites
- **Python 3.10+** installed
- **Git** installed

### 2. Clone the Repository
```bash
git clone https://github.com/SampathKuppili/portfolio.git
cd portfolio
```

### 3. Create & Activate Virtual Environment

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables
Copy the example environment configuration file:
```bash
cd src
cp .env.example .env
```
*(Optionally adjust `SECRET_KEY`, `DEBUG`, or database credentials inside `src/.env`)*

### 6. Apply Database Migrations
```bash
python manage.py migrate
```

### 7. Create an Admin User
```bash
python manage.py createsuperuser
```

### 8. Run the Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to `http://127.0.0.1:8000/`.  
Access the Django Admin panel at `http://127.0.0.1:8000/admin/`.

---

## 🌐 REST API Endpoints

The backend provides public/authenticated API endpoints powered by **Django REST Framework**:

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/projects/` | List all portfolio projects (supports filtering by category) |
| `GET` | `/api/skills/` | List all technical skills |
| `GET` | `/api/posts/` | List published blog posts |
| `POST` | `/api/contact/` | Submit a new contact message |

---

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for details.

---

Designed & Developed by **[Sampath Kuppili](https://github.com/SampathKuppili)**
