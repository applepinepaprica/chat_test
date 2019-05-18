_A simple chat app_

###Technology stack:
* Python 3.6
* Django
* Graphene
* Relay
* Graphql_jwt

###Running project for the first time:

```
python3.6 -m venv venv
source venv/bin/activate
pip install django==2.1.4 graphene-django==2.2.0 django-filter==2.0.0 django-graphql-jwt==0.1.5
cd limbo
python manage.py migrate
python manage.py runserver
```
http://localhost:8000/graphql

###Running project:

```
source venv/bin/activate
cd limbo
python manage.py runserver
```

###Creating an admin user:

```
python manage.py createsuperuser
```

###Queries:

* Getting info about the current user:
```
{
  me {
    id
    username
    email
  }
}
```

* Getting a chat with a particular user:
```
{
  messages(receiverId: "VXNlck5vZGU6Mw==") {
    edges {
      node {
        id
        text
        receiver {
          username
        }
        sender {
          username
        }
        datetime
      }
    }
  }
}
```

* Getting a list of users:
```
{
  users {
    edges {
      node {
        id
        username
        email
      }
    }
  }
}
```

###Mutations:

* Creating an user:
```
mutation {
  createUser(input: {username: "user", password: "password", email: "email@gmail.com"}) {
    user {
      id
      username
      email
    }
  }
}
```

* Saving a message:
```
mutation {
  saveMessage(input: {receiverId: "VXNlck5vZGU6Mg==", text: "text"}) {
    message {
      id
      text
      sender {
        username
      }
      receiver {
        username
      }
      datetime
    }
  }
}
```
###Authentication:

* Getting a token:
```
mutation {
  tokenAuth(username: "user", password: "password") {
    token
  }
}
```

* For auth use the token in Authorization HTTP header:
```
Authorization: JWT eyJ0eXAiOiJKV1QiLCJhbGciO
```
