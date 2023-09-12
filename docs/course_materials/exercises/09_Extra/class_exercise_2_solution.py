from datetime import datetime

end_of_the_year = datetime(2020, 12, 31)
today = datetime.now()
time_to_the_end_of_the_year = end_of_the_year - today
print("There are {} days left…".format(time_to_the_end_of_the_year.days))
