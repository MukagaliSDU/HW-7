from attrs import define
from pydantic import BaseModel


class Flower(BaseModel):
    name: str
    count: int
    cost: int
    id: int = 0


class FlowersRepository:
    flowers: list[Flower]

    def __init__(self):
        self.flowers = [
            Flower(id=1, name="Roza", count=20, cost=2000),
            Flower(id=2, name="Tyolpan", count=10, cost=1000),
            Flower(id=3, name="Mukash", count=30, cost=2000),

        ]

    def save(self, flower: Flower) -> Flower:
        flower.id = len(self.flowers)+1
        self.flowers.append(flower)
        return flower

    def get_all(self):
        return self.flowers

    def get_list(self, flowers_id: list )-> list:
        res = []
        if flowers_id is None:
            return res
        for index, flower in enumerate(self.flowers):
            if str(flower.id) in flowers_id:
                res.append(flower)
        return res







