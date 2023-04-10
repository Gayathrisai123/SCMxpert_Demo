from typing import Dict, Optional
from fastapi.logger import logger
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import  Form, Request, HTTPException, status, Depends, Response, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2, OAuth2PasswordRequestForm
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from passlib.context import CryptContext
import pymongo
from config.config import settings
from schema.schema import User
from auth.oauth2 import LoginForm,get_current_user_from_cookie,login_for_access_token
from passlib.context import CryptContext



router = APIRouter()

router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)



# serves the Indexpage of the web application.

@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    try:
        user = get_current_user_from_cookie(request)
    except ValueError: 
        user = None
        raise HTTPException()
    context = {"user": user,  "request": request}
    # The rendered template is wrapped in a 'TemplateResponse' which includes the HTTP response headers.
    return templates.TemplateResponse("index.html",context)



# this variable server the login page 
Login_template = "login.html"

# variable for mongodb collection
client = settings.client

User_collection =settings.user_collection

# serves the login form page.

@router.get("/login", response_class=HTMLResponse)
def login_view(request: Request):       
    # It expects a GET request and renders the 'Login_template' 
    return templates.TemplateResponse(Login_template, {"request": request} ,status_code=200)


#  Handles the login form submission.

@router.post("/login", response_class=HTMLResponse)
async def login(request: Request):
      # It expects a POST request with the user's email and password as form data.
       form = LoginForm(request)    
       await form.load_data()    
       if await form.is_valid():
            try:
                # It validates the form data and generates a new access token if it is valid,
                #  then redirects to the indexpage.
                response = RedirectResponse("/", status.HTTP_302_FOUND)
                login_for_access_token(response=response, form_data=form)
                form.__dict__.update(msg="Login Successful!")
                return response
            except HTTPException :               
         # If the form data is not valid, it catches a 400 Bad Request exceptionand displays an error message.            
                form.__dict__.update(msg="")
                form.__dict__.get("errors").append("Incorrect Email or Password")
                # return templates.TemplateResponse(Login_template, form.__dict__)
                return templates.TemplateResponse(Login_template, {"request":request, "alert": "Invalid username or password " },status_code=401)
        

# serves the sign-up form page.

@router.get("/signup", response_class=HTMLResponse)
def signup_view(request: Request):   
        # It expects a GET request and renders the 'signup_page.html' template.
        return templates.TemplateResponse("signup_page.html", {"request": request})
    

# Handles the sign-up form submission.

@router.post("/signup", response_class=HTMLResponse)
def signup(request: Request, username: str = Form(...), email: str = Form(...),password: str = Form(...), cpassword: str = Form(...)):
   
    try: 
        hashed_password = hash_password(password)
        user = User(Username=username, Email=email, Password=hashed_password, CPassword=cpassword)
         
         # Check if the email is already registered in the database
        data = User_collection.find_one({"Email": email})
        if data:
            return templates.TemplateResponse("signup_page.html", {"request": request, "message": "Email already exists"})              
        
        # Check if the password and confirmation password match
        if password != cpassword:
            return templates.TemplateResponse("signup_page.html", {"request": request, "message": "Passwords do not match"})
                  
        # If the email is not registered and the passwords match, create a new user and insert it into the database
        User_collection.insert_one(user.dict())

        # Redirect to the login page
        return templates.TemplateResponse(Login_template, {"request": request, "user_created": "user"})
    except pymongo.errors.ConnectionFailure :        
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database connection failed")


# Logout
@router.get("/logout", response_class=HTMLResponse)
def logout():   
    try:
        response = RedirectResponse(url="/")
        # logs out the user by deleting the authentication cookie.
        response.delete_cookie(settings.COOKIE_NAME)
        return response   
    except Exception:
            details = f"Temporary Redirect"
            raise HTTPException({"details": details}, status_code=307)
    except BaseException :
        # If an exception occurs during the process, a 500 Internal Server Error is returned.        
      raise HTTPException(status_code=500, detail="Internal Server Error")
