import constants

def get_page_title(self, page):
	return constants.APPNAME + " - " + page

def is_page_active(self, page, currentpage):
	if (page == currentpage):
		return "class='active'"
	return ""

def get_app_name(self):
	return constants.APPNAME