import tkinter
from PIL import *
from tkinter import *
import test2
import adhaar_ocr
import mycommand
import multiprocessing 
# Function to set focus (cursor) 
import pymysql

def dbConnection():
    return pymysql.connect('localhost', 'root', 
    'root', 'moneyOnClick')
def insert_DB_cust(name,Fnam,address):
    con = dbConnection()
    with con:
        
        cur = con.cursor()
        mySql_insert_query = """INSERT INTO customerDetail (name, Fname, address) 
                                VALUES (%s, %s, %s) """

        recordTuple = (name,Fname, address)
        cur.execute(mySql_insert_query, recordTuple)
        con.commit()
        rows = cur.fetchall()

    
def insert_DB_adhaar(name,aadhaar_number,address,gender):
    con = dbConnection()
    with con:
        
        cur = con.cursor()
        mySql_insert_query = """INSERT INTO aadhar (name, aadhaar_number, address,gender) 
                                VALUES (%s, %s, %s, %s) """

        recordTuple = (name,aadhaar_number, address,gender)
        cur.execute(mySql_insert_query, recordTuple)
        con.commit()
        rows = cur.fetchall()

def focus1(event): 
    # set focus on the course_field box 
    course_field.focus_set() 
  
  
# Function to set focus 
def focus2(event): 
    # set focus on the sem_field box 
    sem_field.focus_set() 
  
  
# Function to set focus 
def focus3(event): 
    # set focus on the form_no_field box 
    form_no_field.focus_set() 
  
  
# Function to set focus 
def focus4(event): 
    # set focus on the contact_no_field box 
    contact_no_field.focus_set() 
  
  
# Function to set focus 
def focus5(event): 
    # set focus on the email_id_field box 
    email_id_field.focus_set() 
  
  
# Function to set focus 
def focus6(event): 
    # set focus on the address_field box 
    address_field.focus_set() 


    


