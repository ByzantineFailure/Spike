from distutils.core import setup
import py2exe

setup(
	name="Spike",
	version="0.1.0",
	author="Michael Eaton",
	author_email="byzanitnefailure@gmail.com",
	description="An assistant for your library (of files)",
	long_description=open("README.md").read(),
	console=["spike.py"],
	zipfile=None,
	options={
		'py2exe':{
			'bundle_files': 0,
			'xref': False,
			'optimize': 2,
			'compressed': 1
		}
	}
)
