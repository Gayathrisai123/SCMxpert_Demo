from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from routers import auth, kafka_data_streaming,create_shipment


# Create a FastAPI app instance
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(auth.router, prefix='')
app.include_router(create_shipment.router,prefix='')
app.include_router(kafka_data_streaming.router,prefix='')


@app.exception_handler(HTTPException)
async def handle_http_exception(request: Request, exc: HTTPException) -> RedirectResponse:
    try:
        if exc.status_code == 401:
            return RedirectResponse(url="/login")            
    except Exception as exception:
        # If an exception occurs during the process, a 500 Internal Server Error is returned.
        raise HTTPException(status_code=403, detail="Data Not Found") from exception