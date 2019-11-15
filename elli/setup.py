from setuptools import setup

setup(
    name='Elli',
    version='1.0',
    long_description=__doc__,
    packages=[''],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "gpiozero==1.5.1"
    ]
)
