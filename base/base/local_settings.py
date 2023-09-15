from datetime import timedelta

SECRET_KEY = 'django-insecure-4f&wq9wl3k#m=hw7ywasnlq15(p&ut2*^lf&6hn6*4ss7sqq@h'

REST_FRAMEWORK = {
    # "EXCEPTION_HANDLER": "apps.common.exceptions.common_exception_handler",
    "NON_FIELD_ERRORS_KEY": "error",
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #            'common.authbackends.XAuthUser',
    # ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": ("apps.api.renderers.GlobalJSONRenderer",),
    "EXCEPTION_HANDLER": "apps.api.exceptions.common_exception_handler",
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}



DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "bug_tracker",
        "USER": "coofis_user",
        "PASSWORD": "coofis_password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
