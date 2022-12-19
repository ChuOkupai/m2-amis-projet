SRCS_PYTHON	:= srcs/python

clean:
	rm -rf $(SRCS_PYTHON)/*/__pycache__

run:
	python3 $(SRCS_PYTHON)/cli

test:
	python3 -m unittest discover -s $(SRCS_PYTHON)

.PHONY: clean run test
