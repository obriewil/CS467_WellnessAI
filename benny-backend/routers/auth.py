from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth
from config import SECRET_KEY
import jwt  # pip install pyjwt
from config import SECRET_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET

oauth = OAuth()

# Google
oauth.register(
    name='google',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
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

def generate_jwt(user_info):
    return jwt.encode(user_info, SECRET_KEY, algorithm='HS256')

@router.get('/{provider}/login')
async def login(provider: str, request: Request):
    client = oauth.create_client(provider)
    redirect_uri = request.url_for('auth_callback', provider=provider)
    return await client.authorize_redirect(request, redirect_uri)

@router.get('/{provider}/callback', name='auth_callback')
async def callback(provider: str, request: Request):
    print(f"Generated Redirect URI: {request.url}") 
    client = oauth.create_client(provider)
    token = await client.authorize_access_token(request)

    user_info = {}
    if provider in ['google', 'apple']:
        user_info = token.get('userinfo')
    else:  # Facebook
        user_info = await client.get('https://graph.facebook.com/me?fields=id,name,email', token=token).json()

    if not user_info or 'sub' not in user_info:
        return HTMLResponse('Authentication failed')
    
    jwt_payload = {
        'sub': user_info['sub'], 
        'name': user_info.get('name'), 
        'email': user_info.get('email')
    }
    jwt_token = generate_jwt(jwt_payload)

    html = f"""
    <script>
        window.opener.postMessage({{ token: '{jwt_token}' }}, '*');
        window.close();
    </script>
    """
    return HTMLResponse(html)