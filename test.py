payload = {'Provider': {0: 'unknown', 1: 'AIRTEL', 2: '#REF!', 3: 'RELIANCE', 4: 'VODAFONE', 5: 'TATA DOCOMO', 6: 'IDEA',
 7: 'UNINOR', 8: 'BSNL', 9: 'VIDEOCON TELECOM', 10: 'LOOP MOBILE', 11: 'MTS', 12: 'AIRCEL', 13: 'ETISALAT', 14:
 'STEL', 15: 'TATA INDICOM', 16: 'MTNL', 17: 'PING MOBILE (QUADRANT)'}, 'Frequency': {0: 2382, 1: 2237, 2: 1119
, 3: 941, 4: 749, 5: 681, 6: 626, 7: 329, 8: 236, 9: 158, 10: 132, 11: 132, 12: 128, 13: 79, 14: 43, 15: 19, 16
: 5, 17: 4}}


# print(payload['Provider'][0])

provider = {}
freq = {}
provider = payload['Provider']
freq = payload['Frequency']
ans = {}
# print("this is provider : ",provider)
# print("this is freq : ",freq)
for i in provider:
    # print("this is : ",i,"\n")
    valuep = provider[i]
    valuef = freq[i]
    
    # print("this is key =",i,"this is a provider value = ",valuep,"\n")

    # print("this is key =",i,"this is a frequency value = ",valuef,"\n")
    ans[valuep] = valuef
    
print("This is ans dict = ",ans)
@app.route("/showdata",methods=['GET','POST'])
def showdata():
    try:
        if(request.method == 'POST'):
        
            res = dataset()
            provider = {}
            freq = {}
            provider = res['Provider']
            freq = res['Frequency']
            ans = {}
            
            for i in provider:
               
                valuep = provider[i]
                valuef = freq[i]
                
               
                ans[valuep] = valuef
                
            print("This is ans dict = ",ans)
            return jsonify({"status":ans}) ,200
        elif request.method == 'GET':
            args = request.args
            args = args.to_dict()
            deliverRate = None
            if 'deliverRate' in args:
                
                deliverRate = args['deliverRate']
                res = dataset(True)
                deliverRate = res
            return jsonify({"deliveryRate":deliverRate})
                
                
        else:
            return jsonify({"status":"Invalid request"}), 400
        
    except Exception as e:
        print(e)
        return jsonify({"error":e})
    
    
    



 @app.route('/alldata',methods=['GET','POST'])
# def alldata():
#     try:
#         if request.method == 'GET':
#             r = dataset()
#             print(res)
#             return jsonify({"Analyse data":res})
#         else:
#             return jsonify({"status":False,"message":"Invalid request"})
            
#         pass
    
#     except Exception as e:
#         print(e)
#         return jsonify({'status':False})