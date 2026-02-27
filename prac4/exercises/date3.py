from datetime import datetime

now = datetime.now()
micro = now.replace(microsecond=0)

print(micro)