from food import Food
from food_database import FoodDatabase
from meal import Meal
from gui import create_window



def main():
  rice = Food('rice', 130, 2, 25, 0.5)
  apple = Food('apple', 50, 1,10, 0.2)
  my_food_database = FoodDatabase()
  my_food_database.add_food(rice)
  my_food_database.add_food(apple)
  my_food_database.save_food()

  new_database = FoodDatabase()
  new_database.load_food()
  print(new_database.get_food("rice").to_dict())

  
  

  breakfast = Meal()
  breakfast.add_food(my_food_database.get_food("rice"), 200)
  breakfast.add_food(my_food_database.get_food("apple"), 150)
  print(breakfast.calculate_meal())
  create_window(my_food_database)


if __name__=="__main__":
  main()
