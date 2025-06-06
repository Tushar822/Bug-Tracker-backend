from fastapi import Depends, HTTPException, status,Request, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from jose import JWTError, jwt
from app.db.database import get_session
from app.models.user import User, UserRole, TokenData
from app.core.config import settings
from typing import Optional

security = HTTPBearer()

# def get_current_user(
#     credentials: HTTPAuthorizationCredentials = Depends(security),
#     session: Session = Depends(get_session)
# ):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
    
#     try:
#         payload = jwt.decode(credentials.credentials, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
#         email: str = payload.get("sub")
#         if email is None:
#             raise credentials_exception
#         token_data = TokenData(email=email)
#     except JWTError:
#         raise credentials_exception
    
#     statement = select(User).where(User.email == token_data.email)
#     user = session.exec(statement).first()
#     if user is None:
#         raise credentials_exception
#     return user

async def get_current_user(
    request: Request,
    session: Session = Depends(get_session),
    access_token: Optional[str] = Cookie(None, alias="access_token")
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not access_token:
        raise credentials_exception
        
    try:
        # Remove "Bearer " prefix if present
        token = access_token #.replace("Bearer ", "")
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    statement = select(User).where(User.email == token_data.email)
    user = session.exec(statement).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_pm(current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.PM:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Project Managers can perform this action"
        )
    return current_user

