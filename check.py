import secrets

secret_key = secrets.token_urlsafe(32)
print(secret_key)  # Copy this key and use it in your FastAPI settings
