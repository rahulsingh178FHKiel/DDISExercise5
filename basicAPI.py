from flask import Flask, request, jsonify, make_response
import jwt
import datetime
import psycopg
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xd5%\x8d6\x17\xa6\x06\xf8\xb6\x88\xb4\x18V\x92\x9cU\x9d\x97\x84)\xd7\xd7g'  # replace with your secret key
item_id_list = ["rrbmxm","evyalg","bcjkqo","ejhgbs","gnnvdj","tshsxl","dxxgzh","wexwtx","isvlvh","fsngtz","pxdxev","mldkng","fngmhl","gfxiwb","uvhqmy","vafllf","uwrqam","gsnumq","etyewq","exuwjp","ybiscu","gzycki","ohkixg","brkzhd","ycpqjq","ajveho","lkjwkx","duwlwa","gpdpqn","bbhxko","vkgymq","kytvdj","vcemho","nxddqu","suxtrh","fiecss","wgghtd","jxlsve","zxfcos","ioktdf","admpeu","dtuiho","spveux","nvdcfc","uimnho","jvhspo","aregmb","ovymuh","hmpgob","ttfrlz","xwurki","qzdtir","fdvaae","sjnvzr","gjrrqk","datftz","yxdgsq","pwyxmu","ukedaa","uuabtq","fulatm","qmqqmc","yyuvam","dvblze","cjxjkz","dfohcz","vyfjgn","kvqpol","yofbso","yuttmu","iyqxuw","rkwbqn","eimjgo","reuizz","amtdlp","ciiyol","geaset","mphiog","pkkrek","pmcpne","zqmfah","ajsqom","krksvr","mrzcgk","eajfjr","zeumvr","nwsven","xbehkp","egqqsn","vcklex","byjqyu","gjjhoy","izrvai","gmurfr","qfaoty","noejqg","imtpqz","rkjqki","qxfdvy","qpzutp","tmtsen","aidivo","asshsm","pioiim","poptro","vbcfgm","vbhvhi","uehwqu","pgteio","ozlowa","ynwasd","qxdqra","izykvw","plprhp","nuqqnw","spnnai","jdyove","goxhoa","caxxjr","jdfdec","bwpcqf","dbpcsw","itglmp","mygpzv","yymqar","iqdpyg","rwtzni","mxsyri","aygvyq","yhujjy","lstwzr","aaygur","czemac","nhlpjv","riopsx","wdntzk","ctmafc","zhuqgp","qwmfmv","mcijzd","hxyxne","vnqaat","tdqfqk","tlggvj","aqgron","xuwzth","dcxsue","agpmnl","mvuebc","qpgjhi","tvmfil","bwizve","yjgpbr","htfnsa","tpujiy","fburnl","aqymds","fplgvo","fzwzlg","ioppue","ytpkcd","ydaprg","ogruxy","jmhtih","irshav","vjizbk","ltatmd","bjiuny","wbgygw","psxcyj","dvgbfj","rqocwb","hlwfeu","hxvlgz","uyyrtg","laqlac","beusvq","fknngh","ytmxyr","bjlgoi","fohydh","jedfpg","aqqipn","lruikl","crmpyu","ilrihn","mmyfga","ntwgvr","cdfgkf","aczckm","tfzrvy","lxubxe","bfgzdc","zktxbz","wmddko","igsvdu","crhcxp","jpjfvq","ipewvc","whnlbh","ooytwz","haopxf","ncqdga","cmtlrw","xbqxdq","dccpfo","hfeapf","wyavcb","flawgq","basofg","jllcqe","rxuoio","bssxdx","txlkth","llozov","qxixqv","mlcloa","bgpwfe","imzthu","srbcgu","vqgqxm","nleyoe","btbqel","pxoekd","ggxjru","qitggo","xaxrkx","uuokzi","csigye","hmhypt","sbrwpy","lbgtdk","libemw","wvctld","tstrdi","qmqyth","zpfwed","ijccfh","zddhtu","sloylb","vfnkbf","egyrnd","hpwytd","ddrikq","hfdypg","yxfjrr","bofgok","npluzj","awqfuw","evayxm","yroutt","ixtqae","fpyuet","wthbut","pnghmn","oqttsz","easwyx","yxtxol","mtoyil","ejmmcj","cporna","zigxmc","cspgzf","dbahmx","gkaxxn","ldsljt","pxahto","sghbrg","twydcd","qgwtgr","bwmvwl","ltrbsu","fgqerb","gfscqw","sjacet","ojzdbz","wqrkou","xbkbaj","wfebqn","qhtbpt","odkgol"]
URL = "postgresql://root@35.195.74.177:26257/the_shop"

