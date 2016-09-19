#testjob2backend

This is test job for demostration my web development stack for create SPA app. In brief, this app is multitasking parser for
selected www sites, full functions description you may see at [Test job descriptionn (rus )](https://github.com/poiskpoisk/testjob2backend/blob/master/%D0%A2%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D0%BE%D0%B5%20%D0%B7%D0%B0%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5%20%D1%81%D0%B5%D1%80%D0%B2%D0%B5%D1%80%D0%BD%D0%BE%D0%B5%20%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5%20.pdf) 

+ _Frontend:_     Algular 2.0, Bootstrap. 
+ _Backend:_      Django, Djangorestframework, Django-cors-middleware
+ _Multitasking:_ concurrent.futures
+ _Parsing:_      lxml
+ _Other:_        docker, git

Screencast with function demonstration and my description

#__Usage:__
+ sudo docker pull abakumov/testjob2backend
+ sudo docker pull abakumov/testjob2frontend
+ sudo docker docker run -i -t -p 8000:8000 abakumov/testjob2backend
+ sudo docker docker run -i -t -p 8000:8000 abakumov/testjob2frontend
+ admin panel backend see at browser http://127.0.0.4:8000/admin/  _Login/pwd:_ ama/alex1972
+ app see at browser http://localhost:3000/





