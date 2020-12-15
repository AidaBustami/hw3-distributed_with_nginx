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
r = redis.Redis(
host='localhost',
port=6379,
password='')


app = Flask(__name__)
api = Api(app)

ma = Marshmallow(app)

count=0
count2=0
count3=0
count6=0
count7=0




	
        
        



class front_end1(Resource):
    
    def get(self,book_topic):
        global count
        hash = hashlib.md5(str.encode(book_topic)) 
        hashkey = str("search") + hash.hexdigest()
        val =r.get(name = hashkey)
        if(val is None or  len(val)<=1 ):
           
            response = requests.get("http://192.168.1.50:10000/" + "search/" +book_topic)
              
            
               
               


            
            if not response :
                data ={'message' : 'topic does not exsit'}
                r.set(name =hashkey , value = json.dumps(data), ex=300) 
                return  jsonify({'message' : 'topic does not exsit'})
            temppp=json.loads( str(response.content, 'utf-8'))  

            freedom=str (jsonify(temppp)) 
            r.set(name =hashkey , value =str(response.content, 'utf-8') , ex=300)
            return jsonify(temppp)
        else:
            return    jsonify (json.loads( val))              
api.add_resource(front_end1, "/search/<book_topic>")


@app.route('/lookup/<item_id>', methods=['GET'])   
def get2(item_id):
    global count2
    hash1 = hashlib.md5(str.encode(item_id)) 
    hashkey = str("lookup") + hash1.hexdigest()
    val =r.get(name = hashkey)
    if (val is None or  len(val)<=1 ):
       
        response = requests.get("http://192.168.1.50:10000/" + "lookup/" + str(item_id) )
            
        
          


        
        if not response:
            data ={'message' : 'id does not exsit'}
            r.set(name =hashkey , value = json.dumps(data) ,ex=300 ) 
             

            return jsonify({'message' : 'id does not exsit'})
        temppp=json.loads( str(response.content, 'utf-8'))
        r.set(name =hashkey , value =str(response.content, 'utf-8') , ex=3000) 
        return jsonify({"titel" :temppp['titel']  ,"price" :temppp['cost'] , "quantity": temppp['number_in_stock'] })
        #return jsonify (temppp)
    else :    
        return jsonify (json.loads( val))    




    
    
        
    


    


@app.route('/buy/<item_id>', methods=['put'])   
def buy(item_id):
    hash1 = hashlib.md5(str.encode(item_id))
    hashkey = str("buy") + hash1.hexdigest() 
    hashkey2 = str("lookup") + hash1.hexdigest()
    val =r.get(name = hashkey)
    if (not(val is None or  len(val)<=1 )):

        return  jsonify (json.loads( val)) 
         






    global count3
    
    response = requests.put("http://192.168.1.50:10000/" + "buy/"+ item_id)
       
    
        






    
    temppp=json.loads( str(response.content, 'utf-8'))


    if temppp['order_id'] ==-1 :
        data ={'message' : 'book does not exsist'}
        
        
        r.set(name =hashkey , value = json.dumps(data) , ex=300)
            
        












        

        
        val =r.get(name = hashkey2)
        if(val is None or  len(val)<=1 ):
            r.set(name =hashkey2 , value = json.dumps(data), ex=300)
            
        else:
            r.delete( hashkey2)  
            r.set(name =hashkey2 , value = json.dumps(data), ex=300)
              
        
        




        return jsonify({'message' : 'book does not exsist!'})
    if temppp['order_id'] == -2 :
        data ={'message' : 'quantity in stock is zero!'}
          
        r.set(name =hashkey , value = json.dumps(data), ex=300)



        
        

        return  jsonify({'message' : 'quantity in stock is zero!'}) 
    else:
        hash = hashlib.md5(str.encode(item_id)) 
        hashkey = str("lookup") + hash.hexdigest()
        val =r.get(name = hashkey)
        if(val is None or  len(val)<=1 ):
            return jsonify(temppp)
        else:
            r.delete( hashkey)  
            return jsonify(temppp)  




        
        




    

    
