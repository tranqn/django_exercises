"""
Django Channels Setup

pip install channels channels-redis

settings.py:
INSTALLED_APPS = [..., 'channels']
ASGI_APPLICATION = 'mysite.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {'hosts': [('127.0.0.1', 6379)]},
    },
}
"""