
from django.shortcuts import render
from django.contrib import messages
import json
import os
import requests  
from bs4 import BeautifulSoup
import datetime
import os
def checkedd():
        path = r"C:\Users\USER\Desktop\json\jumia.json"
        if os.path.exists(path):
            mnt =  datetime.date.today()
            f_date = mnt.strftime("%Y-%m-%d")
            
            creation_time = os.path.getctime(path)


            creation_date = datetime.datetime.fromtimestamp(creation_time)


            strstnig = creation_date.strftime('%Y-%m-%d')


            if strstnig != f_date:
                
                 os.remove(path)


def ajt(ch):
    ch1=''
    x=str(ch)
    ch1=x[0:(len(x)-2)]
    return int(ch1)
      
def strn(ch):
    s=''
    for i in range(len(ch)):
        if ch[i] in ['0','1','2','3','4','5','6','7','8','9'] :
            s=s+ch[i]
    return int(s)

def main():
      
      liste=[]
      x=True
      s=0
      while x :
            page=requests.get(f'https://www.jumia.com.tn/mlp-telephone-tablette/smartphones/?page={s}#catalog-listing')
            src=page.content
            soup=BeautifulSoup(src, "lxml")
            phone=soup.find_all('article',{'class':'prd _fb col c-prd'})
            if phone:
                  s=s+1
                  for i in range (len(phone)):
                        dicvalue={}
                        x0=phone[i].contents[0].get('data-brand')
                        
                            
                        dicvalue['nom']=x0
                                
                        x1=phone[i].contents[0].get('data-name')
                        dicvalue['info']=x1
                                
                        x=phone[i].find('div',{'class':'img-c'})
                        dicvalue['photo']=x.contents[0].get('data-src')
                                
                        y=phone[i].find('div',{'class':'prc'})

                        dicvalue['prixnv']=ajt(strn(y.string))
                        lien=phone[i].contents[0].get('href')
                        dicvalue['lien']='https://www.jumia.com.tn'+lien
                        m=phone[i].find('div',{'class':'old'})
                        if m:
                                    
                                    dicvalue['prixold']=m.string
                                
                        m1=phone[i].find('div',{'class':'bdg _dsct _sm'})
                        if m1:
                                
                                dicvalue['remise']=m1.string
                        m3=phone[i].find('div',{'class':'bdg _oos _xs'})
                        if m3 :
                                    
                                    dicvalue['disponiblite']=m3.contents[1]
                        m4=phone[i].find('div',{'class':'stars _s'})
                        if m4:
                                    
                                    dicvalue['stars']=m4.contents[0]
                            
                        liste.append(dicvalue)
            
    

            else:
                  break 
      return liste
                  
        
            
def ver(ch):
    
    for i in range(len(ch)):
        if ch[i] not  in ['0','1','2','3','4','5','6','7','8','9'] :
            return False
    return True
   
def remplir(filename):
    
    x=main()
    with open(filename, 'w') as file:
    
      json.dump(x, file)



def existee ():
   filename = r"C:\Users\USER\Desktop\json\jumia.json"
   if os.path.exists(filename):
    
    return filename
   else:
    remplir(filename)
    return filename
   

   
def liste_tel():
    ls=[]
    fil=existee()
    with open(fil,'r') as f:
           data=json.load(f)
           for i in range(len(data)):
            
             if data[i]['nom'] in ls :
                continue
             else:
                
                ls.append(data[i]['nom'])
    return ls
          
            
    



def home(request):
   
    
    dicf = []
    
    if request.method=='POST':
        
        x=request.POST['d']
        y=request.POST['t2']
        y1=request.POST['t3']
        
        fil=existee()
        with open(fil,'r') as f:
           data=json.load(f)
    
       
        if x and ver(y) and ver(y1):
            x1 = data
            
            for i in x1:
                
                if i['nom'].lower()==x.lower() and i['prixnv'] >= int(y) and i['prixnv'] <= int(y1) :
                    dicfi = {}
                    dicfi['nom'] = i['nom']
                    dicfi['info'] = i['info']
                    dicfi['photo'] = i['photo']
                    dicfi['prixnv'] = i['prixnv']
                    dicfi['lien'] = i['lien']
                    if 'prixold' in i:
                     dicfi['prixold'] = i['prixold']
                    if 'remise' in i :
                     dicfi['remise'] = i['remise']
                    if 'disponiblite' in i :
                     dicfi['disponiblite'] = i['disponiblite']
                    if 'stars' in i :
                     dicfi['stars'] = i['stars']
                    dicf.append(dicfi)
            if len(dicf) !=0 :
             return render(request,'home.html',{'a':dicf ,'d':'selected','c':y ,'d':y1,'lst':liste_tel()})
            else :
               messages.info(request,"pas de telphone avec cette prix ")
        else:
            messages.info(request,"verfier votre prix ")

       
        
       

    return render(request,'home.html',{'lst':liste_tel()})
    


                     
                          

        
            
    
        
    


    
