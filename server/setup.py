from setuptools import setup

setup(
    name='Elli Server',
    version='1.0',
    long_description=__doc__,
    packages=[''],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask-cors==3.0.9',
        'flask',
    ]
)
