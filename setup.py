from setuptools import setup, find_packages

setup(
    name='jobtech-anonymisering',
    version='1.0.2',
    packages=find_packages(),
    package_data = {
        'jobtech-anonymisering': ['resources/names/*']
    },
    include_package_data=True,
    install_requires=[
        'nltk'
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"]
)
