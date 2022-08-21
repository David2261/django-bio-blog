.PHONY start env activate install dir migrate

PIP = pip install
PYTHON = python manage.py
ENV = virtualenv
REQ = requirements.txt
MIGRATE = migrate
ACTIVATE = venv\Scripts\activate

all: start

start: $(PIP)
	$(PIP) $(ENV)
	$(MAKE) env

env: $(ENV)
	$(ENV) venv
	$(MAKE) activate

activate: $(ACTIVATE)
	$(ACTIVATE)
	$(MAKE) install

install: $(REQ)
	$(PIP) $(REQ)
	$(MAKE) dir

dir: $(REQ)
	cd bioblog/

migrate: $(PYTHON)
	$(PYTHON) $(MIGRATE)