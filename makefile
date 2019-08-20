install: # system-wide standard python installation
	pip install .

install.hack: # install development requirements
	pip install -r requirements.txt
	pip install -e .[test]

build: # build package for distribuition
	rm -rf dist
	python setup.py sdist
	python setup.py bdist_wheel

publish: # publish package to the pypi
	twine upload dist/*

lint: # lint code
	flake8 .

clean: # remove temporary files and artifacts
	rm -rf site/
	rm -rf *.egg-info dist build
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '.coverage' -exec rm -f {} +
	find . -name '__pycache__' -exec rmdir {} +
