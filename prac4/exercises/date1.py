from datetime import datetime, timedelta

today = datetime.now()
days = today - timedelta(days=5)

print(days)