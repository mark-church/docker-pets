from flask import Flask, render_template, request, make_response, redirect
import random, socket, time, json, os, sys, ast, consul

option_a = os.getenv('OPTION_A', "Cats")
option_b = os.getenv('OPTION_B', "Dogs")
option_c = os.getenv('OPTION_C', "Whales")
vote = option_a

db = os.getenv('DB', False)
db_exists = False
debug = os.getenv('DEBUG', False)
threaded = os.getenv('THREADED', False)

option_a_images = os.listdir('./static/option_a')
option_b_images = os.listdir('./static/option_b')
option_c_images = os.listdir('./static/option_c')


healthy = True
version ='1.0'
hostname = socket.gethostname()

print "Starting web container %s" % hostname

app = Flask(__name__)

if db:

    db_exists = True

    if ':' in db:
        (address, port) = db.split(':')
    else:
        address = db
        port = 8500
        db = address + ':' + str(port)

    time.sleep(5)
    
    #Connect to Consul
    c = consul.Consul(host=address, port=port)

    #Test to see Consul values need to be zeroed
    if c.kv.get('hits')[1] == None:
        c.kv.put('hits', '0')
        c.kv.put(option_a, '0')
        c.kv.put(option_b, '0')
        c.kv.put(option_c, '0')


@app.route('/')
def index():
    
    vote_cookie = request.cookies.get('vote')

    
    if db is False:
        vote = option_b
    elif vote_cookie is None:
        return redirect('/vote')
    else:
        vote = vote_cookie
        

    #Health check test that toggles image
    if healthy == True:
        url = get_image(vote)
    else:
        url = "../static/error.png"
    
    if db:
        x, hits = c.kv.get('hits')
        newHits = int(hits["Value"]) + 1
        c.kv.put('hits', str(newHits))
        hit_string = str(newHits) + " Pets Served"

    if not db:
        hit_string = ""
        db_exists == str(db_exists)

    return render_template('pets.html', url=url, hostname=hostname, hit_string=hit_string, title=vote, version=version, db_exists=db_exists)

@app.route("/vote", methods=['POST','GET'])
def vote():

    vote = option_a
    

    if request.method == 'POST':
        vote = request.form['vote']
        name = request.form['name']

        x, hits = c.kv.get('hits')

        if vote == 'a':
            vote = option_a
        elif vote == 'b':
            vote = option_b
        elif vote == 'c':
            vote = option_c
        else:
            print 'error'

        #Record name & vote
        c.kv.put(name, vote)

        #Record vote total
        votes_total = int(c.kv.get(vote)[1]["Value"]) + 1
        c.kv.put(vote, str(votes_total))

        response = make_response(redirect('/'))
        response.set_cookie('vote', value=vote)

        return response


    response = make_response(render_template(
        'vote.html',
        option_a=option_a,
        option_b=option_b,
        option_c=option_c,
        hostname=hostname,
        vote=vote,))

    response.set_cookie('vote', value=vote)
    return response



@app.route('/health', methods=['GET', 'PUT'])
def health():
    global healthy
    if request.method == 'GET':
        if healthy:
            return 'OK', 200
        else:
            return 'NOT OK', 500
    elif request.method == 'PUT':
        if request.headers['Content-Type'] == 'application/json':
            healthy = ast.literal_eval(str(request.json["healthy"]))
            if healthy == True:
                return "healthy"
            if healthy == False:
                return "not healthy"
    else:
        return 'ERROR REQUEST MTHD', 500

@app.route('/kill')
def kill():
    global healthy
    healthy = False
    return 'You have toggled web instance ' + hostname +' to unhealthy', 200


def get_image(vote):
    if vote == option_a:
        image_file = './static/option_a/' + random.choice(option_a_images)
    elif vote == option_b:
        image_file = './static/option_b/' + random.choice(option_b_images)
    elif vote == option_c:
        image_file = './static/option_c/' + random.choice(option_c_images)
    else:
        sys.stdout.write("Error: no valid role")
        sys.exit(1)

    return image_file

#curl -X PUT -H 'Content-Type: application/json' -d '{"healthy": "False"}' http://localhost:5000/health
#curl -X PUT -H 'Content-Type: application/json' -d '{"healthy": "True"}' http://localhost:8000/health
#curl -v http://localhost:8000/health

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=debug, threaded=threaded)
