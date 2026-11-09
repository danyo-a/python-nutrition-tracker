import json
from food import Food
from meal import Meal


class FoodDatabase:
  def __init__(self):
    self._foods = {}

  def add_food(self, food_name):
    if isinstance(food_name, Food) and food_name._name not in self._foods:
        self._foods[food_name._name] = food_name
        return True
    return False

  def get_food(self, food_name):
    if food_name in self._foods:
      return self._foods[food_name]
    return None

  def remove_food(self, food_name):
    if food_name in self._foods:
      del self._foods[food_name]
      return True
    return False

  def update_food(self, food_name):
    if food_name._name in self._foods:
      self._foods[food_name._name] = food_name
      return True
    return False

  def save_food(self):
    file_name = "food_database.json"
    database_dict = {}
    for food_name,food_data in self._foods.items():
      database_dict[food_name] = food_data.to_dict()

    with open(file_name, "w", encoding= "utf-8")as file:
      json.dump(database_dict, file, indent=4)

    return True

  def load_food(self):
    
    with open("food_database.json", "r",  encoding="utf-8")as file:
     loaded_dict = json.load(file)

    for food_name,value in loaded_dict.items():
      new_food = Food(value["name"], value["calories"], value["proteins"], value["carbs"], value["fat"])
      self._foods [food_name] = new_food


    return self._foods