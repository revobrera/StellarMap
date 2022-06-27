from setuptools import setup

setup(

    name='StellarMap',
    version = '0.3.0',
    description='StellarMap is an open source, cross-platform PyQt desktop app used to explore the Stellar blockchain network.',
    long_description='StellarMap is an open source desktop app written in Python, used to explore the Stellar blockchain network. The desktop app is available on Windows, GNU/Linux, Mac OS X, Android, & iOS. ',
    author='Rev Obrera',
    packages=['StellarMap'],
    install_requires = ['numpy==1.21.6', 'pandas==1.4.2','Pillow==9.1.1','PyQt5==5.15.4', 'PyQt6==6.3.0', 'PyQt6-Qt6==6.3.0', 'PyQt6-sip==13.3.1','Qt.py==1.3.7','requests==2.27.1','tabulate==0.8.10'],
    keywords=['Python','StellarMap', 'PyQt5', 'PyQt6', 'Desktop', 'Desktop app']

)