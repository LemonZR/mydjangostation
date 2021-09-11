from django.test import TestCase

# Create your tests here.


import re
price = re.sub(r'\[|\]','', input("价格列表")).split(',')
print(price)