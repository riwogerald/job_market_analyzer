# Kenya Job Market Analysis Platform

A comprehensive job market analysis platform that scrapes job postings from major job sites (LinkedIn, Indeed, Glassdoor) and provides real-time insights into the Kenyan job market including salary trends, skill demand, remote work opportunities, and hiring patterns.

## 🚀 Features

- **Multi-Platform Job Scraping**: Automated scraping from LinkedIn, Indeed, Glassdoor, and company career pages
- **Real-time Analytics**: Live dashboards showing market trends, salary insights, and hiring patterns
- **Advanced Search & Filtering**: Comprehensive job search with location, salary, skills, and experience filters
- **Skill Demand Analysis**: Track the most in-demand skills and their market value
- **Remote Work Trends**: Monitor remote/hybrid work opportunities across industries
- **Company Insights**: Analysis of top hiring companies and industry distributions
- **Interactive Charts**: Dynamic visualizations using Recharts for data presentation
- **Background Processing**: Automated data collection using Celery with Redis
- **RESTful API**: Complete API for integration with external applications

## 🏗️ Project Structure

```
job_market_analyzer/
├── backend/                          # Django Backend
│   ├── job_analyzer/                 # Main Django project
│   │   ├── __init__.py
│   │   ├── settings.py              # Django settings
│   │   ├── urls.py                  # Main URL configuration
│   │   ├── wsgi.py                  # WSGI configuration
│   │   └── celery.py                # Celery configuration
│   ├── apps/                        # Django applications
│   │   ├── jobs/                    # Job posting models and logic
│   │   │   ├── models.py            # Database models (JobPosting, Company, etc.)
│   │   │   ├── admin.py             # Django admin configuration
│   │   │   └── migrations/          # Database migrations
│   │   ├── analytics/               # Analytics and insights
│   │   │   ├── services.py          # Analytics service classes
│   │   │   └── utils.py             # Analytics utility functions
│   │   ├── scrapers/                # Web scraping modules
│   │   │   ├── base_scraper.py      # Base scraper class
│   │   │   ├── linkedin_scraper.py  # LinkedIn scraping logic
│   │   │   ├── indeed_scraper.py    # Indeed scraping logic
│   │   │   └── tasks.py             # Celery tasks for scraping
│   │   └── api/                     # REST API
│   │       ├── views.py             # API endpoints
│   │       ├── serializers.py       # Data serialization
│   │       └── urls.py              # API URL routing
│   ├── requirements.txt             # Python dependencies
│   ├── manage.py                    # Django management script
│   └── Dockerfile                   # Backend Docker configuration
├── frontend/                        # React TypeScript Frontend
│   ├── src/
│   │   ├── components/              # React components
│   │   │   ├── Dashboard/           # Dashboard components
│   │   │   ├── Charts/              # Chart components
│   │   │   ├── Jobs/                # Job-related components
│   │   │   └── Common/              # Shared components
│   │   ├── services/                # API service layer
│   │   │   └── api.ts               # API client configuration
│   │   ├── types/                   # TypeScript type definitions
│   │   │   └── index.ts             # Main type definitions
│   │   ├── utils/                   # Utility functions
│   │   │   └── formatters.ts        # Data formatting utilities
│   │   ├── App.tsx                  # Main App component
│   │   └── index.tsx                # Application entry point
│   ├── package.json                 # Node.js dependencies
│   ├── tsconfig.json                # TypeScript configuration
│   └── Dockerfile                   # Frontend Docker configuration
├── docker-compose.yml               # Multi-container Docker setup
├── .env.example                     # Environment variables template
└── README.md                        # Project documentation
```

## 📋 Prerequisites

Before running this project, ensure you have the following installed:

- **Python 3.9+**
- **Node.js 16+** and **npm/yarn**
- **PostgreSQL 12+**
- **Redis 6+**
- **Google Chrome** (for Selenium web scraping)
- **ChromeDriver** (for Selenium web scraping)
- **Docker & Docker Compose** (optional, for containerized deployment)

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/job-market-analyzer.git
cd job-market-analyzer
```

### 2. Backend Setup

#### Create Virtual Environment

```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

#### Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### Install ChromeDriver

```bash
# On macOS using Homebrew
brew install chromedriver

# On Ubuntu/Debian
sudo apt-get install chromium-chromedriver

# On Windows
# Download from https://chromedriver.chromium.org/
# Add to PATH
```

#### Database Setup

