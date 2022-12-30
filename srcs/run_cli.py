from python.cli import Application
import sys

if __name__ == "__main__":
	app = Application(sys.argv)
	exit_code = app.run()
	sys.exit(exit_code)
