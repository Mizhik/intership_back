from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
import requests
from app.core.settings import config

security = HTTPBearer()


class Auth:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[float] = None):
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
    def get_current_user_with_token(token: str) -> Optional[str]:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не удалось проверить учетные данные",
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
            return email
        except JWTError:
            try:
                jwks_url = f"https://{config.DOMAIN}/.well-known/jwks.json"
                jwks_client = requests.get(jwks_url).json()
                unverified_header = jwt.get_unverified_header(token)
                rsa_key = {}
                for key in jwks_client["keys"]:
                    if key["kid"] == unverified_header["kid"]:
                        rsa_key = {
                            "kty": key["kty"],
                            "kid": key["kid"],
                            "use": key["use"],
                            "n": key["n"],
                            "e": key["e"],
                        }
                if rsa_key:
                    payload = jwt.decode(
                        token,
                        rsa_key,
                        algorithms=[config.ALGORITHM],
                        audience=config.API_AUDIENCE,
                        issuer=f"https://{config.DOMAIN}/",
                    )
                    email: str = payload.get("email")
                    if email is None:
                        raise credentials_exception
                    return email
                else:
                    raise credentials_exception
            except Exception:
                raise credentials_exception
