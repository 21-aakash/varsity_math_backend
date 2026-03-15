# Varsity Website Backend API

A comprehensive FastAPI-based backend for the Varsity Maths educational platform, providing authentication, course management, assignments, quizzes, study materials, and enrollment functionality.

## 🚀 Features

- **Authentication & Authorization**: JWT-based authentication with role-based access control
- **User Management**: Student, faculty, and admin user roles
- **Course Management**: Create and manage educational courses
- **Assignments**: Upload and manage course assignments
- **Study Materials**: Store and distribute learning resources
- **Quizzes**: Create and manage interactive quizzes
- **Enrollment System**: Student course enrollment with payment tracking
- **Database**: SQLite with SQLAlchemy ORM and Alembic migrations

## 📁 Directory Structure

```
backend/
├── .env                    # Environment variables
├── alembic/               # Database migration files
│   ├── env.py
│   ├── script.py.mako
│   └── versions/          # Migration scripts
├── app/                   # Main application code
│   ├── __init__.py
│   ├── main.py           # FastAPI application entry point
│   ├── config/           # Configuration settings
│   │   └── database.py   # Database configuration
│   ├── dependencies/     # Dependency injection
│   │   └── auth.py       # Authentication dependencies
│   ├── models/           # SQLAlchemy models
│   │   ├── base.py       # Base model class
│   │   ├── user.py       # User model
│   │   ├── course.py     # Course model
│   │   ├── assignment.py # Assignment model
│   │   ├── quiz.py       # Quiz model
│   │   ├── study_material.py # Study material model
│   │   └── enrollment.py # Enrollment model
│   ├── routers/          # API route handlers
│   │   ├── auth.py       # Authentication routes
│   │   ├── users.py      # User management routes
│   │   ├── courses.py    # Course management routes
│   │   ├── assignments.py # Assignment routes
│   │   ├── quizzes.py    # Quiz routes
│   │   ├── study_materials.py # Study material routes
│   │   └── enrollments.py # Enrollment routes
│   └── schemas/          # Pydantic schemas
│       ├── user.py       # User schemas
│       ├── course.py     # Course schemas
│       ├── assignment.py # Assignment schemas
│       ├── quiz.py       # Quiz schemas
│       ├── study_material.py # Study material schemas
│       └── enrollment.py # Enrollment schemas
├── requirements.txt      # Python dependencies
├── run.py               # Server startup script
├── varsity.db           # SQLite database file
└── tests/               # Test files
```

## 🏗️ Architecture

### Models (SQLAlchemy)

The backend uses SQLAlchemy ORM with the following models:

#### User Model
```python
class User(Base):
    id: int (Primary Key)
    email: str (Unique)
    hashed_password: str
    full_name: str
    is_active: bool (Default: True)
    role: str (student/faculty/admin, Default: student)
    created_at: datetime
    updated_at: datetime
```

#### Course Model
```python
class Course(Base):
    id: int (Primary Key)
    title: str
    description: str
    instructor_id: int (Foreign Key to User)
    created_at: datetime
    updated_at: datetime
```

#### Assignment Model
```python
class Assignment(Base):
    id: int (Primary Key)
    title: str
    description: str
    course_id: int (Foreign Key to Course)
    due_date: datetime
    created_at: datetime
    updated_at: datetime
```

#### Quiz Model
```python
class Quiz(Base):
    id: int (Primary Key)
    title: str
    description: str
    course_id: int (Foreign Key to Course)
    questions: str (JSON)
    created_at: datetime
    updated_at: datetime
```

#### StudyMaterial Model
```python
class StudyMaterial(Base):
    id: int (Primary Key)
    title: str
    description: str
    file_url: str
    course_id: int (Foreign Key to Course)
    created_at: datetime
    updated_at: datetime
```

#### Enrollment Model
```python
class Enrollment(Base):
    id: int (Primary Key)
    user_id: int (Foreign Key to User)
    course_id: int (Foreign Key to Course)
    first_name: str
    last_name: str
    phone: str
    payment_method: str (online/offline)
    payment_screenshot_url: str (Optional)
    profile_image_url: str (Optional)
    status: str (pending/approved/rejected, Default: pending)
    created_at: datetime
    updated_at: datetime
```

### API Routes

#### Authentication (`/auth`)
- `POST /auth/register` - User registration
- `POST /auth/login` - User login (OAuth2)

#### Users (`/users`)
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update current user profile

#### Courses (`/courses`)
- `GET /courses` - List all courses
- `POST /courses` - Create new course (faculty/admin only)
- `GET /courses/{course_id}` - Get course details
- `PUT /courses/{course_id}` - Update course (faculty/admin only)

#### Assignments (`/assignments`)
- `GET /assignments` - List assignments (with optional course_id filter)
- `POST /assignments` - Create assignment (faculty/admin only)
- `GET /assignments/{assignment_id}` - Get assignment details
- `PUT /assignments/{assignment_id}` - Update assignment (faculty/admin only)

#### Study Materials (`/study-materials`)
- `GET /study-materials` - List study materials (with optional course_id filter)
- `POST /study-materials` - Upload study material (faculty/admin only)
- `GET /study-materials/{material_id}` - Get material details
- `PUT /study-materials/{material_id}` - Update material (faculty/admin only)