```bash
# Create PostgreSQL database
createdb job_analyzer

# Or using PostgreSQL command line
psql -c "CREATE DATABASE job_analyzer;"
```

#### Environment Configuration

Create a `.env` file in the backend directory:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=job_analyzer
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/0
DOMAIN=localhost
```

#### Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

#### Create Superuser

```bash
python manage.py createsuperuser
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

Create frontend environment file:

```bash
# Create .env file
echo "REACT_APP_API_URL=http://localhost:8000/api" > .env
```

## 🚀 Running the Project

### Development Mode

#### Option 1: Manual Setup

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python manage.py runserver
```

**Terminal 2 - Celery Worker:**
```bash
cd backend
source venv/bin/activate
celery -A job_analyzer worker --loglevel=info
```

**Terminal 3 - Celery Beat (Scheduler):**
```bash
cd backend
source venv/bin/activate
celery -A job_analyzer beat --loglevel=info
```

**Terminal 4 - Frontend:**
```bash
cd frontend
npm start
```

**Terminal 5 - Redis:**
```bash
redis-server
```

#### Option 2: Docker Compose (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production Deployment

#### Using Docker Compose for Production

1. **Update environment variables:**

```bash
# Create production .env file
cp .env.example .env.prod
```

Edit `.env.prod`:
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
DB_NAME=job_analyzer_prod
DB_USER=postgres
DB_PASSWORD=secure-password
DB_HOST=db
REDIS_URL=redis://redis:6379/0
DOMAIN=yourdomain.com
```

2. **Create production docker-compose file:**

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: job_analyzer_prod
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secure-password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped

  backend:
    build: ./backend
    command: gunicorn job_analyzer.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - ./backend:/app
      - static_volume:/app/staticfiles
    expose:
      - 8000
    depends_on:
      - db
      - redis
    env_file:
      - .env.prod
    restart: unless-stopped

  celery:
    build: ./backend
    command: celery -A job_analyzer worker --loglevel=info
    volumes:
      - ./backend:/app
    depends_on:
      - db
      - redis
    env_file:
      - .env.prod
    restart: unless-stopped

  celery-beat:
    build: ./backend
    command: celery -A job_analyzer beat --loglevel=info
    volumes:
      - ./backend:/app
    depends_on:
      - db
      - redis
    env_file:
      - .env.prod
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - 80:80
      - 443:443
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - ./frontend/build:/usr/share/nginx/html
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
  static_volume:
```

3. **Deploy:**

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

## 📊 Database Schema

### Key Models

**JobPosting**
- Core job information (title, description, requirements)
- Company relationship
- Location and remote work details
- Salary information
- Skills and technologies
- Source tracking (platform, URL, external ID)

**Company**
- Company information (name, industry, size)
- Location and website details
- Relationship to job postings

**SkillDemand**
- Skill popularity tracking
- Average salary by skill
- Growth rate analysis

**SalaryInsight**
- Salary data aggregation
- Experience level correlation
- Location-based salary trends

## 🔄 Celery Tasks & Scheduling

### Available Tasks

1. **scrape_all_platforms**: Main task that triggers scraping from all job platforms
2. **scrape_linkedin_jobs**: Specific LinkedIn scraping task
3. **scrape_indeed_jobs**: Specific Indeed scraping task
4. **update_skill_demand**: Refresh skill demand analytics
5. **cleanup_old_jobs**: Remove outdated job postings

### Default Schedule

- **Daily at 6:00 AM**: Full platform scraping
- **Daily at 2:00 AM**: Skill demand analysis update
- **Weekly on Sunday at 1:00 AM**: Cleanup old job postings

### Manual Task Execution

```bash
# Run specific scraping task
python manage.py shell
>>> from apps.scrapers.tasks import scrape_linkedin_jobs
>>> scrape_linkedin_jobs.delay("software engineer", "Nairobi")

