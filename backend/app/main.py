# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from .routers import auth, complaints

app = FastAPI(
    title="Complaint Triage System",
    description="AI-powered complaint management with admin dashboard",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(complaints.router)


if os.path.exists("../frontend/static"):
    app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Complaint Triage System API",
        "docs": "/docs",
        "admin_dashboard": "/admin",
        "submit_complaint": "/public"
    }


@app.get("/admin")
def admin_dashboard():
    """Admin dashboard HTML"""
    if os.path.exists("../frontend/static/admin.html"):
        return FileResponse("../frontend/static/admin.html")
    return {"message": "Admin dashboard not found"}


@app.get("/public")
def public_form():
    """Public complaint submission form"""
    if os.path.exists("../frontend/static/public.html"):
        return FileResponse("../frontend/static/public.html")
    return {"message": "Public form not found"}
