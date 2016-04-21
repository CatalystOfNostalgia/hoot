# Install all necessary python modules 
# Also creates a virtual env to work with. 
install-mac:
	brew install mysql
	brew install python3
	pip install virtualenv
	virtualenv -p /usr/bin/python3 env
	env/bin/pip install -Ur requirements.txt;
	@echo 'installed'

install-server:
	sudo apt-get install mysql
	sudo apt-get install python3
	sudo apt-get install python-virtualenv
	virtualenv -p /usr/bin/python3 env
	env/bin/pip install -Ur requirements.txt;
	@echo 'installed'

# Start the mysql server
# And other things 
# If you are getting an error run 'source env/bin/activate'
run:
	/usr/local/bin/mysql.server restart
	mysql -u root < sql/create_tables.sql
	chmod a+x hoot/app.py
	hoot/app.py

# Used to move the directory after pulling
update_dir:
	rm -rf /var/www/html/hoot/
	cp -r /home/ubuntu/hoot/server/. /var/www/html/hoot/

# run the test suite
# WARNING will wipe the DB
test:
	@/usr/local/bin/mysql.server restart
	@mysql -u root < sql/create_tables.sql
	@python3 hoot/testing/test.py

# Delete all the things 
clean:
	rm -rf env/
	find . | \
		grep -E "(__pycache__|\.pyc$)" | \
		xargs rm -rf
