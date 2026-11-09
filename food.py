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