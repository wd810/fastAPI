from passlib.context import CryptContext

# use 'bcrypt' as the hashing algorithm
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

# compare hash
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)