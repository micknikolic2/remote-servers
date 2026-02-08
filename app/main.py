import os

from fastapi import FastAPI, Request, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.bookings import router as bookings_router
from app.listings import router as listings_router
from app.machines import router as machines_router
from app.payments import router as payments_router
from app.benchmarks import router as benchmarks_router
from app.metrics import router as metrics_router


from app.auth import optional_user



# This is the entrypoint of the FastAPI application
# It defines the API routes, page routes (templating with Jinja2), 
# CORS configuration for cross origin requests, and cookie-based session handlings

app = FastAPI(title="Remote Servers Marketplace", version="0.3")

FRONTEND_ORIGIN = "https://remote-servers-marketplace-test.onrender.com"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_ORIGIN,
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(machines_router, prefix="/api/v1/machines", tags=["machines"])
app.include_router(benchmarks_router, prefix="/api/v1/benchmarks", tags=["benchmarks"])
app.include_router(metrics_router, prefix="/api/v1/metrics", tags=["metrics"])
app.include_router(listings_router, prefix="/api/v1/listings", tags=["listings"])
app.include_router(bookings_router, prefix="/api/v1/bookings", tags=["bookings"])
app.include_router(payments_router, prefix="/api/v1/payments", tags=["payments"])


@app.get("/api/v1/health")
def health():
    return {"status": "ok"}


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
templates_dir = os.path.join(BASE_DIR, "frontend", "templates")
static_dir = os.path.join(BASE_DIR, "frontend", "static")

# NOTE: frontend is not implemented
# templates = Jinja2Templates(directory=templates_dir)
# app.mount("/static", StaticFiles(directory=static_dir), name="static")

class StoreSession(BaseModel):
    token: str


@app.post("/auth/store-session")
async def store_session(payload: StoreSession, response: Response):
    """Supabase gives us a JWT via the frontend.
    This endpoint stores it in an HttpOnly cookie so our 
    server-rendered HTML pages can know the logged-in user."""
    response.set_cookie(
        key="access_token",
        value=payload.token,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/"
    )
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, user=Depends(optional_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request, user=Depends(optional_user)):
    if user:
        return RedirectResponse("/")
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request, user=Depends(optional_user)):
    if user:
        return RedirectResponse("/")
    return templates.TemplateResponse("signup.html", {"request": request})


@app.get("/listings", response_class=HTMLResponse)
async def listings_page(request: Request, user=Depends(optional_user)):
    return templates.TemplateResponse("listings.html", {"request": request, "user": user})


@app.get("/bookings", response_class=HTMLResponse)
async def bookings_page(request: Request, user=Depends(optional_user)):
    if not user:
        return RedirectResponse("/login")
    return templates.TemplateResponse("bookings.html", {"request": request, "user": user})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request, user=Depends(optional_user)):
    if not user:
        return RedirectResponse("/login")
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})


@app.get("/payments/success", response_class=HTMLResponse)
async def payment_success_page(
    request: Request, 
    session_id: str = None, 
    booking_id: str = None,
    amount: float = None,
    currency: str = "USD",
    user=Depends(optional_user)
):
    return templates.TemplateResponse(
        "payment_success.html", 
        {
            "request": request, 
            "user": user,
            "session_id": session_id,
            "booking_id": booking_id,
            "amount": amount,
            "currency": currency
        }
    )

@app.get("/payments/cancel", response_class=HTMLResponse)
async def payment_cancel_page(
    request: Request, 
    booking_id: str = None,
    user=Depends(optional_user)
):
    return templates.TemplateResponse(
        "payment_cancel.html", 
        {
            "request": request, 
            "user": user,
            "booking_id": booking_id
        }
    )


@app.get("/logout")
async def logout():
    response = RedirectResponse("/")
    response.delete_cookie("access_token")
    return response