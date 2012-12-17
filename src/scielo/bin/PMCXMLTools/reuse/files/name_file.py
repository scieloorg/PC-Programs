from datetime import date, datetime


def return_path_based_on_date():
    today = date.today().isoformat()
    return today[0:4] + '/' + today[5:7] + '/' + today[8:9]
    
def path_range_of_10days():
    today = date.today().isoformat()
    return today[0:4] + '/' + today[5:7] + '/' + today[8:9]
    
def filename_now():
    return datetime.now().isoformat().replace(':','')
    
def filename_today():
	return date.today().isoformat()