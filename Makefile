initial-setup:
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt

update:
	./venv/bin/pip install -r requirements.txt
	