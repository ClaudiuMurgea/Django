# pyramid/constants.py

## The password measure can be "minutes", "hours" or "days"
PASSWORD_MEASURE = "days"
PASSWORD_EXPIRATION_TIME = 90

PIN_MEASURE = "minutes"
PIN_EXPIRATION_TIME = 3

USER_MAXIMUM_FAILED_ATTEMPTS = 25

TOKEN_MEASURE = "hours"
TOKEN_EXPIRATION_TIME = 1000