
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


def searchFoods(index, count=0, child=True):
    global selectList
    global foods
    if(index >= len(foods)):
        return None
    sum = foods[index].food_price + count
    if sum > 30:
        return None
    else:
        for i in range(len(foods)):
          result = searchFoods(index + 1 + i, sum)
          if result == None:
              if child:
                  return foods[index].food_name
          else:
              if child:
                  return foods[index].food_name + " - " + result
              else:
                  selectList.append(foods[index].food_name + " - " + result)


for i in range(len(foods)):
    searchFoods(i, child=False)

for item in selectList:
    print(item)
