_A simple chat app_

### Technology stack:
* Python 3.6
* Django
* Graphene
* Relay
* Graphql_jwt

### Running project for the first time:

```
python3.6 -m venv venv
source venv/bin/activate
pip install django==2.1.4 graphene-django==2.2.0 django-filter==2.0.0 django-graphql-jwt==0.1.5
cd chat
python manage.py migrate
python manage.py runserver
```
http://localhost:8000/graphql

### Running project:

```
source venv/bin/activate
cd chat
python manage.py runserver
```

### Creating an admin user:

```
python manage.py createsuperuser
```

### Using:

* Create an user using http://localhost:8000/graphql:
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

* Get a token:
```
mutation {
  tokenAuth(username: "user", password: "password") {
    token
  }
}
```

* Using the token you can create a dialogue:
```
curl \
  -H "Content-Type:application/json" \
  -H "Authorization:JWT $TOKEN" \
  -d '{
      "query": "mutation {createDialogue(input:{receiverId:\"$ID\"}) {dialogue { id }}}"
      ,"variables":null
    }' \
  -X POST 'http://localhost:8000/graphql/'  | python -m json.tool
```

* Save a message:
```
curl \
  -H "Content-Type:application/json" \
  -H "Authorization:JWT $TOKEN" \
  -d '{
      "query": "mutation {saveMessage (input: {dialogueId: \"$ID\", text: \"text\"}) {message {id text sender { username } receiver { username } datetime}}}"
      ,"variables":null
    }' \
  -X POST 'http://localhost:8000/graphql/'  | python -m json.tool
```

* And get a chat with other user:
```
curl \
  -H "Content-Type:application/json" \
  -H "Authorization:JWT $TOKEN" \
  -d '{
      "query": "{messages (receiverId: \"$ID\") {edges {node {id text receiver { username } sender { username } datetime}}}}"
      ,"variables":null
    }' \
  -X POST 'http://localhost:8000/graphql/'  | python -m json.tool
```

### Queries:

* Getting info about the current user:
```
{
  me {
    id
    username
    email
  }
}

curl \
  -H "Content-Type:application/json" \
  -H "Authorization:JWT $TOKEN" \
  -d '{
      "query": "{me {id username email}}"
      ,"variables":null
    }' \
  -X POST 'http://localhost:8000/graphql/'  | python -m json.tool
```

* Getting a chat with a particular user:
```
{
  messages(dialogueId: "VXNlck5vZGU6Mw==") {
    edges {
      node {
        id
        text
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

* Getting a list of dialogues:
```
{
  myDialogues {
    edges {
      node {
        id
        user1 {
          username
        }
        user2 {
          username
        }
      }
    }
  }
}
```

### Mutations:

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

* Creating a dialogue:
```
mutation {
  createDialogue(input: {receiverId: "VXNlck5vZGU6Mg=="}) {
    dialogue {
      id
      user1 {
        username
      }
      user2 {
        username
      }
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
