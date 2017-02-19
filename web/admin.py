from flask import Flask, render_template, request, make_response, redirect
import random, socket, time, json, os, sys, ast, consul

db = os.getenv('DB')
debug = os.getenv('DEBUG', False)
pass_file = os.getenv('ADMIN_PASSWORD_FILE', None)

option_a = os.getenv('OPTION_A', "Cats")
option_b = os.getenv('OPTION_B', "Dogs")
option_c = os.getenv('OPTION_C', "Whales")

hostname = socket.gethostname()

admin_id_list = []

if pass_file is not None:
    if os.path.isfile(pass_file):
        f = open(pass_file, 'r')
        password = f.readline().rstrip()
    else:
        print "Incorrect ADMIN_PASSWORD_FILE location given. Given file does not exist."
        pass_file = None

app = Flask(__name__)

images = ["https://bloglaurel.com/uploads/2015/10/blog-docker-bloglaurel-ghd-square.jpg"]

url = random.choice(images)

if db:
    if ':' in db:
        (address, port) = db.split(':')
    else:
        address = db
        port = 8500
        db = address + ':' + str(port)

    time.sleep(5)
    
    #Connect to Consul
    c = consul.Consul(host=address, port=port)
else:
    print "No DB given"



@app.route('/', methods=['GET', 'POST'])
def index():
    admin_id = request.cookies.get('paas_admin_id')

    if pass_file is None:
        return redirect('/admin')

    error = None
    if request.method == 'POST':
        if request.form['password'] != password:
            error = 'Invalid credentials.'
        else:
            #Succesful password entry, create admin_id, set cookie
            admin_id = hex(random.getrandbits(64))[2:-1]
            admin_id_list.append(admin_id)
            response = make_response(redirect('/admin'))
            response.set_cookie('paas_admin_id', value=admin_id)
            return response

    return render_template('login.html', error=error, url=url)


@app.route('/admin', methods=['POST','GET'])
def console():
    admin_id = request.cookies.get('paas_admin_id')

    #if (admin_id not in admin_id_list) and (admin_password_file):
     #   return redirect('/')

    if request.method == 'POST':
        pass

    a_votes = int(c.kv.get(option_a)[1]["Value"])
    b_votes = int(c.kv.get(option_b)[1]["Value"])
    c_votes = int(c.kv.get(option_c)[1]["Value"])

    return render_template('admin.html',
        option_a=option_a,
        option_b=option_b,
        option_c=option_c,
        a_votes=a_votes,
        b_votes=b_votes,
        c_votes=c_votes,
        hostname=hostname)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000, debug=debug)
