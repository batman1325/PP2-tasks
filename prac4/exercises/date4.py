from datetime import datetime

date1 = datetime(2026, 2, 20, 10, 0, 0)
date2 = datetime(2026, 2, 24, 12, 30, 0)

diff = date2 - date1
seconds = diff.total_seconds()

print(seconds)