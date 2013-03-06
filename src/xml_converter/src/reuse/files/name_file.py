from datetime import date, datetime
import os


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

def add_date_to_filename(filename, prefix = True):
    path = os.path.dirname(filename)
    name = os.path.basename(filename)
    now = datetime.now().isoformat().replace(':', '')
    
    if prefix:
        new_name = now + '.' + name
    else:
        dot_position = name.rfind('.')
        ext = name[dot_position:]
        new_name = name[0:dot_position] + '.' + now + ext
    return new_name
