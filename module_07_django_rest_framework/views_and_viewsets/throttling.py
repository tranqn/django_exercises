from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class BurstAnonThrottle(AnonRateThrottle):
    rate = "30/minute"


class SustainedAnonThrottle(AnonRateThrottle):
    rate = "100/day"


class BurstUserThrottle(UserRateThrottle):
    rate = "60/minute"


class SustainedUserThrottle(UserRateThrottle):
    rate = "1000/day"


# settings.py:
# REST_FRAMEWORK = {
#     'DEFAULT_THROTTLE_CLASSES': [
#         'rest_framework.throttling.AnonRateThrottle',
#         'rest_framework.throttling.UserRateThrottle',
#     ],
#     'DEFAULT_THROTTLE_RATES': {
#         'anon': '100/day',
#         'user': '1000/day',
#     },
# }