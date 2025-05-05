from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime


def set_jwt_cookies(response, access_token, refresh_token=None):
    """
    Устанавливает JWT токены в cookies ответа.
    """
    access_expiration = datetime.fromtimestamp(access_token.payload['exp'])
    
    # Устанавливаем access token в куки
    response.set_cookie(
        settings.SIMPLE_JWT['AUTH_COOKIE'],
        access_token,
        expires=access_expiration,
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
    )
    
    # Если предоставлен refresh token, устанавливаем его в куки
    if refresh_token:
        refresh_expiration = datetime.fromtimestamp(refresh_token.payload['exp'])
        response.set_cookie(
            settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'],
            refresh_token,
            expires=refresh_expiration,
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
            path=settings.SIMPLE_JWT['AUTH_COOKIE_PATH'],
        )
    
    return response


def get_tokens_from_cookies(request):
    """
    Извлекает JWT токены из cookies запроса.
    """
    access_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
    refresh_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
    
    return access_token, refresh_token

class CookieJWTAuthentication(JWTAuthentication):
    """
    Пользовательский класс аутентификации JWT, который поддерживает cookies.
    """
    def authenticate(self, request):
        # Сначала пробуем получить токен из Authorization заголовка
        header_auth = super().authenticate(request)
        if header_auth is not None:
            return header_auth
        
        # Если нет в заголовке, пробуем из cookies
        access_token, _ = get_tokens_from_cookies(request)
        if not access_token:
            return None
        
        # Добавляем заголовок Authorization с токеном из куки
        validated_token = self.get_validated_token(access_token)
        return self.get_user(validated_token), validated_token 