#Code developed and maintained by Abhay Maurya

#Some important modules to import 

import os
import time
from datetime import datetime
from win10toast import ToastNotifier    #for toast notifications
from zipfile import ZipFile
from tkinter import filedialog      #for file browse dialog box
from tkinter import *       #for gui
import ctypes           #for windows message box 

#Some UDFs
#Index Generator generates index of all the files in the directory

def Index_generator(path):
    files = []
    subdirs = []
    index = {}  #Index Dictionary

    #Populating Files, Subdirs

    for root, dirs, filenames in os.walk(path):
        for subdir in dirs:
            subdirs.append(os.path.relpath(os.path.join(root, subdir), path))

        for f in filenames:
            files.append(os.path.relpath(os.path.join(root, f), path))

    for f in files:
        index[f] = os.path.getmtime(os.path.join(path, files[0]))

    return dict(files=files, subdirs=subdirs, index=index)

#This UDF computes difference between two different indexes

def compute_diff(dir_base, dir_cmp):
    data = {}
    data['deleted'] = list(set(dir_cmp['files']) - set(dir_base['files']))
    data['created'] = list(set(dir_base['files']) - set(dir_cmp['files']))
    data['updated'] = []
    data['deleted_dirs'] = list(set(dir_cmp['subdirs']) - set(dir_base['subdirs']))

    for f in set(dir_cmp['files']).intersection(set(dir_base['files'])):
        if dir_base['index'][f] != dir_cmp['index'][f]:
            data['updated'].append(f)

    return data

#Main Data Type Dictionary

fileTypes = {}
fileTypes["Images"] = ["jpg", "gif", "png", "jpeg", "bmp", "dmg"]
fileTypes["Audio"] = ["mp3", "wav", "wma", "aiff", "flac", "aac", "xspf", "mid"]
fileTypes["Video"] = ["m4v", "3gp", "flv", "mpeg", "mov", "mpg", "mpe", "wmv", "MOV", "mp4", "mkv", "m2ts", "sfl"]
fileTypes["Documents and Spreadsheets"] = ["accdb", "_xls", "mdb", "one","doc", "docx", "xls", "xlsx", "csi", "csv", "txt", "ppt", "pptx", "pdf", "rtf"]
fileTypes["Programs"] = ["py", "whl", "pyc", "pyproject", "cpp", "c", "m", "o", "h"]
fileTypes["Executables"] = ["exe"]
fileTypes["Installer"] = ["msi"]
fileTypes["Java Exe"] = ["jar" , "air"]
fileTypes["APK Files"] = ["apk"]
fileTypes["Flash Files"] = ["fla", "swf"]
fileTypes["LOG Files"] = ["log"]
fileTypes["Photoshop Documents"] = ["psd"]
fileTypes["Dap Downloads"] = ["dap"]
fileTypes["SFVIDCAP Files"] = ["sfvidcap"]
fileTypes["Torrent"] = ["torrent"]
fileTypes["Compressed"] = ["zip", "tar", "7z", "rar", "bz2", "gz"]
fileTypes["ISO Files"] = ["vmdk", "ova", "iso"]
fileTypes["Chrome Extensions"] = ["crx"]
fileTypes["SFK Files"] = ["sfk"]
fileTypes["VEP Files"] = ["vep"]
fileTypes["BAK Files"] = ["bak"]
fileTypes["MDI Files"] = ["mdi"]
fileTypes["ASD Files"] = ["asd"]
fileTypes["VEG Files"] = ["veg"]
fileTypes["SFAP0 Files"] = ["sfap0"]
fileTypes["Fritzing Files"] = ["fzz"]
fileTypes["Registry Files"] = ["reg"]
fileTypes["DO Files"] = ["do"]
fileTypes["AHK Files"] = ["ahk"]
fileTypes["V-REP Files"] = ["ttt", "ttm"]
fileTypes["ORIG Files"] = ["orig"]
fileTypes["VMWare Files"] = ["ova"]
fileTypes["ARIA2 Files"] = ["aria2"]
fileTypes["Shortcuts"] = ["lnk"]
fileTypes["FL Studio Projects"] = ["flp"]
fileTypes["Web Codes"] = ["htm", "html", "css", "js", "php", "xml"]

#Searching for Cookie.txt file

