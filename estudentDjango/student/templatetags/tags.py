from django import template

register = template.Library()
def date_extend(value):
    return str(value)+"/"+str(value+1)[2:]

def nacin_studija(value):
    if not value:
        return "Izredni"
    
    return ""

def enrol(value):
	return "" if value == "V1" else value

register.filter('nacin_studija', nacin_studija)
register.filter('date_extend', date_extend)
register.filter('enrol', enrol)