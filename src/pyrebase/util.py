def is_valid_str(string):
  return isinstance(string, str) and len(string) > 0

def is_valid_number(number):
  return isinstance(number, int) or isinstance(number, float)

def is_valid_attr(attribute):
  return is_valid_str(attribute) or is_valid_number(attribute)