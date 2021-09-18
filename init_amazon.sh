#!/bin/bash
sudo apt update
sudo apt install postgresql postgresql-contrib

# Remove this block if you don't want to use venv
if [ -d "env" ]
then
    sudo apt install python3.8-venv
    python3 -m venv env
    source env/bin/activate
    pip install -r requirements.txt
else
    source env/bin/activate
fi

# This process is interactive, you need to enter a password same as the one in config.py
sudo -u postgres psql postgres -c '\password'

# create the database
dbname=amazon
if [[ -n `sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -w "$dbname"` ]]; then
    sudo -u postgres dropdb $dbname
fi
sudo -u postgres createdb $dbname

# create tables in the database
sudo -u postgres psql -af create.sql $dbname

# populate the database with initial data:
# user 'icecream@tastes.good' has password 'test123' 
sudo -u postgres psql amazon -c "INSERT INTO users(id, email, password, firstname,lastname) VALUES (0,'icecream@tastes.good','pbkdf2:sha256:260000\$1GvmeoAkcWb89TyU\$5f711eafb243c1c1a884715dd9bd6d185f29ccd3dab59ad19cc201a7260091cb','Joey','Shmoey');"
# insert products
sudo -u postgres psql amazon -c "INSERT INTO products(pid,product_name,price,available) VALUES (1,'vanilla ice cream',2.99,true);"
sudo -u postgres psql amazon -c "INSERT INTO products(pid,product_name,price,available) VALUES (2,'chocolate ice cream',2.99,true);"
sudo -u postgres psql amazon -c "INSERT INTO products(pid,product_name,price,available) VALUES (3,'strawberry ice cream',2.99,true);"
sudo -u postgres psql amazon -c "INSERT INTO products(pid,product_name,price,available) VALUES (4,'6-pack of paycheck pilsners',11.49,true);"
sudo -u postgres psql amazon -c "INSERT INTO products(pid,product_name,price,available) VALUES (5,'seven fabergé easter eggs',1199000.00,true);"
sudo -u postgres psql amazon -c "INSERT INTO products(pid,product_name,price,available) VALUES (6,'painting - the storm on the sea of galilee',44000000.00,true);"
# insert previous purchases
sudo -u postgres psql amazon -c "INSERT INTO purchases(order_nr,uid,pid,time_purchased) VALUES (0,0,1,'2021-09-10 13:12:58');"
sudo -u postgres psql amazon -c "INSERT INTO purchases(order_nr,uid,pid,time_purchased) VALUES (1,0,2,'2021-09-11 13:17:23');"
sudo -u postgres psql amazon -c "INSERT INTO purchases(order_nr,uid,pid,time_purchased) VALUES (2,0,1,'2021-09-12 13:11:36');"
sudo -u postgres psql amazon -c "INSERT INTO purchases(order_nr,uid,pid,time_purchased) VALUES (3,0,2,'2021-09-13 13:19:01');"
sudo -u postgres psql amazon -c "INSERT INTO purchases(order_nr,uid,pid,time_purchased) VALUES (4,0,3,'2021-09-13 19:18:54');"