SRCS_DIR	:= srcs
SRCS_PYTHON	:= $(SRCS_DIR)/python

clean:
	rm -rf $(SRCS_DIR)/__pycache__ $(SRCS_PYTHON)/__pycache__ $(SRCS_PYTHON)/*/__pycache__

run:
	python3 $(SRCS_DIR)/run_cli.py

test:
	python3 -m unittest discover -s $(SRCS_DIR)

.PHONY: clean run test
