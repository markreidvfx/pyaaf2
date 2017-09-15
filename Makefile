
test: python-version
	@python -m unittest discover tests

python-version:
	@python --version

clean:
	rm */*.pyc */*/*.pyc
