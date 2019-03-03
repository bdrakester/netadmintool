# WSGI Entry Point for the NetAdminTool API
from api import app as application

if __name__ == "__main__":
	application.run()
