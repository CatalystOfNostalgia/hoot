# Hoot
Hoot is a full feature engine which analyzes the comments and reviews left on products. It takes these comments and analyzes the emotions which are conveyed in the comments. The backend is designed to be ran on an AWS EC2 instance. The data is meant to be stored on S3. The app is built for iOS. In order to install it is necessary to supply the necessary AWS Keys to the repo for it to be able to function on AWS.

## Server Installation Instructions
* Requirements
  * AWS public and private keys, as well as an Amazon Product Advertising API tag
  * Python 3.5
  * A server running Apache, we use Amazon EC2
  * an S3 bucket - though the code is currently hardcoded to put items in a bucket named "hootproject"

* Instructions

To run the server, an AWS EC2 server and S3 instance must be setup. This is because we make extensive use of these services. Apache is used to run the flask server, and python is used to run the data ingestor and the indexer.

To ingest data from a UCSD subset run the data_ingestor.py script with the --filename argument pointing to  gzip file downloaded from here http://jmcauley.ucsd.edu/data/amazon/links.html

Our server typically has 3 processes running at all times - the app.py process, the data_ingestor process, and the scraper.py file which searches for product updates
To index the ingested file, run indexer.py from the hoot/server directory. This will re-index everything and allow it to be searched by the API

## iOS App Installation Instructions
* Requirements
  * OSX
  * XCode
* Instructions

 Navigate to the Hoot folder and open the xcode project. Click on the "run" button in the top left corner of XCode.  
