from starlette.config import Config

config = Config('.env')

# Export variables for other files to use
SECRET_KEY = config('SECRET_KEY', cast=str)
GOOGLE_CLIENT_ID = config('GOOGLE_CLIENT_ID', cast=str, default=None)
GOOGLE_CLIENT_SECRET = config('GOOGLE_CLIENT_SECRET', cast=str, default=None)
# Need to add Apple and Facebook Client secrets at some point