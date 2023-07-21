from attrs import define
from pydantic import BaseModel


class Purchase(BaseModel):
    user_id: int = 0
    flower_id: int = 0


class PurchasesRepository:
    purchases: list[Purchase]

    def __init__(self):
        self.purchases = []

    def save(self, purchase: Purchase):
        self.purchases.append(purchase)

    def get_all(self):
        return self.purchases

    def get_by_user_id(self, user_id: int) -> list:
        flowers = [i.flower_id for i in self.purchases if i.user_id == user_id]
        return flowers
