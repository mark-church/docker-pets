# Docker Pets
> written for `chrch/docker-pets:1.1`

Docker Pets is a simple application that's useful for testing out features of Docker Datacenter.

If you are interested in a guide on how to demo Docker Pets on the Universal Control Plane then check out [this tutorial](https://github.com/mark-church/docker-pets/blob/master/DEMO-DDC.md).

If you are interested in contributing to Docker pets please check out the [Release Notes & Roadmap.](https://github.com/mark-church/docker-pets/blob/master/ROADMAP.md).

Ppetsets is comprised of two images:

- `chrch/docker-pets` is a front-end Python Flask container that serves up random images of housepets, depending on the given configuration
- `consul` is a back-end KV store that stores the number of visits that the `web` services recieve. It's configured to bootstrap itself with 3 replicas so that we have fault tolerant persistence.

## Building Pets from Scratch
Pets is hosted on the Docker Hub but you can also build it locally.

```
$ git clone https://github.com/mark-church/docker-pets
$ cd docker-pets/web
$ docker build -t chrch/web:1.1 .
```



## Running Pets as a Single Container, Stateless App
```
$ docker run -it -p 5000:5000 chrch/docker-pets
```


## Running Pets on Docker for Mac/Windows in Development
Docker Swarm can easily be set up to run applications on a single developer laptop. The full app can be brought up to run in the same way it would run in production. We use a compose v3 file to deploy a fully fault tolerant frontend and backend, along with the configurations, secrets, and networks required for the application to run.
pets
This is the full architecture that is deployed when using [pets-dev-compose.yml](https://github.com/mark-church/docker-pets/blob/master/pets-dev-compose.yml).

```
$ git clone https://github.com/mark-church/docker-pets

~/docker-pets$ docker -v
Docker version 1.13.1-rc1, build 2527cfc

~/docker-pets$ docker node ls
ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
fd3ovikiq7tzmdr70zukbsgbs *  moby      Ready   Active        Leader

~/docker-pets$ docker stack deploy -c pets-dev-compose.yml pets
```

![](docs/images/pets-dev-arch.png) 


## Pets configuration parameters
The `web` container has several configuration parameters as environment variables:


- **`DB`**: Tells `web` where to find `db`. Service name or `<ip>:<port>`.
- **`DEBUG`**: Puts `web` containers in to debug mode. When mounting a volume for code, they will restart automatically when they detect a change in the code. Defaults to off, set to `True` to turn on.
- **`ADMIN_PASSWORD_FILE`**: Turns secrets on. If set, will password protect the Admin Console of `web`. Set to the full location of the Swarm secret (`/run/secrets/< X >`)

## Exposed Services
- Client Web Access - (dev port `5000`, prod URL `pets.dckr.org`)
	- `/` shows the selected Pet
	- `/vote` displays the vote selection
	- `/health` displays the application health of the given container
	- `/kill` toggles the health off for one of the web servers
- Admin Console - (dev port `7000`, prod URL `admin.pets.dckr.org`)
	- `/` displays voting results, redirects to `/login` if secrets are configured
	- `/login` requests login password
- Consul Backend - (dev port `8500`, prod ephemeral port)
	- `/ui` displays Consul server UI

## Voting Option Configuration

- **`OPTION_A`**: Defaults to 'Cats'. Pictures located in `/docker-petspets/web/static/option_a`
- **`OPTION_B`**: Defaults to 'Dogs'. Pictures located in `/docker-pets/web/static/option_b`
- **`OPTION_C`**: Defaults to 'Whales'. Pictures located in `/docker-pets/web/static/option_c`





## Running Ppetsets on Docker UCP in Production
This [full length tutorial](https://github.com/mark-church/docker-pets/blob/master/DEMO-DDC.md) will show you how to deploy and demo DDC with the pets app.

Production apps have entirely different requirements when it comes to security, deployment, and also security. Fortunately, deployment on Swarm & UCP is very much the same from development to production. Some minor additions to our compose file add in capabilities for secrets and also for L7 load balancing.

This is the full architecture that is deployed when using [pets-prod-compose.yml](https://github.com/mark-church/docker-pets/blob/master/pets-prod-compose.yml).

```
$ echo "mysecret" | docker secret create admin_password_v1 -
$ docker stack deploy -c pets-prod-compose.yml pets
```

![](docs/images/pets-prod-arch.png) 
