# Selit! Web

[![Build Status](https://travis-ci.org/unizar-30226-2019-07/Break.svg?branch=master)](https://travis-ci.org/unizar-30226-2019-07/Break)
[![codecov](https://codecov.io/gh/unizar-30226-2019-07/Break/branch/master/graph/badge.svg)](https://codecov.io/gh/unizar-30226-2019-07/Break)

Release version: https://selit-web.herokuapp.com/
Beta version: https://selit-web-develop.herokuapp.com/

## Acerca de
Trabajo de la Universidad de Zaragoza.

Asignatura:
	Proyecto Software

Repositorio: 
	Interfaz web (Front-end)
	
Autores:
	Victor Batlle
	Alonso Muñoz
	Pablo Orduna
	
## Instrucciones	
***********************************************
				Instalación
***********************************************
LINUX:

$ sudo apt-get update

$ sudo apt-get install python3-pip python3-dev nginx

$ sudo pip3 install virtualenv

$ apt-get install python3-venv

virtualenv flaskprojectenv

cd $(nombreWeb)

$ python3 -m venv venv

$ virtualenv venv

$ source venv/bin/activate

(vent)$ pip install flask

***********************************************
				 Ejecución
***********************************************
$ source venv/bin/activate
	(linux)
-------------------------
$ venv\Scripts\activate
	(windows)

(venv)$ flask run
