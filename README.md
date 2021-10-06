# Quiz + audio

I have built this web app to let schools access a customizable quiz maker and even put it online

## Setup :

```python
git clone https://github.com/escaper01/quizalcpt.git
```

```bash
cd QuizMaker
```

```bash
virtualenv venv
```

```bash
./venv/Scripts/activate
```

```bash
pip install -r requirements.txt
```

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

```bash
python manage.py createsuperuser
```

```bash
python manage.py runserver
```

In order to make a quiz 

1. create a user that will be a teacher :

```bash
go to http://127.0.0.1:8000/admin
```

![Untitled](README/Untitled%207.png)

![Untitled](README/Untitled%201.png)

![Untitled](README/Untitled%202.png)

Fill in all info and Hit save

![Untitled](README/Untitled%203.png)

Go to teachers model and choose the previous User that you made

2   . Log in as a teacher

![Untitled](README/Untitled%204.png)

Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and click on I'm a teacher and use the credentials that you made for the teacher

3   .Add a quiz

![Untitled](README/Untitled%205.png)

add the title and its audio and save it

![Untitled](README/Untitled%206.png)

First query the order number of the question that you want to add
Then enter all the question component and its options and the correct answer...
At the end hit Save