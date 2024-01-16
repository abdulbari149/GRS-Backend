run:
	export FLASK_APP=app.py
	flask run --debug

init-db:
	export FLASK_APP=app.py
	flask init-db