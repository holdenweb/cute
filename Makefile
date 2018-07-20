MAIN_DIR := $(dir $(realpath $(firstword $(MAKEFILE_LIST))))
SCRIPTS = $(MAIN_DIR)scripts
CONFIG_DIR = $(MAIN_DIR)/templates

HOST = alice
NET = holdenwebs

all:
	echo scripts live in $(SCRIPTS)

host:
	@python $(SCRIPTS)/parameterize.py --config_dir=templates --net=$(NET) --host=$(HOST)

hosts.py:	templates/hosts.json templates/*/config.json
	python $(SCRIPTS)/buildhosts.py

build-all:
	@make hosts.py && \
	HOSTS=$$(for host in $$(cd $(CONFIG_DIR); ls | grep -v "\.") ; do  echo $$host; done) && \
	for host in $$HOSTS; \
		do \
		echo Configuring host $$host; \
		make HOST=$$host NET=$(NET) host; \
		echo Please plug in host $$host and hit return; \
		read answer; \
	done
