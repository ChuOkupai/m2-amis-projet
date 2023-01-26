INIT		:= .init
SRCS_DIR	:= srcs
SRCS_PYTHON	:= $(SRCS_DIR)/python

$(INIT):
	cd $(SRCS_DIR)/c/nauty && ./configure && make
	touch $(INIT)

run: $(INIT)
	python3 $(SRCS_DIR)/run_cli.py

clean:
	rm -rf $(SRCS_DIR)/__pycache__ $(SRCS_PYTHON)/__pycache__ $(SRCS_PYTHON)/*/__pycache__ $(INIT)

test:
	python3 -m unittest discover -s $(SRCS_DIR)

.PHONY: clean run test
