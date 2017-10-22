import os
from functools import wraps
from collections import Counter

from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['wc_secret_key'] = os.environ.get('WC_SECRET_KEY')

def wc_secret_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.form.get('wc_secret_key') != app.config['wc_secret_key']:
            response = jsonify({
                'text': 'Bad authorization'
            })
            response.status_code = 401
            return response
        return f(*args, **kwargs)
    return decorated_function

@app.route('/wc', methods=['POST'])
@wc_secret_key_required
def wc():
    text = request.form.get('text')
    if text:
        word_list = str(text).lower().split()

        counter = Counter()
        for word in word_list:
            counter[word] += 1;

        most_common_word, count = counter.most_common(1)[0]
        return jsonify({
            'word_count': len(word_list),
            'most_common': {
                'word': most_common_word,
                'count': count
            }
        })

    response = jsonify({
        'text': 'The `text` body parameter is required.'
    })
    response.status_code = 422
    return response


