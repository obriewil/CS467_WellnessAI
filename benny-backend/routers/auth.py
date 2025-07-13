from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
import jwt  # pip install pyjwt

config = Config('.env')
oauth = OAuth(config)

# Google
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'}
)

# Apple
oauth.register(
    name='apple',
    server_metadata_url='https://appleid.apple.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email name'}
)

# Facebook (OAuth2 manual config)
oauth.register(
    name='facebook',
    authorize_url='https://www.facebook.com/v20.0/dialog/oauth',
    access_token_url='https://graph.facebook.com/v20.0/oauth/access_token',
    userinfo_endpoint='https://graph.facebook.com/me?fields=id,name,email',
    client_kwargs={'scope': 'email'}
)

router = APIRouter(prefix='/api/v1/auth')

SECRET_KEY = config('SECRET_KEY')  # For JWT signing

def generate_jwt(user_info):
    return jwt.encode(user_info, SECRET_KEY, algorithm='HS256')

@router.get('/{provider}/login')
async def login(provider: str, request: Request):
    client = oauth.create_client(provider)
    redirect_uri = request.url_for('auth_callback', provider=provider)
    return await client.authorize_redirect(request, redirect_uri)

@router.get('/{provider}/callback', name='auth_callback')
async def callback(provider: str, request: Request):
    client = oauth.create_client(provider)
    token = await client.authorize_access_token(request)
    if provider in ['google', 'apple']:
        user = token.get('userinfo')
    else:  # Facebook
        user = await client.get('https://graph.facebook.com/me?fields=id,name,email', token=token).json()
    if not user:
        return HTMLResponse('Authentication failed')
    # Assume user creation/update in DB here, get user_id or info
    jwt_token = generate_jwt({'sub': user['id'], 'name': user.get('name'), 'email': user.get('email')})
    html = f"""
    <script>
        window.opener.postMessage({{ token: '{jwt_token}' }}, '*');
        window.close();
    </script>
    """
    return HTMLResponse(html)