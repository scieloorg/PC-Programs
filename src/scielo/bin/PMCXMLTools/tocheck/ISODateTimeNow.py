import datetime


class ISODateTimeNow:
    def __init__(self):
       pass
       
    def get_date(self):
        return datetime.date.today().isoformat().replace('-', '')
    
    def get_time(self):
		now = datetime.datetime.now().timetuple()
		h = '0' + now[4]
		h = h[-2:]
		min = '0' + now[5]
		min = min[-2:]
		seg = '0' + now[6]
		seg = seg[-2:]
		return h + min + seg    
    
    def get_date_time(self):
        return self.get_date() + self.get_time()

    