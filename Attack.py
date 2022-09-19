from Evasion import Evasion

class Attack:
  def __init__(self, name, num_charges_needed, evasion_method):
    self.name = name
    self.num_charges_needed = num_charges_needed
    self.power = num_charges_needed*10
    self.evasion_method = evasion_method
  
  def __str__(self):
    return str((self.name, self.power, self.evasion_method, self.num_charges_needed))
  
attacks = [Attack("Kamehameha", 1, Evasion.DODGE),\
         Attack("Sayonara", 2, Evasion.BLOCK),\
         Attack("Spin Kamehameha", 3, Evasion.BLOCK)]
