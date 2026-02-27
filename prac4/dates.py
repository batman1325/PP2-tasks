import datetime

x = datetime.datetime.now()
print(x)

#______________

import datetime

x = datetime.datetime.now()

print(x.year)
print(x.strftime("%A"))

#______________

import datetime

x = datetime.datetime(2020, 5, 17)

print(x)

#______________

import datetime

x = datetime.datetime(2018, 6, 1)

print(x.strftime("%B"))
