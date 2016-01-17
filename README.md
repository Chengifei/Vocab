# Welcome
This temporarily untitled project is aimed to help memorizing vocabularies.
# System Requirements
Python3 installation in a linux distro is required to run the program. It is originally written in python3.4.
# How it works
The get.py is a gadget grabbing words info from web (refer to [Web scraping](https://en.wikipedia.org/wiki/Web_scraping)). More specifically, the meanings are from youdao (an online dictionary provider in China) and phonetics are from OxfordDictionaries.
The main.py is a question generater basically, some extra code is included but not used, which is reserved for future developing.
# Using the program
The program itself does not bring any vocabulary data. This should be provided with a dictionary in json format.
Open the linux terminal, switch to your working dir and then simply run:

	$ python main.py

It should work fine.
# Bugs
This is a python3 program only tested on FEDORA-22 with python3.4x86-64 and has some known conflicts with windows.
# Postscirpt
This is not the initial version of the program, as I remembered, there have to be at least three release-ready version and nearly thousand time of running and debugging. The drafting and quick-profit version is written only with functions, i.e. not object oriented. Later, realized the importance of debugging and the neatness of the code, I involved classes, only a few days ago. Now it seems to work well.
