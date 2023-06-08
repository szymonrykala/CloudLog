BINARIES := jq python3
DIST_DIR := $(dist-folder)
DEFAULT_DIR := "$(HOME)/cloudlog"

ifeq ($(DIST_DIR),)
	DIST_DIR := $(DEFAULT_DIR)
endif


hello:
	@echo "make build\nmake install"


build: system_dependencies build_package end
install: __create_runner_package __prepare_systemd_file __register_service


system_dependencies:
	@echo "Instaling system dependencies\n"
	# sudo apt update;

	@for item in $(BINARIES); do \
		if ! command -v $$item >/dev/null; then \
			echo "Installing $$item ..."; \
			sudo apt install -y $$item; \
		fi; \
	done

	@if ! command -v poetry; then\
		echo "Installing poetry ...";\
		curl -sSL https://install.python-poetry.org | python3;\
	fi


__tests:
	poetry install;
	
	@echo "Running tests";
	poetry run python -m pytest;


build_package: __tests
	@if [ -e ./dist ]; then\
		rm -r ./dist;\
	fi;\

	poetry build --format wheel --directory .;

	@echo "\nDistribution dir set to $(DIST_DIR)";
	
	@if [ ! -e $(DIST_DIR) ]; then \
		mkdir $(DIST_DIR); \
		mkdir $(DIST_DIR)/logs;\
	fi;\

	sudo find /home/szymon/cloudlog/ -name "*.whl" -type f -delete; 
	
	@cp -r ./dist/. $(DIST_DIR);


__create_runner_package:
	@if [ $$DEFAULT_DIR == $$DIST_DIR ]; then\
		cd $(DIST_DIR);\
		rm -r ./runner;\
		mkdir runner;\
		cd runner;\
		poetry new .;\
		poetry add ../*.whl;\
	else \
		echo "Installing aborted.\ndist-folder needs to be default.";\
	fi; \


__prepare_systemd_file:
	@if [ $$DEFAULT_DIR == $$DIST_DIR ]; then\
		cat ./cloudlog.txt | sed "s/__USER__/$$USER/g" > ./cloudlog.service;\
	else \
		echo "Creating of systemd file aborted. Build path needs to be default.";\
	fi; \


__register_service:
	@sudo cp ./cloudlog.service /etc/systemd/system/;
	@sudo systemctl daemon-reload ;
	@sudo systemctl enable cloudlog;
	@sudo systemctl restart cloudlog;
	@sudo systemctl status cloudlog | cat;


end:
	@echo "Build successful!!\n\
	The package is here '$(DIST_DIR)'\n\
	> 'make install' to install it as a service cloudlog"