try:
    cookies = open("Cookie.txt","r")
except:
    cookies = open("Cookie.txt","w")
    cookies.write("False\n")
    cookies.close()
    cookies = open("Cookie.txt","r")

#Reading Cookie.txt

cookie=cookies.readlines()
cookie_path=os.path.abspath("Cookie.txt")
iconpath=(cookie_path.split("Cookie.txt"))[0]+"EasiIcon.ico"
if cookie[0]=="False\n":
    root = Tk()
    root.title("Easi")
    root.iconbitmap(iconpath)
    try:
        Label(root, text="Do you want pop-up notifications?").grid(row=0, sticky=W, padx=6, pady=6)
        v = IntVar()
        v.set(1)
        def quit_loop():
            global notification
            notification = v.get()
            if notification==1:
                notification=True
            else:
                notification=False
            root.quit()
        Radiobutton(root, text="Yes", variable=v, value=1).grid(row=1, sticky=W)
        Radiobutton(root, text="No", variable=v, value=2).grid(row=2, sticky=W)
        Button(root, text='Next', command=quit_loop).grid(row=3, sticky=W, pady=4, padx=4)
        mainloop()
        root.withdraw()
    except:
        ctypes.windll.user32.MessageBoxW(0, "No Value Selected!", "Easi", 0)
        raise SystemExit("Cancelling: No Value Selected!")
    folder_selected = filedialog.askdirectory()
    fname = folder_selected
    if not fname:
        cookies.close()
        os.remove("Cookie.txt")
        ctypes.windll.user32.MessageBoxW(0, "No Directory Supplied!", "Easi", 0)
        raise SystemExit("Cancelling: No Directory supplied")
    else:
        path = str(fname)
        cookies.close()
        os.remove("Cookie.txt")
        cookies = open("Cookie.txt","w")
        cookies.writelines(["True\n",path,"\n"+str(notification)])
        cookies.close()
elif cookie[0]=="True\n":
    path = str(cookie[1])
    notification=bool(cookie[2])
    cookies.close()

#Service Started

if notification:
    toaster = ToastNotifier()
    toaster.show_toast("Easi","Service Started",threaded=True,icon_path=iconpath,duration=None)

#Main While Loop

