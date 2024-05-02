from faker import Faker
from datetime import datetime, timedelta

fake = Faker()



for i in range(20):
    # Generate a datetime 5 years before the current year
    start_date = datetime.now() - timedelta(days=100)  # Subtract 5 years worth of days
    end_date = datetime.now()
    datetime_data = fake.date_time_between(start_date=start_date, end_date=end_date).strftime('%Y-%m-%d %H:%M:%S')

    print(datetime_data)
