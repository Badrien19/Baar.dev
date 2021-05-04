
# How to put your site online

## 1 setup vps
    
    firewall, accept 22 443 80

## 2 setup ovh
    
    entrée "A" baar.dev -> ip vps
    entré "C name" www.baar.dev -> baar.dev.

## 3 setup le vps
    
###    Install python3 sur le serveur:
[Tuto link's](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-ubuntu-18-04-quickstart)
    
    apt update
    apt upgrade
    apt install git
    apt install python3-pip
    apt install python3-venv
    
    mkdir .venv
    cd .venv
    python3 -m venv baar.dev
    source baar.dev/bin/activate
    
    
### Installer et configurer nginx sur le serveur:
[Tuto link's](https://www.digitalocean.com/community/tutorials/comment-installer-nginx-sur-ubuntu-18-04-fr)
    
    apt install nginx
    cd /var/www
    git clone https://github.com/badrien19/baar.men
    (rm db.sqlite3)
    pip3 install -r requirements.txt
    
    python3 manage.py migrate
    python3 manage.py collectstatic
    python3 manage.py runserver

    cd /etc/nginx/sites-available/

    nginx -t
    service nginx restart

    vim baar.dev (voir nginx_config)
    ln -s /etc/nginx/sites-available/baar.dev /etc/nginx/sites-enabled/baar.dev

    Securiser nginx (tls/https): https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04-fr
    
    apt install certbot python3-certbot-nginx
    certbot --nginx -d baar.dev -d www.baar.dev
    
    
### Lancer le serveur django avec un daemon gunicorn:
[Tuto link's](https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-20-04-fr)
    
    (seulement une partie du tuto concerne ca)

    pip install gunicorn
    
    cd /etc/systemd/system/
    vim baar.dev.service (voir gunicorn_config)
    
    systemctl start baar.dev
    systemctl enable baar.dev
    systemctl status baar.dev
