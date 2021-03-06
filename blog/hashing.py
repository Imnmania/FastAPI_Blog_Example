from passlib.context import CryptContext


#========================= HASHING PASSWORD ========================#
pwd_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')


#========================= CUSTOM CLASS FOR HASHING ==================#
class Hash():
    def bcrypt(password: str):
        return pwd_ctx.hash(password)