@app.route('/increment_quantity_in_stock/<item_id>', methods=['put'])   
def inc(item_id):
    global count6
    if (count6 == 0):
        response = requests.post("http://192.168.1.50:6000/" + "book_incraese_in_stock", {"item_id" :item_id})
        count6=1
    elif count6==1 :
        response = requests.post("http://192.168.1.50:7000/" + "book_incraese_in_stock", {"item_id" :item_id})    
        count6=2
    else:
        response = requests.post("http://192.168.1.50:9000/" + "book_incraese_in_stock", {"item_id" :item_id})
        count6=0




    
    if not response:
        return jsonify({'message' : 'book does not exsist!'})
    temppp=json.loads( str(response.content, 'utf-8'))
    return jsonify(temppp)


@app.route('/deccrement_quantity_in_stock/<item_id>', methods=['put'])   
def dec(item_id):
    global count7
    if (count7==0):
        response = requests.post("http://192.168.1.50:6000/" + "book_decraese_in_stock", {"item_id" :item_id})
        count7=1
    elif count7 == 1:
        response = requests.post("http://192.168.1.50:7000/" + "book_decraese_in_stock", {"item_id" :item_id})  
        count7=2
    else:
        response = requests.post("http://192.168.1.50:9000/" + "book_decraese_in_stock", {"item_id" :item_id}) 
        count7=0




    
    temppp=json.loads( str(response.content, 'utf-8'))
    if  temppp[0]['titel'] == None:
        return jsonify({'message' : 'book does not exsist!'})
        
    if temppp[0]['titel']=="zero" :
        return jsonify({'message' : 'zero quantity'})
    
    return jsonify(temppp[0])



class front3(Resource):
    def put(self):        
        catalog89_update_args = reqparse.RequestParser()
        catalog89_update_args.add_argument("item_id", type=str, help="#id")
        catalog89_update_args.add_argument("topic", type=str, help="#topic")
        args = catalog89_update_args.parse_args()
        hash1 = hashlib.md5(str.encode(args['item_id'])) 
        hash2 = hashlib.md5(str.encode(args['topic'])) 
        hashkey = str("lookup") + hash1.hexdigest()
        

        hash_key2 =str("search") + hash2.hexdigest()
        hash3=str("buy") + hash1.hexdigest()
        val =r.get(name = hashkey)
        if(not (val is None or  len(val)<=1 )):
           
        
            r.delete( hashkey)    
        val =r.get(name = hash_key2)   
        if(not (val is None or  len(val)<=1 )):
            r.delete( hash_key2) 
        val =r.get(name = hash3)
        if(not (val is None or  len(val)<=1 )):
           
        
            r.delete( hash3)     






		
api.add_resource(front3, "/consistant")
class front4(Resource):
    def put(self):        
        catalog89_update_args = reqparse.RequestParser()
        catalog89_update_args.add_argument("item_id", type=str, help="#id")
        catalog89_update_args.add_argument("topic", type=str, help="#id")
        args = catalog89_update_args.parse_args()
        hash1 = hashlib.md5(str.encode(args['item_id'])) 
        hash2 = hashlib.md5(str.encode(args['topic'])) 
        hashkey = str("lookup") + hash1.hexdigest()
        

        hash_key2 =str("search") + hash2.hexdigest()
        hash3=str("buy") + hash1.hexdigest()
        val =r.get(name = hashkey)
        if(not (val is None or  len(val)<=1 )):
            r.delete( hashkey)   

           
        
               
        val =r.get(name = hash_key2)   
        if(not (val is None or  len(val)<=1 )):
            r.delete( hash_key2) 
        val =r.get(name = hash3)      

        if(not (val is None or  len(val)<=1 )):
            r.delete(hash3) 






		
api.add_resource(front4, "/consistant2")




#,ssl_context= ('cert.pem', 'key.pem')
if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True, port="8000"  )