from typing import Dict, List, Optional
from fastapi import Request
from fastapi.security import OAuth2, OAuth2PasswordRequestForm
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi import  Form, Request, HTTPException, status, Depends, Response, APIRouter
from fastapi.security.utils import get_authorization_scheme_param
from config.config import settings
from schema.schema import User
import datetime as dt
from jose import JWTError, jwt
from passlib.context import CryptContext


router = APIRouter()

#  for password encrypt and decrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


class LoginForm:
    
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.login_user: Optional[str] = None
        self.login_password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.login_user = form.get("login_user")
        self.login_password = form.get("login_password")

    async def is_valid(self):
       
        if not self.login_user or not (self.login_user.__contains__("@")):
            self.errors.append("Email is required")
        if not self.login_password or len(self.login_password) < 4:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False   

    
class OAuth2PasswordBearerWithCookie(OAuth2):
    
    def __init__(self, tokenUrl: str, scheme_name: Optional[str] = None, scopes: Optional[Dict[str, str]] = None, description: Optional[str] = None, auto_error: bool = True):
       
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        
        authorization: str = request.cookies.get(settings.COOKIE_NAME)
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return None
        return param

oauth2_schema = OAuth2PasswordBearerWithCookie(tokenUrl="token")    

def create_access_token(data: Dict) -> str:
   
    to_encode = data.copy()
    expire = dt.datetime.utcnow() + dt.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


# variable for mongodb collection
client=settings.client
User_collection =settings.user_collection

def get_user(email: str) -> User:    
    user = User_collection.find_one({"Email":email})
    if user:
        return user
    raise HTTPException(status_code=404, detail="user Not Found")


def authenticate_user(username: str, plain_password: str) -> User:    
    user = get_user(username)
    if not user:        
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(plain_password, user['Password']):        
        raise HTTPException(status_code=401, detail="Incorrect password")

    return user

def decode_token(token: str) -> User:    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials."
    )
    token = str(token).replace("Bearer", "").strip()

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc

    user = get_user(username)
    return user

def get_current_user_from_token(token: str = Depends(oauth2_schema)) -> User:
    #   Get the current user from the cookies in a request.
    user = decode_token(token)
    return user
    


def get_current_user_from_cookie(request: Request) -> User:   
    #     Get the current user from the cookies in a request.
    token = request.cookies.get(settings.COOKIE_NAME)
    user = decode_token(token)
    return user



@router.post("token")
def login_for_access_token(response: Response,form_data: OAuth2PasswordRequestForm = Depends()) -> Dict[str, str]:
    # Authenticate the user with the provided credentials
    user = authenticate_user(form_data.login_user, form_data.login_password)
    if not user:
        # If the user is not authenticated, raise an HTTPException with 401 status code
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    # Create an access token for the authenticated user
    access_token = create_access_token(data={"username": user["Email"]})

    # Set an HttpOnly cookie in the response. `httponly=True` prevents
    response.set_cookie(key=settings.COOKIE_NAME,value=f"Bearer {access_token}",  httponly=True)
    # Return the access token and token type in a dictionary
    return {settings.COOKIE_NAME: access_token, "token_type": "bearer"}
 