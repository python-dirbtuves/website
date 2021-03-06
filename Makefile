all: bin/django

help:
	@echo 'make ubuntu     install the necessary system packages (requires sudo)'
	@echo 'make            set up the development environment'
	@echo 'make run        start the web server'
	@echo 'make test       run project test suite'
	@echo 'make testall    run all tests, pyflakes, pylint and coverage'
	@echo 'make tags       build ctags file'
	@echo 'make lint       check coding style'

ubuntu:
	sudo apt-get update
	sudo apt-get -y build-dep python-psycopg2
	sudo apt-get -y install build-essential python-dev exuberant-ctags

run: bin/django ; bin/django runserver

test: bin/django ; bin/django test --settings=pylab.settings.testing --nologcapture

testall: bin/django ; scripts/runtests.py pylab

tags: bin/django ; bin/ctags -v --tag-relative

clean: ; rm -rf bin .coverage develop-eggs include .installed.cfg lib pylab_lt.egg-info parts

lint: bin/django
	bin/flake8 --exclude=migrations --ignore=E501,E241 pylab
	bin/django htmllint
	bin/pylint --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" pylab

buildout.cfg: ; ./scripts/genconfig.py config/env/development.cfg

bin/pip: ; virtualenv --no-site-packages --python=python3 .

bin/buildout: bin/pip ; $< install zc.buildout==2.3.1

mkdirs: var/www/static var/www/media

var/www/static var/www/media: ; mkdir -p $@

bin/django: bin/buildout buildout.cfg $(wildcard config/*.cfg) $(wildcard config/env/*.cfg) mkdirs ; $<
	bin/django compilemessages

.PHONY: all help run mkdirs test testall tags clean
