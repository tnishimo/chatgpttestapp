from flask import Flask, request, jsonify
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

# In-memory storage
users = set()
followers = defaultdict(set)
posts = []

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    if not username:
        return jsonify({'error': 'username required'}), 400
    if username in users:
        return jsonify({'error': 'user exists'}), 400
    users.add(username)
    return jsonify({'message': f'{username} registered'})

@app.route('/post', methods=['POST'])
def post():
    username = request.form.get('username')
    content = request.form.get('content')
    if not username or not content:
        return jsonify({'error': 'username and content required'}), 400
    if username not in users:
        return jsonify({'error': 'unknown user'}), 400
    posts.append({'user': username, 'content': content, 'time': datetime.utcnow()})
    return jsonify({'message': 'post created'})

@app.route('/follow', methods=['POST'])
def follow():
    follower = request.form.get('follower')
    followee = request.form.get('followee')
    if not follower or not followee:
        return jsonify({'error': 'follower and followee required'}), 400
    if follower not in users or followee not in users:
        return jsonify({'error': 'unknown user'}), 400
    followers[follower].add(followee)
    return jsonify({'message': f'{follower} now follows {followee}'})

@app.route('/feed', methods=['GET'])
def feed():
    username = request.args.get('username')
    if not username or username not in users:
        return jsonify({'error': 'unknown user'}), 400
    followees = followers[username] | {username}
    user_posts = [p for p in posts if p['user'] in followees]
    user_posts.sort(key=lambda p: p['time'], reverse=True)
    formatted = [{'user': p['user'], 'content': p['content'], 'time': p['time'].isoformat()} for p in user_posts]
    return jsonify({'feed': formatted})

if __name__ == '__main__':
    app.run(debug=True)
