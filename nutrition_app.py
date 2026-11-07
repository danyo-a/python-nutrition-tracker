import json


class Food:
  def __init__(self, name, calories, proteins, carbs, fat):
    self._name = name
    self._calories = calories
    self._proteins = proteins
    self._carbs = carbs
    self._fat = fat 


  def calculate_value(self, weight):
    value_dict = {}
    for value_name , value in {'calories' : self._calories ,'proteins' :self._proteins,'carbs':self._carbs, 'fat':self._fat}.items():
      value_dict[value_name] =  (weight/100) * value
    return value_dict

  def to_dict(self):
    value_dict = {'name':self._name, 'calories' : self._calories ,'proteins' :self._proteins,'carbs':self._carbs, 'fat':self._fat}

    return value_dict





class Meal:
  def __init__(self):
    self._food_dic = {}
    


  def calculate_meal(self):
    sum_meal = {'calories' : 0 ,'proteins' :0,'carbs':0, 'fat':0}
    for key_name, food_data in self._food_dic.items():

      for value_name, value in food_data[0].calculate_value(food_data[1]).items():
        sum_meal[value_name] += value
    return sum_meal

  def add_food(self, food_name, weight):
    try:
      weight = float(weight)

    except (ValueError, TypeError):
      return False


    if weight <= 0:
      return False

    if isinstance(food_name,Food):
      if food_name._name not in self._food_dic:
        self._food_dic[food_name._name] = [food_name, weight]
        return True
      
      self._food_dic[food_name._name][1] += weight
      return True
    
    return False
  
  def remove_food(self, food_name):
    if isinstance(food_name, Food) and food_name._name in self._food_dic:
        del self._food_dic[food_name._name]
        return True
    return False

  def update_food(self, food_name, weight):
      if isinstance(food_name, Food):
        try:
          weight = float(weight)
        except (ValueError, TypeError):
          return False
    
        if weight <= 0:
          return False
        
        if food_name._name not in self._food_dic:
          return False
        
        self._food_dic[food_name._name][1] = weight
        return True
      
      return False


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
  breakfast.add_food(my_food_database.get_food("banana"), 200)
  breakfast.add_food(my_food_database.get_food("rice"), 200)
  breakfast.add_food(my_food_database.get_food("apple"), 150)


 
  



if __name__=="__main__":
  main()
