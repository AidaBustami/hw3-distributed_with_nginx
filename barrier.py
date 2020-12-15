from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
from flask import  request, jsonify
import requests
import json

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
from flask import  request, jsonify
from flask import Flask
from flask_caching import Cache
import requests
import json

import hashlib
from flask import Flask, request
import redis



app = Flask(__name__)
api = Api(app)

ma = Marshmallow(app)


@app.route('/lookup/<item_id>', methods=['GET'])   
def buy(item_id):
    return
     
@app.route('/search/<book_topic>', methods=['GET'])   
def buy2(book_topic):
    return



        
@app.route('/buy/<book_id>', methods=['put'])   
def buy3(book_id):
    return        

@app.route('/book2/<book_id>', methods=['patch'])   
def buy4(book_id):
    return 


    

    




#,ssl_context= ('cert.pem', 'key.pem')
if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True, port="10000"  )