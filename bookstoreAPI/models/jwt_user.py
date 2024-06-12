from bookstoreAPI.models.user import User

class JWTUser(User):
    disabled: bool
    role: str