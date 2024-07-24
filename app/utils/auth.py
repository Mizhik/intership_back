from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from jose import jwt, JWTError 
from jwt import PyJWKClient
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from app.core.settings import config

security = HTTPBearer()


class Auth:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

    @staticmethod
    async def create_access_token(data: dict, expires_delta: Optional[float] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.now() + timedelta(minutes=15)
        to_encode.update(
            {"iat": datetime.now(), "exp": expire, "scope": "access_token"}
        )
        encoded_access_token = jwt.encode(
            to_encode, config.AUTH_SECRET_KEY, algorithm=config.AUTH_ALGORITHM
        )
        return encoded_access_token

    @staticmethod
    async def get_current_user_with_token(token: str) -> Optional[tuple[str, str]]:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(
                token,
                config.AUTH_SECRET_KEY,
                algorithms=[config.AUTH_ALGORITHM],
            )
            email: str = payload.get("sub")
            if email is None:
                raise credentials_exception
            return email, "own_service"
        except JWTError:
            try:
                jwks_client = PyJWKClient(config.AUTH0_JWKS_URL)
                signing_key = jwks_client.get_signing_key_from_jwt(token)

                payload = jwt.decode(
                    token,
                    signing_key.key,
                    algorithms=[config.ALGORITHM],
                    issuer=config.ISSUER,
                    audience=config.API_AUDIENCE,
                )
                email: str = payload.get("email")
                if email is None:
                    raise credentials_exception
                return email, "auth0"
            except JWTError as e:
                raise credentials_exception from e
