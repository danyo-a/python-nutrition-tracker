from food import Food


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