class Skeleton:
    def __init__(self,root =None):        
        self.root = root
        self.root.title("Horamavu Coders...")
        self.create_panel()
        dbConnection()
        self.call_ocr_aadhar
        self.aadhardata = []
        self.aadharLabel = []
        # set the background colour of GUI window 
        self.root.configure(background='light green')     

    def create_panel(self):
        # name_label = Label(self.Root_Frame,text="Enter Name").place(x=205,y=305)
        # name_field = Text(self.root,width=8, height=2)
        
        # name_field.place(x=245, y=330)
        # dob_label = Label(self.Root_Frame,text="Enter DOB").place(x=205,y=325)
        # address_label = Label(self.Root_Frame,text="Enter DOB").place(x=205,y=345)
        
  
    # set the configuration of GUI window 
    # root.geometry("500x300") 
        
        # create a Form label 
        self.name = Label(self.root, text="Name:", bg="light green") 
    
        # create a Name label 
        self.Fname = Label(self.root, text="Fathers Name:", bg="light green") 
    
        # create a Course label 
        self.Add = Label(self.root, text="Address:", bg="light green") 
    
        # create a Semester label 
        self.DOB = Label(self.root, text="dateOfBirth:", bg="light green")
        self.docNumber =  Label(self.root, text="DocNumber:", bg="light green")
        self.gender = Label(self.root, text="Gender:", bg="light green") 
     
        # in table like structure . 
        self.name.place(x=15, y=30) 
        self.Fname.place(x=15, y=50) 
        self.Add.place(x=15, y=70) 
        self.DOB.place(x=15, y=90) 
        self.gender.place(x=15, y=110) 
        self.docNumber.place(x=15,y=130)
        self.submit_btn = Button(self.root,text="Addhar Data",command=self.call_ocr_aadhar).place(x=20,y = 150)
        self.submit_btn = Button(self.root,text="Pan Data",command=self.call_ocr_pan).place(x=90,y = 150)
        self.submit_btn = Button(self.root,text="voterID Data",command=self.call_ocr_voter).place(x=800,y = 150)
        self.submit_btn = Button(self.root,text="Compare",command=self.compare).place(x=1000,y = 350)
        # # create a text entry box 
        # # for typing the information 
        
        # self.FName_field = Entry(self.root) 
        # self.DOB = Entry(self.root) 
        # self.address_field = Entry(self.root) 
        # contact_no_field = Entry(self.root) 
        # email_id_field = Entry(self.root) 
        # address_field = Entry(self.root) 
    
        # # bind method of widget is used for 
        # # the binding the function with the events 
    
        # # whenever the enter key is pressed 
        # # then call the focus1 function 
        # self.name_field.bind("<Return>", focus1) 
    
        # # whenever the enter key is pressed 
        # # then call the focus2 function 
        # self.FName_field.bind("<Return>", focus2) 
    
        # # whenever the enter key is pressed 
        # # then call the focus3 function 
        # sem_field.bind("<Return>", focus3) 
    
        # # whenever the enter key is pressed 
        # # then call the focus4 function 
        # form_no_field.bind("<Return>", focus4) 
    
        # # whenever the enter key is pressed 
        # # then call the focus5 function 
        # contact_no_field.bind("<Return>", focus5) 
    
        # # whenever the enter key is pressed 
        # # then call the focus6 function 
        # email_id_field.bind("<Return>", focus6) 
    
        # # grid method is used for placing 
        # # the widgets at respective positions 
        # # in table like structure . 
        # self.name_field.place(x=600, y=50) 
        # self.FName_field.place(x=600, y=70) 
        # self.DOB_field.place(x=600, y=90) 
        # self.Address.place(x=600, y=110) 
        # self.contact_no_field.place(x=600, y=130) 
        # email_id_field.place(x=600, y=150) 
        # address_field.place(x=600, y=170) 

    #     self.submit_btn = Button(self.root,text="submit",command=self.form_submit).place(x=700,y = 200)


    # def form_submit(self):
    #     formDataJson = {
    #         "name":"",
    #         "Fname":"",
    #         "DOB":"",



    #     }
    #     self.name_field.get()

    def call_ocr_aadhar(self):
        # p1 = multiprocessing.Process(target=self.caller, args=(10, )) 
        front_data_dic, back_data_dic = adhaar_ocr.ocr_capture()
        self.x_aadhar = 110
        self.y = [ 30,50,70,90,110,130]
        self.aadhardata = front_data_dic
        self.BackaadharData = back_data_dic
        
        self.aadharLabel.append(Label(self.root, text=self.aadhardata["name"]))
        self.aadharLabel.append(Label(self.root, text="NA"))
        self.aadharLabel.append(Label(self.root, text=self.BackaadharData["address"]))
        self.aadharLabel.append(Label(self.root, text=self.aadhardata["dob"]))
        self.aadharLabel.append(Label(self.root, text=self.aadhardata["gender"]))
        self.aadharLabel.append(Label(self.root, text=self.aadhardata["aadhar_num"]))

        # insert_DB_cust(self.aadhardata["name"], "xyz", self.BackaadharData["address"])
        insert_DB_adhaar(self.aadhardata["name"], self.aadhardata["aadhar_num"],self.BackaadharData["address"],self.aadhardata["gender"])
        
        # if self.aadhardata["aadhar_num"] == self.BackaadharData['aadhar_num']:

        
        for i in range(6): 
            self.aadharLabel[i].place(x=self.x_aadhar,y=self.y[i])


    def call_ocr_pan(self):
        self.pan_dic = adhaar_ocr.ocr_pan_capture()
    

    def call_ocr_voter(self):
        self.front_voter_dic, self.rear_voter_dic = adhaar_ocr.ocr_voter_capture()
        self.compare()
        
    def compare(self):
        
        compare_N_Score= 0
        compare_P_Score= 0
        pan_value = ""
        voter_val = ""
        aadhar_val = "" 
        print("compare...")
        
        
        aadhar=get_aadhar_data(front_image_aadhar,rear_image_aadhar)
        paan=get_pan_data(pan_image)
        voter=get_voter_id_data(voter_id_front_img,voter_id_rear_img)
        name_list_aadhar=aadhar["name"].split()
        name_list_pan=paan["name"].split()
        name_list_voter=voter["name"].split()
        aadhar_len=len(name_list_aadhar)
        ct=0

        up=max(len(name_list_aadhar),len(name_list_pan))
        for i in name_list_aadhar:
                for j in name_list_pan:
                        if(i==j):
                                ct=ct+1
        percent1=(ct/up)*100
        name_join_a="".join(map(str, name_list_aadhar))  
        name_join_p="".join(map(str, name_list_pan))
        name_join_v="".join(map(str, name_list_voter))
        print(name_join_a,name_join_p,name_join_v)
        ct2=0
        if(name_join_a!=name_join_p):
            print("aadha and pan name not matching")
            ct2=ct2+1
        if(name_join_p!=name_join_v):
            print("pan and voter id doesnt match")
            ct2=ct2+1
        if(ct2==0):
            print("Name in proper format")       

        if(ct2==1):
            print("66%")
        if(ct==2):
            print("pan,aadhar,voter id all have differenet names")

            
        
    #   def caller(self):
        
if __name__ == "__main__":
    
    window = tkinter.Tk()
    Skeleton(window)
    window.mainloop()

