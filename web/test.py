from flask import Flask, render_template, request, make_response
import random, socket, time, json, os, sys, ast, consul

option_a = os.getenv('OPTION_A', "Cats")
option_b = os.getenv('OPTION_B', "Dogs")
option_c = os.getenv('OPTION_C', "Whales")
option_d = os.getenv('OPTION_D', "Penguins")
hostname = socket.gethostname()
debug = True

app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def index():

    #vote_cookie = request.cookies.get('vote')

    #if vote_cookie:


    if request.method == 'POST':
        vote = request.form['vote']

    voter_id = hex(random.getrandbits(64))[2:-1]

    resp = make_response(render_template(
        'test.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        vote=vote,
    ))

    resp.set_cookie('voter_id', voter_id)


    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=debug)
