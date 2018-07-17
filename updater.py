import io
import os
import json
from hashlib import sha1
import hmac

import git
from flask import Flask, request, abort


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def main():

    with io.open("secret", 'r') as f:
        secret = f.read()

    header_signature = request.headers.get('X-Hub-Signature')
    if header_signature is None:
        abort(403)

    sha_name, signature = header_signature.split('=')
    if sha_name != 'sha1':
        abort(501)

    mac = hmac.new(secret.encode(), msg=request.data, digestmod=sha1)

    if not hmac.compare_digest(str(mac.hexdigest()), str(signature)):
        abort(403)

    data = json.loads(request.data.decode())
    user = data['sender']['login']
    contributors = {}

    if os.path.isfile("contributors.json"):
        with io.open("contributors.json", 'r') as f:
            contributors = json.load(f)
    else:
        contributors = {}

    if user in contributors:
        contributors[user] += 1

    else:
        contributors[user] = 1

    with io.open("contributors.json", 'w') as f:
        json.dump(contributors, f)

    contributors_str = (
        "# Contributors\nThese people have helped write this "
        "collection of information about the game! If you see them in-game, "
        "give them a pat on the back and some fireworks :)\n\n")

    for k in sorted(contributors, key=contributors.get, reverse=True):
        contributors_str = (
            contributors_str + "- %s (%d edits)" % (k, contributors[k]) + "\n")

    with io.open("contributors.md", 'w') as f:
        f.write(contributors_str)

    g = git.cmd.Git("wiki")
    g.pull()

    return str({"message": "success"})


if __name__ == '__main__':
    app.run(host="localhost", port=7878, debug=False)
