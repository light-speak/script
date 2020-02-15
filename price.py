
class Food:
    food_name = ''
    food_price = 0

    def __init__(self, name, price):
        self.food_name = name
        self.food_price = price


selectList = []

foods = [
    Food("A", 10),
    Food("B", 5),
    Food("C", 10),
    Food("D", 22),
    Food("F", 15),
]


def searchFoods(index, prefix=[]):
    global selectList
    count = 0
    for item in prefix:
        count += item.food_price
    prefix.append(foods[index])
    for i in range(index + 1, len(foods) - 1):
        searchFoods(i, prefix)
    if len(prefix) > 0 and 20 <=  count + foods[index].food_price <= 30:
        selectList.append(prefix)

for i in range(len(foods)):
    searchFoods(i)

for item in selectList:
    print(item)
