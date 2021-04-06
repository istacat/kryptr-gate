from app.models import User

ALL_USERS = [
    (user.id, user)
    for user in User.query.filter(User.deleted == False).filter(User.is_active == True)
]