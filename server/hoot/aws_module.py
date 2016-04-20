import json, boto, boto.s3.connection, bottlenose, os.path
from boto.s3.key import Key
from urllib.error import HTTPError

# Load the AWS key information
f = open(os.path.dirname(os.path.realpath(__file__)) + "/keys/aws_keys.json")
configs = json.loads(f.read())

s3conn = boto.connect_s3(aws_access_key_id=configs["aws_public_key"],aws_secret_access_key=configs["aws_secret_key"])
bucket = s3conn.get_bucket("hootproject")

def error_handler(err):
    ex = err['exception']
    if isinstance(ex, HTTPError) and ex.code == 503:
        time.sleep(random.expovariate(0.1))
        return True

def setup_product_api():
    return bottlenose.Amazon(configs["aws_public_key"],
                             configs["aws_secret_key"],
                             configs["product_api_tag"],
                             ErrorHandler=error_handler,
                             MaxQPS=0.9)

def push_to_S3(filename, jsonToUpload):
    k = Key(bucket)
    k.key = filename
    k.set_contents_from_string(jsonToUpload)

def retrieve_from_S3(filename):
    key = bucket.new_key(filename)
    contents = key.get_contents_as_string()
    return contents