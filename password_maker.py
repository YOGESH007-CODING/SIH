import hashlib

from main import ADMIN_PASSWORD_HASH
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

print(hash_password(ADMIN_PASSWORD_HASH));