#### Quizzes (`/quizzes`)
- `GET /quizzes` - List quizzes (with optional course_id filter)
- `POST /quizzes` - Create quiz (faculty/admin only)
- `GET /quizzes/{quiz_id}` - Get quiz details
- `PUT /quizzes/{quiz_id}` - Update quiz (faculty/admin only)

#### Enrollments (`/enrollments`)
- `GET /enrollments` - List user enrollments
- `POST /enrollments` - Create enrollment
- `GET /enrollments/{enrollment_id}` - Get enrollment details
- `PUT /enrollments/{enrollment_id}` - Update enrollment

## 🔧 Setup & Installation

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone the repository and navigate to backend directory:**
   ```bash
   cd varsity_website/backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the backend directory:
   ```env
   DATABASE_URL=sqlite+aiosqlite:///./varsity.db
   SECRET_KEY=your-secret-key-here
   ```

5. **Run database migrations:**
   ```bash
   python -m alembic upgrade head
   ```

6. **Start the server:**
   ```bash
   python run.py
   ```

   The API will be available at `http://localhost:8001`

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Register/Login** to get an access token
2. **Include token** in Authorization header: `Bearer <token>`
3. **Token expires** after 30 minutes (configurable)

### User Roles
- **student**: Can view courses, enroll, access study materials
- **faculty**: Can create/manage courses, assignments, materials, quizzes
- **admin**: Full access including user management

## 🗄️ Database

### SQLite Configuration
- **File**: `varsity.db` (created automatically)
- **Driver**: aiosqlite for async operations
- **Migrations**: Managed by Alembic

### Switching to PostgreSQL
To use PostgreSQL instead of SQLite:

1. Update `DATABASE_URL` in `.env`:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost/varsity_db
   ```

2. Install PostgreSQL driver:
   ```bash
   pip install asyncpg
   ```

3. Update `alembic.ini`:
   ```ini
   sqlalchemy.url = postgresql+asyncpg://user:password@localhost/varsity_db
   ```

## 🧪 Testing

Run tests with:
```bash
python -m pytest tests/
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8001/docs`
- **ReDoc**: `http://localhost:8001/redoc`

## 🔄 Development Workflow

1. **Make model changes** in `app/models/`
2. **Generate migration**:
   ```bash
   python -m alembic revision --autogenerate -m "description"
   ```
3. **Apply migration**:
   ```bash
   python -m alembic upgrade head
   ```
4. **Update schemas** in `app/schemas/` if needed
5. **Add routes** in `app/routers/`
6. **Include router** in `app/main.py`

## 🚀 Deployment

### Quick Deploy Options

#### Railway (Easiest - Recommended)
1. **Connect your GitHub repo** to [Railway](https://railway.app)
2. **Railway auto-detects** the `railway.toml` config
3. **Add environment variables** from `.env.production`
4. **Deploy** - Done! 🚀

#### Render (Free tier available)
1. **Create PostgreSQL Database:**
   - Go to Render Dashboard → New → PostgreSQL
   - Choose free tier, name it (e.g., `varsity-db`)
   - Create database

2. **Create Web Service:**
   - New → Web Service
   - Connect your GitHub repository
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python -m alembic upgrade head`
   - **Start Command**: `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

3. **Add Environment Variables:**
   - `DATABASE_URL`: Copy from PostgreSQL "External Database URL"
   - `SECRET_KEY`: Generate a strong random key
   - `ENVIRONMENT`: production

4. **Deploy!** 🚀

#### Manual Deployment
```bash
# Linux/Mac
./deploy.sh

# Windows
deploy.bat
```

### Production Considerations
- ✅ CORS configured for `https://varsitymath.netlify.app`
- ✅ Environment variables for sensitive data
- ✅ Production-grade database (PostgreSQL recommended)
- ✅ Health check endpoint at `/health`
- ✅ Docker support with provided Dockerfile
- ✅ Heroku support with Procfile

### Environment Variables for Production

Copy these from `.env.production` to your deployment platform:

```env
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database
SECRET_KEY=your-super-secret-key-change-this-in-production
ENVIRONMENT=production
```

### Database Setup for Production

#### PostgreSQL Configuration
The app automatically detects and uses PostgreSQL when you set the `DATABASE_URL` environment variable.

**Example PostgreSQL URL:**
```
postgresql://username:password@host:port/database_name
```

#### Testing Database Connection
Before deploying, test your database connection:

**Windows:**
```cmd
test-db.bat
```

**Linux/Mac:**
```bash
./test-db.sh
```

This will:
- ✅ Test database connectivity
- 🗄️ Run migrations automatically
- 📊 Verify all tables are created

1. **Create PostgreSQL database** on your hosting platform
2. **Update DATABASE_URL** in environment variables
3. **Deploy** - migrations run automatically

### Docker Deployment
```bash
# Build and run with gunicorn
docker build -t varsity-backend .
docker run -p 8001:8001 varsity-backend
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with proper tests
4. Run migrations if models changed
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.