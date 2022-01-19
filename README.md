
         _______.____    ____      _______..___  ___.  __   __  ___      ___              _______. _______   __  ___ 
        /       |\   \  /   /     /       ||   \/   | |  | |  |/  /     /   \            /       ||       \ |  |/  / 
       |   (----` \   \/   /     |   (----`|  \  /  | |  | |  '  /     /  ^  \          |   (----`|  .--.  ||  '  /  
        \   \      \_    _/       \   \    |  |\/|  | |  | |    <     /  /_\  \          \   \    |  |  |  ||    <   
    .----)   |       |  |     .----)   |   |  |  |  | |  | |  .  \   /  _____  \     .----)   |   |  '--'  ||  .  \  
    |_______/        |__|     |_______/    |__|  |__| |__| |__|\__\ /__/     \__\    |_______/    |_______/ |__|\__\
    ====================================================================================================================



# About

Tools to enhance the Sysmika ERPs by adding integrations with external systems. Each integration is built using
a microservice approach, in which each service (integration) comes OOTB with a basic set of operations:
* Authentication against the external system
* Basic CRUD operations 
* An internal in-memory database to cache transactions
* Test suite

Each service exposes an API, which is defined using the [OpenAPI](https://swagger.io/) specification. 

# Installation

## Linux (for development/production)

* Install Python 3.9 and Pip
* Install Mysql, and python3.9-dev headers
* Install Redis by running these commands
  * $ redisurl="http://download.redis.io/redis-stable.tar.gz"
  * $ curl -s -o redis-stable.tar.gz $redisurl
  * $ sudo su root
  * $ mkdir -p /usr/local/lib/
  * $ chmod a+w /usr/local/lib/
  * $ tar -C /usr/local/lib/ -xzf redis-stable.tar.gz
  * $ rm redis-stable.tar.gz
  * $ cd /usr/local/lib/redis-stable/
  * $ make && make install
* Create a config file in /etc/redis called **6379.conf** and with these configuration parameters
  ``` 
  # /etc/redis/6379.conf
  port			6379
  daemonize		yes
  save			60 1
  bind			127.0.0.1
  tcp-keepalive		300
  dbfilename		dump.rdb
  dir			./
  rdbcompression		yes`
  ```
* Run __sudo apt install pipenv__
* Go to the root of the project and run __pipenv shell__ and __pipenv install__
* Create a Database in Mysql or any other DB engine
* From the root of the project run __python manage.py makemigrations__ and then __python manage.py migrate__
  * This will create all tables in the Database
* Start the Redis server: __redis-server /etc/conf/6379.conf
  * Verify that is running using __redis-cli PING__
* Start the Celery worker from the root of the project __celery -A  conf worker --loglevel=info__ # TODO daemonize the worker
* Start Django by running __pipenv run server__ from the project root.


# Project Structure
 # TODO

# Roadmap

`TODO`