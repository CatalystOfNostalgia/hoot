# Install all necessary python modules 
# Also creates a virtual env to work with. 
install:
	brew install mysql
	sudo pip install virtualenv
	virtualenv env
	env/bin/pip install -Ur requirements.txt;
	@echo 'installed'


# Start the mysql server
# And other things 
# If you are getting an error run 'source env/bin/activate'
run:
	/usr/local/bin/mysql.server restart
	mysql -u root < sql/create_tables.sql
	#chmod a+x hoot/app.py
	#hoot/./app.py

# run the test suite
# WARNING will wipe the DB
test:
	@/usr/local/bin/mysql.server restart
	@mysql -u root < sql/create_tables.sql
	@python3 hoot/test.py

# Deactivate virtualenv and delete it. 
# Delete all the things 
clean:
	/usr/local/bin/mysql.server stop
	rm -rf env/
