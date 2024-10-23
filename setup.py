from setuptools import setup

setup(
    name='morg',
    version='0.1.0',
    packages=['api', 'files', 'models', 'service'],
    url='https://github.com/fscotto/music-organizer',
    license='GPL-3.0',
    author='Fabio Scotto di Santolo',
    author_email='fabio.scottodisantolo@gmail.com',
    description='Project for recognize automatically and organize music folders',
    install_requires=['pyinstaller', 'shazamio', 'python-magic']
)