while True:

    #Check for current time and date

    dt = datetime.today()

    #Generate two indexes to compare
    a=Index_generator(path)
    time.sleep(1)
    b=Index_generator(path)

    #Computing Difference

    data=compute_diff(b,a)

    #Analysing Data

    #If any file is deleted
    if data['deleted']!=[]:
        if len(data['deleted'])==1:
            if notification:
                toaster.show_toast("Easi",str(len(data['deleted']))+" file deleted.",threaded=True,icon_path=iconpath,duration=None)
        else:
            if notification:
                toaster.show_toast("Easi",str(len(data['deleted']))+" files deleted.",threaded=True,icon_path=iconpath,duration=None)
    if data['created']!=[]:
        #print("Created file : ",data['created'])
        for file in data['created']:
            if "." in file and "\\" not in file:
                ext=(file.split("."))[-1]
                #print(ext)
                for filetype in fileTypes.keys():
                    if ext in fileTypes[filetype]:
                        if ext=="crdownload":
                            if notification:
                                toaster.show_toast("Easi","Download Started",threaded=True,icon_path=iconpath,duration=None)
                        elif ext=="zip":
                            file2=path+"/"+str(file)
                            print("file2 : "+file2)
                            try:
                                with ZipFile(file2, 'r') as zip:
                                    zip.printdir() 
                                    print('Extracting all the files now...') 
                                    zip.extractall(path=path) 
                                    print('Done!') 
                                os.remove(file2)
                            except:
                                print('Zip can\'t be extracted.')
                                # try:
                                #     path2=path+"/"+str(filetype)
                                #     path3=path+"/"+str(filetype)+"/"+str(file)
                                #     path4=path+"/"+str(filetype)+"/(New"+str(dt.second)+str(dt.microsecond)+")"+str(file)
                                #     print("path2 : "+path2)
                                #     os.mkdir(path2)
                                # except OSError:
                                #     #print ("Creation of the directory %s failed" % path2)
                                #     pass
                                # file2=path+"/"+str(file)
                                # try:
                                #     print("file2 : "+file2)
                                #     print("path3 : "+path3)
                                #     os.rename(file2, path3)
                                #     #print("Created file : ",path3)
                                #     toaster.show_toast("Easi","File Downloaded : "+file,threaded=True,icon_path=iconpath,duration=None)
                                # except OSError:
                                #     #print("Created file : ",file2)
                                #     os.rename(file2, path4)
                        else:
                            try:
                                path2=path+"/"+str(filetype)
                                path3=path+"/"+str(filetype)+"/"+str(file)
                                path4=path+"/"+str(filetype)+"/(New"+str(dt.second)+str(dt.microsecond)+")"+str(file)
                                print("path2 : "+path2)
                                os.mkdir(path2)
                            except OSError:
                                #print ("Creation of the directory %s failed" % path2)
                                pass
                            file2=path+"/"+str(file)
                            try:
                                print("file2 : "+file2)
                                print("path3 : "+path3)
                                os.rename(file2, path3)
                                if notification:
                                    toaster.show_toast("Easi","File Downloaded : "+file,threaded=True,icon_path=iconpath,duration=None)
                            except OSError:
                                #print("Created file : ",file2)
                                os.rename(file2, path4)
    if data['updated']!=[]:
        #print("Updated file : ",data['updated'])
        #print("Created file : ",data['created'])
        for file in data['updated']:
            if "." in file and "\\" not in file:
                ext=(file.split("."))[-1]
                #print(ext)
                for filetype in fileTypes.keys():
                    if ext in fileTypes[filetype]:
                        if ext=="crdownload":
                            #print("Detected Downloading")
                            pass
                        elif ext=="zip":
                            file2=path+"/"+str(file)
                            print("file2 : "+file2)
                            try:
                                with ZipFile(file2, 'r') as zip:
                                    zip.printdir() 
                                    print('Extracting all the files now...') 
                                    zip.extractall(path=path) 
                                    print('Done!') 
                                os.remove(file2)
                            except:
                                print('Zip can\'t be extracted.')
                                # try:
                                #     path2=path+"/"+str(filetype)
                                #     path3=path+"/"+str(filetype)+"/"+str(file)
                                #     path4=path+"/"+str(filetype)+"/(New"+str(dt.second)+str(dt.microsecond)+")"+str(file)
                                #     print("path2 : "+path2)
                                #     os.mkdir(path2)
                                # except OSError:
                                #     #print ("Creation of the directory %s failed" % path2)
                                #     pass
                                # file2=path+"/"+str(file)
                                # try:
                                #     print("file2 : "+file2)
                                #     print("path3 : "+path3)
                                #     os.rename(file2, path3)
                                #     #print("Created file : ",path3)
                                #     toaster.show_toast("Easi","File Downloaded : "+file,threaded=True,icon_path=iconpath,duration=None)
                                # except OSError:
                                #     #print("Created file : ",file2)
                                #     os.rename(file2, path4)
                        else:
                            try:
                                path2=path+"/"+str(filetype)
                                path3=path+"/"+str(filetype)+"/"+str(file)
                                path4=path+"/"+str(filetype)+"/(New"+str(dt.second)+str(dt.microsecond)+")"+str(file)
                                print("path2 : "+path2)
                                os.mkdir(path2)
                            except OSError:
                                #print ("Creation of the directory %s failed" % path2)
                                pass
                            file2=path+"/"+str(file)
                            try:
                                print("file2 : "+file2)
                                print("path3 : "+path3)
                                os.rename(file2, path3)
                                if notification:
                                    toaster.show_toast("Easi","File Downloaded : "+file,threaded=True,icon_path=iconpath,duration=None)
                            except OSError:
                                #print("Created file : ",file2)
                                os.rename(file2, path4)
    if data['deleted_dirs']!=[]:
        #print("Deleted Directory : ",data['deleted_dirs'])
        if len(data['deleted_dirs'])==1:
            if notification:
                toaster.show_toast("Easi",str(len(data['deleted_dirs']))+" folder deleted.",threaded=True,icon_path=iconpath,duration=None)
        else:
            if notification:
                toaster.show_toast("Easi",str(len(data['deleted_dirs']))+" folders deleted.",threaded=True,icon_path=iconpath,duration=None)
