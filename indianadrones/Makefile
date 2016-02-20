VENV=venv
PYTHON=venv/bin/python3
PIP=venv/bin/pip

$(VENV):
	virtualenv -p $(shell which python3) $(VENV)

install: $(VENV)
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) app.py

shell:
	$(PYTHON)
