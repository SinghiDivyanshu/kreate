import time 
import requests
import operator
import re
import json
import sys
import re
import gui_main
# import pymsql


# Import library to display results
#import matplotlib.pyplot as plt
#from matplotlib.lines import Line2D

_url = 'https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/RecognizeText'
# _url = 'https://eastasia.api.cognitive.microsoft.com/vision/v2.0/recognizeText'
_key = None  #Here you have to paste your primary key
_maxNumRetries = 10



# def my_mysql();
#     con = pymysql.connect('localhost', 'root', 
#         'root', 'moneyOnClick')

#     with con:

#         cur = con.cursor()
#         cur.execute("insert into aadhar (1,'singhi', '2000-05-20',8156121,'xyz qwerty')")

#         version = cur.fetchone()
#         print ("done")




def processRequest( json, data, headers, params ):

    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """
    data_list=[]
    retries = 0
    result = None
    print ("hell!!!!")
    while True:
        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )
        if response.status_code == 429:
            print( "Message: %s" % ( response.json() ) )
            if retries <= _maxNumRetries: 
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break
        elif response.status_code == 202:
            result = response.headers['Operation-Location']
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json() ) )
        break
        
    return result

def getOCRTextResult( operationLocation, headers ):
    """
    Helper function to get text result from operation location

    Parameters:
    operationLocation: operationLocation to get text result, See API Documentation
    headers: Used to pass the key information
    """

    retries = 0
    result = None

    while True:
        response = requests.request('get', operationLocation, json=None, data=None, headers=headers, params=None)
        if response.status_code == 429:
            print("Message: %s" % (response.json()))
            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print('Error: failed after retrying!')
                break
        elif response.status_code == 200:
            result = response.json()
        else:
            print("Error code: %d" % (response.status_code))
            print("Message: %s" % (response.json()))
        break
    
    return result


    
front_image_aadhar = ""
rear_image_aadhar=""
# front_image_aadhar = "/home/divyanshu/Documents/StarLord_Workspace/kreate_hacathon/uploads/aadhar_singhi_aadhar_front.jpeg"
# rear_image_aadhar="/home/divyanshu/Documents/StarLord_Workspace/kreate_hacathon/uploads/aadhar_singh_aadhar_back.jpeg"


    

# def get_aadhar_data(front_image_aadhar,rear_image_aadhar):
#     front_data_dic=get_aadhar_front(front_image_aadhar)
#     rear_data_dic=get_aadhar_back(rear_image_aadhar)
#     print(front_data_dic)
#     print (rear_data_dic)

def get_aadhar_front(front_image_aadhar):
    front_data_dic={}
    if len(front_image_aadhar) == 0:
        return front_data_dic
    front_data_list=doc_text_data(front_image_aadhar)
    front_data_list=[x.lower() for x in front_data_list]
    for i in range(len(front_data_list)):
        mo = re.search(r"\d{2}[-/]\d{2}[-/]\d{4}$",str(front_data_list[i]))
        if mo:
            front_data_dic.update({"dob":mo.group()})
            front_data_dic.update({"name":front_data_list[i-1]})
        if(str(front_data_list[i]).find("male")!=-1):
            front_data_dic.update({"gender":"male"})
        elif(str(front_data_list[i]).find("female")!=-1):
            front_data_dic.update({"gender":"female"})
        elif(str(front_data_list[i]).find("transgender")!=-1):
            front_data_dic.update({"gender":"transgender"})
        match_found = re.search(r"^\d{4}\s\d{4}\s\d{4}$",str(front_data_list[i]))
        if match_found:
            front_data_dic.update({"aadhar_num":match_found.group()})    
            return front_data_dic        


def get_aadhar_back(pathToFileInDisk):
    if len(pathToFileInDisk) == 0:
        return {}
    data_list=[]  
    aadhar_num=0  
    with open(pathToFileInDisk, 'rb') as f:
        data = f.read()
    # Computer Vision parameters
    params = {'mode' : 'Handwritten'}
    _key = "6ad9a2d49a30474b8f0cdba889866003"
    full_address=""
    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _key
    headers['Content-Type'] = 'application/octet-stream'

    json = None
    operationLocation = processRequest(json, data, headers, params)

    _key = "6ad9a2d49a30474b8f0cdba889866003"
    result = None
    data_list=[]
    if (operationLocation != None):
        headers = {}
        headers['Ocp-Apim-Subscription-Key'] = _key
        while True:
            time.sleep(1)
            result = getOCRTextResult(operationLocation, headers)
            for i in range(len(result["recognitionResult"]["lines"])):
                mo = re.search(r"^\d{4}\s\d{4}\s\d{4}$",str(result["recognitionResult"]["lines"][i]["text"]))
                if mo:
                    aadhar_num=result["recognitionResult"]["lines"][i]["text"]
                    start=(result["recognitionResult"]["lines"][i]["boundingBox"][2])
                    end=(result["recognitionResult"]["lines"][i]["boundingBox"][0])
                    mid=((end-start)/2)+start
                    end_reading=result["recognitionResult"]["lines"][i]["boundingBox"][5]

            address_list=[]
            for i in range(len(result["recognitionResult"]["lines"])):
                if(result["recognitionResult"]["lines"][i]["boundingBox"][0]>mid and result["recognitionResult"]["lines"][i]["boundingBox"][3]<end_reading):
                    address_list.append(result["recognitionResult"]["lines"][i]["text"])   
            for i in range(len(address_list)):
                if(str(address_list[i].lower()).find("address")!=-1):
                    address_list[i]=address_list[i].replace('Address:','')
            full_address=' '.join(map(str, address_list))
            full_address = full_address.replace(',','-')
            full_address = full_address.replace("'","")
            return {"address":full_address,"aadhar_num":aadhar_num}                     
            if result['status'] == 'Succeeded' or result['status'] == 'Failed':
                break


def doc_text_data(pathToFileInDisk):
    data_list=[]    
    with open(pathToFileInDisk, 'rb') as f:
        data = f.read()

    # Computer Vision parameters
    params = {'mode' : 'Handwritten'}
    _key = "6ad9a2d49a30474b8f0cdba889866003"

    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _key
    headers['Content-Type'] = 'application/octet-stream'

    json = None
    operationLocation = processRequest(json, data, headers, params)

    _key = "6ad9a2d49a30474b8f0cdba889866003"
    result = None
    data_list=[]
    if (operationLocation != None):
        headers = {}
        headers['Ocp-Apim-Subscription-Key'] = _key
        while True:
            time.sleep(1)
            result = getOCRTextResult(operationLocation, headers)
            for i in range(len(result["recognitionResult"]["lines"])):
                data_list.append((result["recognitionResult"]["lines"][i]["text"]))
                
            return data_list
            if result['status'] == 'Succeeded' or result['status'] == 'Failed':
                break


# get_aadhar_data(front_image_aadhar,rear_image_aadhar)
# Load raw image file into memory
local_path = "/home/divyanshu/Documents/StarLord_Workspace/kreate_hacathon/"

# my_mysql()
def ocr_capture():
    images = ["singh_aadhar_back.jpeg","singhi_aadhar_front.jpeg"]
    for image in images:
        if image.find('aadhar_front') != -1:
            front_image_aadhar = "/home/divyanshu/Documents/StarLord_Workspace/kreate_hacathon/"+ image
            front_data_dic=get_aadhar_front(front_image_aadhar)
            print(front_data_dic)
        if image.find('aadhar_back') != -1:
            back_image_aadhar = "/home/divyanshu/Documents/StarLord_Workspace/kreate_hacathon/" +image    
            rear_data_dic=get_aadhar_back(back_image_aadhar)
            rear_data_dic.update({front_data_dic})
    return (rear_data_dic)

# test = {"add":"123","gender":"male"}
# print (test)
# sys.stdout(test)


def ocr_pan_capture():
    pan_image=local_path  + 'singh_pan.jpeg'
    pan_list=doc_text_data(pan_image)
    pan_dic={}
    pan_list=[x.lower() for x in pan_list]
    for i in range(len(pan_list)):
        pan_list[i]=pan_list[i].encode('ascii','ignore')
    
    for i in range(len(pan_list)):    
        match_f = re.search(r"[a-z]{5}[0-9]{4}[a-z]{1}",str(pan_list[i]))
        if match_f:
            pan_dic.update({"pan_number":match_f.group()})
        if (str(pan_list[i]).find("father's name")>-1):
            pan_dic.update({"name":pan_list[i-1]})
            pan_dic.update({"father name":pan_list[i+1]})
        mo = re.search(r"\d{2}[-/]\d{2}[-/]\d{4}$",str(pan_list[i]))
        if mo:
            pan_dic.update({"dob":mo.group()})    
    print(pan_dic)
    return pan_dic



voter_id_front_img=local_path+'singhi_voterid_front.jpeg'
voter_id_rear_img=local_path+'singh_vote_bridack.jpeg'

def ocr_voter_capture():
    voter_id_dic_front=get_voter_id_data_front(voter_id_front_img)
    voter_id_dic_rear=get_voter_id_data_rear(voter_id_rear_img)
    voter_id_dic_front.update({voter_id_dic_rear})
    print(voter_id_dic_rear)
    return (voter_id_dic_front)
    
def get_voter_id_data_rear(voter_id_rear):
    voter_id_list1=doc_text_data(voter_id_rear)
    voter_id_list=[x.lower() for x in voter_id_list1] 
    voter_id_dic1={} 
    # print(voter_id_list)
    ct=0
    address_list_2=[] 
    address_cnt=0
    for i in range(len(voter_id_list)):
        voter_id_list[i]=voter_id_list[i].encode('ascii','ignore')
    for i in range(len(voter_id_list)):
        
        match = re.findall(r"[\d]{2}-[\d]{2}-[\d]{4}",str(voter_id_list[i]))
        if match:
            voter_id_dic1.update({"DOB":match})       
        if (((str(voter_id_list[i]).find("address")!=(-1) and address_cnt==0) or ct==1) and not(re.search(r"\d{2}[/]\d{2}[/]\d{4}$",str(voter_id_list[i])))):
            ct=1 
            address_cnt=1
            address_list_2.append(voter_id_list[i])  
        if (re.findall(r"[\d]{2}/[\d]{2}/[\d]{4}",str(voter_id_list[i]))):
            ct=0
            
        if (str(voter_id_list[i]).find("male")!=(-1)):
            voter_id_dic1.update({"sex":"male"})
        elif (str(voter_id_list[i]).find("female")!=(-1)):
            voter_id_dic1.update({"sex":"female"})
    for i in range(len(address_list_2)):
        if(str(address_list_2[i]).find("address")!=-1):
            address_list_2[i]=str(address_list_2[i]).replace('address :','')          
    voter_id_dic1.update({"address":address_list_2})
    return voter_id_dic1         

def get_voter_id_data_front(voter_id_front):
    voter_id_list=doc_text_data(voter_id_front)
    voter_id_list=[x.lower() for x in voter_id_list]
    voter_id_dic={}
    ct=0
    address_list_2=[]
    for i in range(len(voter_id_list)):
        voter_id_list[i]=voter_id_list[i].encode('ascii','ignore')
    for i in range(len(voter_id_list)):
        mo = re.search(r"^\d{2}[-/]\d{2}[-/]\d{4}$",str(voter_id_list[i]))
        if mo:
            voter_id_dic.update({"dob":mo.group()})   
        match_f = re.search(r"[a-z]{3}[' ']?[0-9]{7}",str(voter_id_list[i]))
        if match_f:
            voter_id_dic.update({"voter_id_num":match_f.group()})
        if (str(voter_id_list[i]).find("male")!=(-1)):
            voter_id_dic.update({"sex":"male"})
        elif (str(voter_id_list[i]).find("female")!=(-1)):
            voter_id_dic.update({"sex":"female"})
        if (str(voter_id_list[i]).find("name")!=(-1) and str(voter_id_list[i]).find("father's name")==-1):
            voter_id_dic.update({"name":voter_id_list[i][str(voter_id_list[i]).find(":")+1:]})
        elif(str(voter_id_list[i]).find("father's name")!=-1):
            voter_id_dic.update({"father_name":voter_id_list[i][str(voter_id_list[i]).find(":")+1:]})
        print(address_list_2)     
       
    return (voter_id_dic)