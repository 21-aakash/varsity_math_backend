from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, courses, assignments, study_materials, quizzes, enrollments

app = FastAPI(title="Varsity Website API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(courses.router, prefix="/courses", tags=["Courses"])
app.include_router(assignments.router, prefix="/assignments", tags=["Assignments"])
app.include_router(study_materials.router, prefix="/study-materials", tags=["Study Materials"])
app.include_router(quizzes.router, prefix="/quizzes", tags=["Quizzes"])
app.include_router(enrollments.router, prefix="/enrollments", tags=["Enrollments"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Varsity Website API"}