# Or via Django admin trigger
# Visit http://localhost:8000/admin/ and use the admin interface
```

## 🔌 API Endpoints

### Job Endpoints

```
GET /api/jobs/                    # List jobs with filtering
GET /api/jobs/{id}/              # Get specific job details
GET /api/companies/              # List companies
GET /api/skills/                 # List skills demand
GET /api/skills/top/             # Get top skills
```

### Analytics Endpoints

```
GET /api/analytics/market-overview/           # Overall market statistics
GET /api/analytics/location-distribution/     # Jobs by location
GET /api/analytics/experience-distribution/   # Jobs by experience level
GET /api/analytics/employment-type-distribution/ # Jobs by employment type
GET /api/analytics/remote-work-trends/        # Remote work trends over time
GET /api/analytics/salary-insights/           # Salary analysis
GET /api/analytics/hiring-trends/             # Hiring trends over time
GET /api/analytics/industry-insights/         # Industry-wise analysis
```

### Query Parameters

**Job Search:**
```
?search=python developer
&location=nairobi
&employment_type=full_time
&experience_level=mid
&remote_type=remote
&min_salary=50000
&max_salary=150000
&skills=python,django
&page=1
&page_size=20
```

## 🎨 Frontend Features

### Components Overview

1. **Dashboard**: Main analytics dashboard with key metrics
2. **JobSearch**: Advanced search and filtering interface
3. **JobList**: Paginated job listings with filters
4. **Charts**: Interactive data visualizations
5. **MarketOverview**: Key market statistics cards

### Chart Types

- **Bar Charts**: Location distribution, skill demand
- **Line Charts**: Hiring trends over time
- **Pie Charts**: Employment type distribution
- **Area Charts**: Remote work trends

## 🔧 Configuration

### Backend Configuration

Key settings in `backend/job_analyzer/settings.py`:

```python
# Scraping Configuration
SCRAPING_DELAY = 2  # Seconds between requests
USER_AGENT_LIST = [...]  # Rotating user agents

# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # ... other settings
    }
}
```

### Frontend Configuration

Environment variables in `frontend/.env`:

```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_VERSION=1.0.0
```

## 🐛 Troubleshooting

### Common Issues

**1. Selenium/ChromeDriver Issues:**
```bash
# Ensure ChromeDriver is in PATH
which chromedriver

# Update ChromeDriver to match Chrome version
brew upgrade chromedriver  # macOS
```

**2. Database Connection Issues:**
```bash
# Check PostgreSQL is running
sudo service postgresql status

# Check database exists
psql -l | grep job_analyzer
```

**3. Redis Connection Issues:**
```bash
# Check Redis is running
redis-cli ping
# Should return "PONG"
```

**4. Celery Worker Issues:**
```bash
# Check Celery can connect to Redis
celery -A job_analyzer inspect ping

# Monitor Celery tasks
celery -A job_analyzer events
```

**5. CORS Issues:**
```python
# In settings.py, ensure frontend URL is in CORS_ALLOWED_ORIGINS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
```

### Debugging Tips

**Enable Django Debug Mode:**
```bash
export DEBUG=True
python manage.py runserver
```

**Check Celery Task Status:**
```python
# In Django shell
from apps.scrapers.tasks import scrape_linkedin_jobs
result = scrape_linkedin_jobs.delay("software engineer", "Nairobi")
print(result.status)
print(result.result)
```

**Monitor Database Queries:**
```python
# In settings.py for development
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
```

## 📈 Performance Optimization

### Backend Optimizations

1. **Database Indexing**: Key indexes on frequently queried fields
2. **Query Optimization**: Use `select_related()` and `prefetch_related()`
3. **Caching**: Redis caching for expensive analytics queries
4. **Pagination**: Limit API response sizes

### Frontend Optimizations

1. **Code Splitting**: Dynamic imports for route-based splitting
2. **Memoization**: React.memo and useMemo for expensive components
3. **Debouncing**: Search input debouncing to reduce API calls
4. **Virtual Scrolling**: For large job listings

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Create Pull Request**

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for all frontend code
- Write tests for new features
- Update documentation for API changes
- Use meaningful commit messages

### Code Style

**Python:**
```bash
# Format with black
black backend/

# Lint with flake8
flake8 backend/
```

**TypeScript:**
```bash
# Format with prettier
npm run format

# Lint with ESLint
npm run lint
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:

- **Issues**: [GitHub Issues](https://github.com/yourusername/job-market-analyzer/issues)
- **Email**: support@jobmarketanalyzer.com
- **Documentation**: [Project Wiki](https://github.com/yourusername/job-market-analyzer/wiki)

## 🚀 Roadmap

- [ ] **Additional Job Sites**: CareerBuilder, Glassdoor integration
- [ ] **Email Alerts**: Job alert subscriptions
- [ ] **Machine Learning**: Job recommendation engine
- [ ] **Mobile App**: React Native mobile application
- [ ] **Advanced Analytics**: Predictive hiring trends
- [ ] **Company Profiles**: Detailed company analysis pages
- [ ] **Salary Negotiation**: Salary negotiation insights
- [ ] **API Keys**: Third-party API access management

---

**Built with ❤️ for the Kenyan job market**
