from faker import Faker

from faker import Faker

# Create a Faker instance
fake = Faker()



for i in range(20):

        # Generate a fake date in the format 'YYYY-MM-DD'
    fake_date = fake.date_between(start_date='-10y', end_date='-5y')  # Generate a date within the last 5 years until today
    fake_date_str = fake_date.strftime('%Y-%m-%d')  # Convert the date object to a string in the desired format

    print(fake_date_str)
