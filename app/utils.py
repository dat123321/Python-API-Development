from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
pwd_context.default_scheme()


def Hash(pwd: str):
    return pwd_context.hash(pwd)


def verify(plain_password, hashed_pass):
    return pwd_context.verify(plain_password, hashed_pass)