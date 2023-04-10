from dotenv import load_dotenv
from fastapi.responses import HTMLResponse
from fastapi import Request, HTTPException, Depends, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config.config import settings
from schema.schema import User
from auth.oauth2 import get_current_user_from_token

router = APIRouter()

router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


# variable for mongodb collection
client = settings.client

Data_Stream =settings.streaming_collection


@router.get("/datastream", response_class=HTMLResponse)
def streaming_page(request: Request, user: User = Depends(get_current_user_from_token)):       
    try:
        streaming_values = []
        all_shipments = Data_Stream.find({})
        for i in all_shipments:
            streaming_values.append(i)
        context = {"user": user,"streaming_values":streaming_values,"request": request}
        return templates.TemplateResponse("datastream.html", context)
    except Exception as e:        
        return HTTPException(status_code=503, detail="Server Temporarily unavailable")
