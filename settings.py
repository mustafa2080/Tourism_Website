# ...existing code...

# CSRF Settings
CSRF_TRUSTED_ORIGINS = [
    'https://tourismwebsite-production.up.railway.app',
    'http://127.0.0.1:8000',
    'http://localhost:8000'
]

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = True
CSRF_USE_SESSIONS = True

# Security Settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Make sure MIDDLEWARE includes CSRF
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # Make sure this is present
    # ...rest of your middleware...
]