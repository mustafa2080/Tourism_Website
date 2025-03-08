# ...existing code...

INSTALLED_APPS = [
    # ...existing code...
    'apps.destinations',
    # ...existing code...
]

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

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# WhiteNoise Configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Image Optimization Settings
IMAGEKIT_CACHE_BACKEND = 'default'
IMAGEKIT_CACHE_TTL = 2592000  # 30 days cache

# Cache Settings
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,  # 5 minutes
    }
}

# Compression settings
COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.rCSSMinFilter',
]
COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']
COMPRESS_OFFLINE = True

# Make sure MIDDLEWARE includes CSRF
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this after security middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # Make sure this is present
    'django.middleware.gzip.GZipMiddleware',  # Add this for compression
    'django.middleware.cache.UpdateCacheMiddleware',  # Add this
    'django.middleware.cache.FetchFromCacheMiddleware',  # Add this
    # ...rest of your middleware...
]

# For production
DEBUG = False
ALLOWED_HOSTS = ['*']  # Update with your Railway domain

# WhiteNoise Settings
WHITENOISE_MAX_AGE = 31536000  # 1 year