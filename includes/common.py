
import datetime

def format_date(timestamp,format='',timezone=None): 
    #todo: implement type paramter e.g. type='medium'
    if timezone:
        #todo: get the users timezone
        timestamp += timezone
        pass
    
    if not format:
        format = '%a, %m/%d/%Y - %I:%M %p'
    date = datetime.datetime.fromtimestamp(timestamp)
    return date.strftime(format)