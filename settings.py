# ...existing code...

CSRF_TRUSTED_ORIGINS = [
    'https://tourismwebsite-production.up.railway.app',
    'http://127.0.0.1:8000',
    'http://localhost:8000'
]

CSRF_COOKIE_SECURE = True  # for HTTPS
CSRF_COOKIE_SAMESITE = 'Lax'