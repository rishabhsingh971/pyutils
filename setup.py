import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='PyUtils',
    version='0.0.1',
    author='Rishabh Singh',
    author_email='rishabhsingh971@gmail.com',
    description='Testing installation of Package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/mike-huls/toolbox',
    project_urls = {
        "Bug Tracker": "https://github.com/mike-huls/toolbox/issues"
    },
    license='MIT',
    packages=['toolbox'],
    install_requires=['requests'],
)