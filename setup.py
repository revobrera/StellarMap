from setuptools import setup

setup(

    name='StellarMap',
    version = '0.1',
    description='This package was created by Rev Obrera',
    long_description='This app was created by Rev Obrera. Modifications and packaging was done by RexMello',
    author='Rev Obrera',
    packages=['StellarMap'],
    install_requires = ['pandas==1.4.2','Pillow==9.1.1','PyQt5==5.15.4','requests==2.27.1'],
    keywords=['Python','StellarMap']

)