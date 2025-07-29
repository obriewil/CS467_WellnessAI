from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from routers.auth import SECRET_KEY

router = APIRouter(prefix='/api/v1/users')
security = HTTPBearer()

def decode_jwt(token: str):
    """
    Decodes the JWT token to get user information
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

@router.get("/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Grabs current user's data from their token
    """
    token = credentials.credentials
    user_data = decode_jwt(token)
    return {"user": user_data}