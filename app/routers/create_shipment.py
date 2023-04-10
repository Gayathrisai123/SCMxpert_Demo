from dotenv import load_dotenv
from pymongo.errors import PyMongoError
from fastapi.responses import HTMLResponse
from fastapi import Form, Request, HTTPException, Depends, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config.config import settings

from schema.schema import Shipment, User
from routers.auth import get_current_user_from_cookie
from auth.oauth2 import get_current_user_from_token

router = APIRouter()

router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@router.get("/shipment", response_class=HTMLResponse)
def shipment_view(request: Request, user: User = Depends(get_current_user_from_token)):
    try:
        context = {"user": user, "request": request}
        return templates.TemplateResponse("createshipment.html", context)
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception))


# variable for mongodb collection
client = settings.client
Shipment_collection = settings.shipment_collection


@router.post("/shipment", response_class=HTMLResponse)
def createshipment(request: Request, Shipment_invoicenumber: str = Form(...), Container_number: str = Form(...),
                   Shipment_description: str = Form(...), route: str = Form(...), goods: str = Form(...),device: str = Form(...),
                   expected_delivery_date: str = Form(...), po_number: str = Form(...), delivery_number: str = Form(...),
                   ndc_number: str = Form(...), Batch_id: str = Form(...), serial_number_of_goods: str = Form(...), ):
    username = get_current_user_from_cookie(request)
    user = Shipment(Shipment_invoicenumber=Shipment_invoicenumber, Container_number=Container_number, Shipment_description=Shipment_description,
                    route=route, goods=goods, device=device,  expected_delivery_date=expected_delivery_date, po_number=po_number, delivery_number=delivery_number,
                    ndc_number=ndc_number, Batch_id=Batch_id, serial_number_of_goods=serial_number_of_goods)

    details = Shipment_collection.find_one(
        {"Shipment_invoicenumber": Shipment_invoicenumber})

    try:
        if not details:
            Shipment_collection.insert_one(user.dict())
            return templates.TemplateResponse("createshipment.html", {"request": request, "user": username, "success_message": "Success!  shipment has been created"})
        return templates.TemplateResponse("createshipment.html", {"request": request, "user": username, "message": "*Shipment_Invoice_Number already exists"},
                                          status_code="409")
    except Exception:
        details = f" Unprocessable Entity"
        raise HTTPException(
            {"request": request, "details": details}, status_code=422)
    except BaseException as exception:
        error_message = f"Internal Server Error: {str(exception)}"
        raise HTTPException(
            {"request": request, "error_message": error_message}, status_code=500)
