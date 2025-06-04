# chatgpttestapp

This is a minimal microblogging application similar to Twitter built with Flask.

## Setup

Install requirements and start the server:

```bash
pip install -r requirements.txt
python app.py
```

## API

- `POST /register` with form field `username` – register a user.
- `POST /post` with `username` and `content` – create a post.
- `POST /follow` with `follower` and `followee` – follow another user.
- `GET /feed?username=<name>` – get a feed of posts from the user and those they follow.
