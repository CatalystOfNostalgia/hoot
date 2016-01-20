# Install all necessary python modules 
# Also creates a virtual env to work with. 
install:
	brew install mysql
	sudo pip install virtualenv
	virtualenv env
	source env/bin/activate;
	env/bin/pip install -Ur requirements.txt;
	@echo 'installed'


# Start the mysql server
# And other things 
run: install 
	/usr/local/bin/mysql.server restart
	mysql -u root < sql/create_tables.sql

# Deactivate virtualenv and delete it. 
# Delete all the things 
clean:
	/usr/local/bin/mysql.server stop
	rm -rf env/
