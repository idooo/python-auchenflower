

Auchenflower framework
======================



This is another simple python framework for rapid web development.

It is include:

- Built-in wsgi server above CherryPy

- Simple MVC model

- Views based on Jinja2 templates

- SASS compiler based on libsass

- MongoDB db layer based on pymongo



Install
-------

1) Clone this repository



2) Install requirements

(Auchenflower framework requires CherryPy, jinja2, libsass and pymongo
(optional)), you can easly install all of these by using pip. Execute this command in
project directory:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
pip install -r requirements.txt
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



3) Create your configuration file in `./conf/` or use the existing one. By
default Auchenflower will use `./conf/default.conf `



4) Run loader script by execute this in Auchenflower directory:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
./loader.sh [config name]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



5) Now you can find your website here (by standard `default.conf`):

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
http://127.0.0.1:8085
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





Optimal configuration
---------------------

The optimal thing is to use nginx web-server (or something like this) in
the front of your website to deliver static content. In this case you should:



1) Configure your website to run local:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# config file 
... 
server.socket_host = "127.0.0.1" 
server.socket_port = 8081 
site.host = "my-server.com" 
...
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



2) Configure your nginx (for example) webserver as a reverse proxy:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# something like this in /etc/nginx/sites-enabled/default
# ...

server { 
    root /usr/share/nginx/www; 
    index index.html index.htm; 
    server_name my-server.com; 

    location / {
        proxy_pass http://127.0.0.1:8081; 
        proxy_set_header   X-Real-IP $remote_addr; 
        proxy_set_header   Host $http_host; 
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for; 
    } 
}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~










