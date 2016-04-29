# Hoot
Hoot is a full feature engine which analyzes the comments and reviews left on products. It takes these comments and analyzes the emotions which are conveyed in the comments. The backend is designed to be ran on an AWS EC2 instance. The data is meant to be stored on S3. The app is built for iOS. In order to install it is necessary to supply the necessary AWS Keys to the repo for it to be able to function on AWS.

# Installation
Development requires XCode for the front end and a python environment for the server.

Python version 3.5 is used. To run the IOS application, launch the project on XCode and select any iPhone version for the simulator.

To run the server, an AWS EC2 server and S3 instance must be setup. This is because we make extensive use of these services. Apache is used to run the flask server, and python is used to run the data ingestor and the indexer. Amazon AWS keys and a Product Advertising API must be put in the hoot/server/hoot/keys/aws_keys.json file since the aws_module.py uses that to authenticate the various Amazon libraries.

Running the iOS app is very simple. It requires a device running OSX and the XCode app. To open the project, navigate to hoot/Hoot and click the Hoot.xcodeproj. This will open the project in XCode. Make sure that the simulated device is either an iPhone6s or iPhone6s plus. This is selected in the top left of XCode. Then hit the run button which is found in the top left of XCode. This will build the app and bring up a simulator with the app running in it

To ingest data from a UCSD subset run the data_ingestor.py script with the --filename argument pointing to  gzip file downloaded from here http://jmcauley.ucsd.edu/data/amazon/links.html

Our server typically has 3 processes running at all times - the app.py process, the data_ingestor process, and the scraper.py file which searches for product updates
