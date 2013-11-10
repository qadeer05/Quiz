Quiz
====
Quiz is a web based program that helps two users to answer the same set of questions in realtime.

Quiz is built on top of tornado and uses sockjs. 

Requirements
============
To run this software you need python 2.7 installed. 

Quiz depends on the following frameworks and softwares - 
* Tornado
* Sockjs
* MongoDB
* Redis

Before running the server please make sure that you have redis and mongodb installed and are running.

Starting Quiz Server
====================
To run the server follow the steps listed below - 
* Clone the repository 

```
> git clone https://github.com/qadeer05/Quiz.git
```

* Activate virtualenv

```
> venv Quiz
> cd Quiz
> source bin/activate
```

* Install the dependencies

```
> pip install -r requirements.txt
```

* Start the server

```
> python quiz/src/server.py
```