def random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def verify():
    auth_header = request.headers.get('Authorization')
    parts = auth_header.split(' ')
    if len(parts) == 2 and parts[0] == 'Bearer':
        # The second part is the JWT token
        jwt_token = parts[1]
        try:
            # Decode the token using the secret key
            payload = jwt.decode(jwt_token, app.config['SECRET_KEY'], algorithms=['HS256'])
            # return payload
            return True
        except jwt.ExpiredSignatureError:
            # Signature has expired
            return 'Token timed out.'
        except jwt.InvalidTokenError:
            # Token is invalid
            return 'Invalid user token.'    
    else:
        return 'Invalid Authorization header format.'    
        
        
    
#Case 1
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return make_response('Email and/or password was not provided', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    # URL = "postgresql://root@35.195.74.177:26257/the_shop"
    with psycopg.connect(URL) as conn:
        print("Connected to DB")
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE email='"+data.get('email')+"'")
        result = cursor.fetchall()
        for row in result:
            print("in result")
            print(row)
            password = ''.join(result[0])
        cursor.close()
    conn.close()

    # cases 
    #if result has nothing or just [] then the email doesn't exist
    if data.get('password') != password:
        return make_response('Password verification failed', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
 
    jwttoken = jwt.encode({'email' : data.get('email'), 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])

    return jsonify(token=jwttoken)

#Case 2
#/userinfo  
@app.route('/userinfo', methods=['GET'])
def case2():
    validation_result = verify()

    if isinstance(validation_result, str):  
        return jsonify({"message": validation_result}), 401
    else:  
        with psycopg.connect(URL) as conn:
            print("Connected to DB")
            cursor = conn.cursor()
            user_id = str(request.args.get('user_id'))
            query = "SELECT *  FROM users WHERE uid='"+user_id+"';"
            print(query)
            cursor.execute(query)
            result = cursor.fetchall()
            #CHeck first if the record is present. Omit out the password from the tuple
            if not result:
                return make_response('User id was not found.', 404, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
            else:
                # userAttributes = list(result)
                userAttributes = [item for sub in result for item in sub]
                print(userAttributes[0])
                del userAttributes[4]
                return jsonify(userAttributes)
            cursor.close()
        conn.close()

#Case 3
# GET /saleoffers
@app.route('/saleoffers', methods=['GET'])
def case3():

    validation_result = verify()

    if isinstance(validation_result, str):  
        return jsonify({"message": validation_result}), 401
    else:  
        with psycopg.connect(URL) as conn:
            print("Connected to DB")
            cursor = conn.cursor()
            query=returnRecords("sales")
            cursor.execute(query)
            result = cursor.fetchall()
            #CHeck first if the record is present. Omit out the password from the tuple
            if not result:
                return make_response('User id was not found.', 404, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
            else:
                return jsonify(result)
            cursor.close()
        conn.close()


#Case 4
# GET /purchases
@app.route('/purchaseoffers', methods=['GET'])
def case4():
    validation_result = verify()
    if isinstance(validation_result, str):  
        return jsonify({"message": validation_result}), 401
    else:  
        with psycopg.connect(URL) as conn:
            print("Connected to DB")
            cursor = conn.cursor()
            query=returnRecords("purchases")
            cursor.execute(query)
            result = cursor.fetchall()
            #CHeck first if the record is present. Omit out the password from the tuple
            if not result:
                return make_response('User id was not found.', 404, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
            else:
                return jsonify(result)
            cursor.close()
        conn.close()


#Case 5
# GET /sales?user_id=123
@app.route('/offerbyuserid', methods=['GET'])
def case5():
    print("in case 5")
    validation_result = verify()
    if isinstance(validation_result, str):  
        return jsonify({"message": validation_result}), 401
    else:  
        with psycopg.connect(URL) as conn:
            print("Connected to DB")
            cursor = conn.cursor()
            user_id = str(request.args.get('user_id'))
            cursor.execute("SELECT * FROM sales  WHERE buyer_uid IS NULL AND seller_uid ='"+user_id+"';")
            result = cursor.fetchall()
            if not result:
                output = "No offers were found for this user"
            else:
                output = result
            return jsonify(output)
            cursor.close()
        conn.close()

@app.route('/offerby100users', methods=['GET'])
def case6():
    validation_result = verify()
    if isinstance(validation_result, str):  
        return jsonify({"message": validation_result}), 401
    else:  
        with psycopg.connect(URL) as conn:
            print("Connected to DB")
            cursor = conn.cursor()
            query = '''
            SELECT s.sale_id, i.*, s.*
            FROM items AS i
            JOIN sales AS s ON i.item_id = s.item_id
            WHERE s.buyer_uid IS NULL
            ORDER BY RANDOM()\
            LIMIT 100;\
            '''
            print(query)
            cursor.execute(query)
            result = cursor.fetchall()
            #CHeck first if the record is present. Omit out the password from the tuple
            if not result:
                return make_response('User id was not found.', 404, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
            else:
                return jsonify(result)
            cursor.close()
        conn.close()


@app.route('/createoffer', methods=['PUT'])
def case7():
    validation_result = verify()
    if isinstance(validation_result, str):  
        return jsonify({"message": validation_result}), 401
    else:  
        #2 parts of the query. 1st get user id from the token. 2nd put the record in.
        with psycopg.connect(URL) as conn:
            cursor = conn.cursor()
            auth_header = request.headers.get('Authorization')
            parts = auth_header.split(' ')
            if len(parts) == 2 and parts[0] == 'Bearer':
                jwt_token = parts[1]
            payload = jwt.decode(jwt_token, app.config['SECRET_KEY'], algorithms=['HS256'])
            query = "SELECT uid FROM users WHERE email = '"+payload.get('email')+"'"
            cursor.execute(query)
            result1 = cursor.fetchall()
            sale_id = random_string(20)
            seller_uid = ''.join(result1[0])
            # item_id = random_string(10)
            item_id = random.choice(item_id_list)
            quantity = random.randint(1, 100)
            price_per_item = random.randint(1, 1000)
            price_total = price_per_item * quantity
            state = random_string(20)
            seller_description = random_string(50)
            batch = random.randint(1, 1000)
            query2 = f"""
            INSERT INTO sales VALUES (
            '{sale_id}',
            '{seller_uid}',
            NULL,
            '{item_id}',
            '{quantity}',
            '{price_per_item}',
            '{price_total}',
            '{state}',
            '{seller_description}',
            '{datetime.datetime.now()}',
            NULL,
            '{batch}') RETURNING *;
            """
            print(query2)
            cursor.execute(query2)
            result2 = cursor.fetchall()
            #CHeck first if the record is present. Omit out the password from the tuple
            if not result2:
                return make_response('User id was not found.', 404, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
            else:
                return jsonify(result2)
            cursor.close()
        conn.close()


@app.route('/buyofferbysaleid', methods=['PUT'])
def case8():
    validation_result = verify()
    if isinstance(validation_result, str): 
        return jsonify({"message": validation_result}), 401
    else:  
        with psycopg.connect(URL) as conn:
            print("Connected to DB")
            try:
                cursor = conn.cursor()
                sale_id = str(request.args.get('sale_id'))
                #check if sale_id exists
                query_1 = "SELECT EXISTS (SELECT 1 FROM sales WHERE sale_id = '"+sale_id+"');"
                cursor.execute(query_1)
                result = cursor.fetchall()
                result = result[0]
                print(result[0])
                if result[0]:
                    #get offers by self
                    auth_header = request.headers.get('Authorization')
                    parts = auth_header.split(' ')
                    if len(parts) == 2 and parts[0] == 'Bearer':
                        jwt_token = parts[1]
                    payload = jwt.decode(jwt_token, app.config['SECRET_KEY'], algorithms=['HS256'])
                    query_to_get_uid = "SELECT uid FROM users WHERE email = '"+payload.get('email')+"'"
                    cursor.execute(query_to_get_uid)
                    result_to_get_uid = cursor.fetchall()
                    seller_uid = ''.join(result_to_get_uid[0])
                    #get the buyer id of the given sale_id 
                    query_get_buyer_id = (f"SELECT seller_uid FROM sales WHERE sale_id = '{sale_id}';")
                    print(query_get_buyer_id)
                    cursor.execute(query_get_buyer_id)
                    buyer_uid = cursor.fetchone()[0]
                    if seller_uid == buyer_uid:
                        cursor.close()
                        conn.close()
                        return make_response('Unauthorized', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
                    else:
                        #Update 2  values in the sales record
                        buyer_uid = seller_uid
                        date_sold = datetime.datetime.utcnow()
                        cursor.execute(f'''UPDATE sales 
                        SET buyer_uid = '{buyer_uid}', date_sold = '{date_sold}' 
                        WHERE sale_id = '{sale_id}';
                        ''')
                        #Update sales record in items table by incrementing it by 1 
                        cursor.execute(f'''
                        UPDATE items 
                        SET sales = sales + 1 
                        WHERE item_id = (SELECT item_id FROM sales WHERE sale_id = '{sale_id}');
                        ''')
                        # Update the sales, sales_sum, and balance attributes of the seller user record
                        cursor.execute(f'''
                        UPDATE users 
                        SET sales = sales + 1, 
                            sales_sum = sales_sum + (SELECT price_per_item FROM sales WHERE sale_id = '{sale_id}'), 
                            balance = balance + (SELECT price_per_item FROM sales WHERE sale_id = '{sale_id}') 
                        WHERE uid = '{seller_uid}';
                        ''')
                        # Update the purchases, purchases_sum, and balance attributes of the buyer user record
                        cursor.execute(f'''
                        UPDATE users 
                        SET purchases = purchases + 1, 
                            purchases_sum = purchases_sum + (SELECT price_per_item FROM sales WHERE sale_id = '{sale_id}'), 
                            balance = balance - (SELECT price_per_item FROM sales WHERE sale_id = '{sale_id}') 
                        WHERE uid = '{buyer_uid}';
                        ''')
                        conn.commit()
                        cursor.close()
                        conn.close()
                        return jsonify(result)
                else:
                    cursor.close()
                    conn.close()
                    return make_response('Unknown sale id', 404, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
            except psycopg3.DatabaseError as error:
                # If an error occurs, roll back the transaction
                if conn:
                    conn.rollback()
                    print("Error:", error)            
            cursor.close()
        conn.close()


#Check if sale ID exists. Unknown sale id. Check if its authorized. Then delete it.
@app.route('/deleteofferbysaleid', methods=['DELETE'])
def case9():
    validation_result = verify()
    if isinstance(validation_result, str):  
        return jsonify({"message": validation_result}), 401
    else:  
        with psycopg.connect(URL) as conn:
            print("Connected to DB")
            cursor = conn.cursor()
            sale_id = str(request.args.get('sale_id'))
            #check if sale_id exists
            query_1 = "SELECT EXISTS (SELECT 1 FROM sales WHERE sale_id = '"+sale_id+"');"
            cursor.execute(query_1)
            result = cursor.fetchall()
            result = result[0]
            print(result[0])
            if result[0]:
                #get offers by self
                auth_header = request.headers.get('Authorization')
                parts = auth_header.split(' ')
                if len(parts) == 2 and parts[0] == 'Bearer':
                    jwt_token = parts[1]
                payload = jwt.decode(jwt_token, app.config['SECRET_KEY'], algorithms=['HS256'])
                query_to_get_uid = "SELECT uid FROM users WHERE email = '"+payload.get('email')+"'"
                cursor.execute(query_to_get_uid)
                result_to_get_uid = cursor.fetchall()
                seller_uid = ''.join(result_to_get_uid[0])
                # final_query = "SELECT * FROM sales WHERE buyer_uid IS NULL AND sale_id = '"+sale_id+"' AND seller_uid = '"+seller_uid+"';"
                final_query = "DELETE FROM sales WHERE buyer_uid IS NULL AND sale_id = '"+sale_id+"' AND seller_uid = '"+seller_uid+"';"
                print(final_query)
                cursor.execute(final_query)
                conn.commit()
                result = cursor.rowcount
                #CHeck first if the record is present. Omit out the password from the tuple
                if not result:
                    return make_response('Unauthorized', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
                else:
                    return jsonify(result)
            else:
                return make_response('Unknown sale id', 404, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
            cursor.close()
        conn.close()


@app.route('/getownuserid', methods=['GET'])
def case10():
    validation_result = verify()
    if isinstance(validation_result, str):  
        return jsonify({"message": validation_result}), 401
    else:  
        #2 parts of the query. 1st get user id from the token. 2nd put the record in.
        with psycopg.connect(URL) as conn:
            print("Case 10")
            cursor = conn.cursor()
            auth_header = request.headers.get('Authorization')
            parts = auth_header.split(' ')
            if len(parts) == 2 and parts[0] == 'Bearer':
                jwt_token = parts[1]
            payload = jwt.decode(jwt_token, app.config['SECRET_KEY'], algorithms=['HS256'])
            query = "SELECT uid FROM users WHERE email = '"+payload.get('email')+"'"
            cursor.execute(query)
            result = cursor.fetchall()
            uid = ''.join(result[0])
            if not result:
                return make_response('User id was not found.', 404, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
            else:
                return jsonify(uid=uid)
            cursor.close()
        conn.close()


@app.route('/getbalancesum', methods=['GET'])
def case11():
    with psycopg.connect(URL) as conn:
        print("Connected to DB")
        cursor = conn.cursor()
        query = '''
        SELECT SUM(balance) AS total_balance
        FROM users;
        '''
        cursor.execute(query)
        result = cursor.fetchone()
        balanceSum = int(result[0])
        print(f" val : {balanceSum}")
        if not result:
            return make_response('Balance was not found.', 404, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
        else:
            return jsonify(balanceSum=balanceSum)
        cursor.close()
    conn.close()            

@app.route('/get1row', methods=['GET'])
def case12():
    with psycopg.connect(URL) as conn:
        print("Connected to DB")
        cursor = conn.cursor()
        query = '''
        SELECT email, password FROM users ORDER BY RANDOM() LIMIT 1;
        '''
        cursor.execute(query)
        result = cursor.fetchone()
        if not result:
            return make_response('Balance was not found.', 404, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
        else:
            return jsonify(email=result[0], password=result[1])
        cursor.close()
    conn.close()            

# GET /api/sales?user_id=1&item_title=&seller_description=best&manufacturer_description=popular
def returnRecords(mode):
    if mode == "sales":
        uid_string = "sell"
    elif mode == "purchases":
        uid_string = "buy"
    user_id = request.args.get('user_id')
    item_title = request.args.get('item_title')
    manufacturer_description = request.args.get('manufacturer_description')
    seller_description = request.args.get('seller_description')
    filter_string = ""
    if not item_title and not seller_description and not manufacturer_description:
        filter_string = ""
    else:
        filter_string += " AND ("
        if item_title: 
            filter_string += "i.title LIKE '%"+item_title+"%' "
        if seller_description: 
            filter_string += "AND s.seller_description LIKE '%"+seller_description+"%' "
        if manufacturer_description: 
            filter_string += "AND i.manufacturer_description LIKE '%"+manufacturer_description+"%'"
        filter_string += ") "
    query = '''
    SELECT s.'''+uid_string+'''er_uid, s.seller_description, i.item_id, i.manufacturer_description, i.title, s.date_offered
    FROM sales s
    JOIN items i ON s.item_id = i.item_id
    WHERE s.'''+uid_string+'''er_uid = \''''+user_id+'''\' '''+filter_string+'''  
    ORDER BY s.date_offered DESC;
    '''
    print(f"{query}")
    return query

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
