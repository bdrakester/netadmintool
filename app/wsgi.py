# WSGI Entry Point for the NetAdminTool Web Application
from app import app as application

if __name__ == "__main__":
	application.run()
