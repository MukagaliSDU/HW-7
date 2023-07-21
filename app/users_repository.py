from attrs import define


@define
class User:
    email: str
    full_name: str
    password: str
    id: int = 0


class UsersRepository:
    users: list[User]

    def __init__(self):
        self.users = [
            User(id=1, email="user1", full_name="new jontan", password="123"),
            User(id=2, email="user2", full_name="new Nelson Mandela", password="123"),
        ]
        self.carts = []

    def save(self, user: User):
        user.id = len(self.users) + 1
        self.users.append(user)

    def get_by_email(self, email: str) -> User:
        for user in self.users:
            if user.email == email:
                return user
        return None

    def get_by_id(self, id: int) -> User:
        for user in self.users:
            if user.id == id:
                return user
        return None

