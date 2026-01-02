# backend/app/routers/complaints.py
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List

from ..email_service import send_email
from ..database import get_db
from ..models import Complaint
from ..auth import get_current_admin
from ..schemas import ComplaintCreate, ComplaintResponse
from ..agent import ai_agent
from ..ai_reply import generate_reply

router = APIRouter(prefix="/complaints", tags=["complaints"])


@router.post("/submit")
def submit_complaint(payload: ComplaintCreate, db: Session = Depends(get_db)):
    """Public endpoint for submitting complaints"""
    
    if not payload.text or len(payload.text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Complaint text too short (min 10 characters)")
    
    try:
        print(f"📝 Analyzing complaint: {payload.text[:50]}...")
        analysis = ai_agent(payload.text)
        
        new_complaint = Complaint(
            customer_name=payload.customer_name,
            email=payload.email,
            text=payload.text,
            category=analysis.get("category", "other"),
            severity=analysis.get("priority", "medium"),
            notes=analysis.get("summary", ""),
            status="open"
        )
        
        db.add(new_complaint)
        db.commit()
        db.refresh(new_complaint)
        
        print(f"✅ Complaint saved with ID: {new_complaint.id}")
        
        return {
            "success": True,
            "message": "Complaint submitted successfully",
            "complaint_id": new_complaint.id,
            "analysis": {
                "category": new_complaint.category,
                "severity": new_complaint.severity,
                "summary": new_complaint.notes,
                "sentiment": analysis.get("sentiment", "neutral")
            }
        }
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        
        # Still save complaint even if AI fails
        new_complaint = Complaint(
            customer_name=payload.customer_name,
            email=payload.email,
            text=payload.text,
            category="other",
            severity="medium",
            notes="Pending analysis",
            status="open"
        )
        db.add(new_complaint)
        db.commit()
        db.refresh(new_complaint)
        
        return {
            "success": True,
            "message": "Complaint submitted (AI analysis pending)",
            "complaint_id": new_complaint.id,
            "warning": "AI analysis failed but complaint was saved"
        }


@router.get("/", response_model=List[ComplaintResponse])
def get_all_complaints(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    """Get all complaints (admin only)"""
    complaints = db.query(Complaint).order_by(Complaint.created_at.desc()).all()
    return complaints


@router.get("/{complaint_id}", response_model=ComplaintResponse)
def get_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    """Get single complaint details"""
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint


@router.get("/stats/summary")
def get_stats(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    """Get dashboard statistics"""
    complaints = db.query(Complaint).all()
    
    total = len(complaints)
    open_count = sum(1 for c in complaints if c.status == "open")
    high_priority = sum(1 for c in complaints if c.severity == "high")
    
    category_stats = {}
    for c in complaints:
        if c.category:
            category_stats[c.category] = category_stats.get(c.category, 0) + 1
    
    return {
        "total_complaints": total,
        "open_complaints": open_count,
        "high_priority": high_priority,
        "by_category": category_stats
    }


@router.patch("/{complaint_id}/status")
def update_status(
    complaint_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    """Update complaint status"""
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    valid_statuses = ["open", "in_progress", "resolved", "closed"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be: {valid_statuses}")
    
    complaint.status = status
    db.commit()
    
    return {
        "success": True,
        "message": "Status updated",
        "complaint_id": complaint_id,
        "status": status
    }


@router.delete("/{complaint_id}")
def delete_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    """Delete complaint"""
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    db.delete(complaint)
    db.commit()
    
    return {
        "success": True,
        "message": "Complaint deleted",
        "complaint_id": complaint_id
    }


@router.post("/{complaint_id}/reply")
def generate_ai_reply(
    complaint_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    """Generate AI draft reply"""
    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")
    
    try:
        print(f"📝 Generating reply for complaint {complaint_id}...")
        
        reply = generate_reply(
            complaint.text,
            complaint.category or "general",
            complaint.severity or "medium"
        )
        
        complaint.draft_reply = reply
        db.commit()
        
        return {
            "success": True,
            "complaint_id": complaint_id,
            "draft_reply": reply
        }
        
    except Exception as e:
        print(f"❌ Reply generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Reply generation failed: {str(e)}")

@router.post("/{complaint_id}/send_reply")
def send_reply(
    complaint_id: int,
    reply_text: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    print("🔥 SEND_REPLY HIT")
    print("🔥 complaint_id:", complaint_id)
    print("🔥 reply_text:", reply_text)

    complaint = db.query(Complaint).filter(Complaint.id == complaint_id).first()
    if not complaint:
        raise HTTPException(status_code=404, detail="Complaint not found")

    success = send_email(
        to_email=complaint.email,
        subject=f"Reply to your complaint #{complaint.id}",
        content=reply_text
    )

    if not success:
        raise HTTPException(status_code=500, detail="Email sending failed")

    complaint.status = "resolved"
    complaint.draft_reply = reply_text
    db.commit()

    return {"success": True}