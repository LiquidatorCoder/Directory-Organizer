import os
import time
from datetime import datetime
from win10toast import ToastNotifier
from zipfile import ZipFile
import PySimpleGUI as sg

try:
    cookies = open("Cookie.txt","r")
except:
    cookies = open("Cookie.txt","w")
    cookies.write("False\n")
    cookies.close()
    cookies = open("Cookie.txt","r")

cookie=cookies.readlines()
if cookie[0]=="False\n":
    fname = sg.popup_get_folder('Directory to open')
    if not fname:
        sg.popup("Cancel", "No Directory supplied")
        raise SystemExit("Cancelling: no Directory supplied")
    else:
        path = str(fname)
        cookies.close()
        os.remove("Cookie.txt")
        cookies = open("Cookie.txt","w")
        cookies.writelines(["True\n",path])
        cookies.close()
elif cookie[0]=="True\n":
    path = str(cookie[1])
    cookies.close()




toaster = ToastNotifier()
toaster.show_toast("Easi","Service Started",threaded=True,icon_path=iconpath,duration=None)

def Index_generator(path):
    files = []
    subdirs = []
    index = {}

    #print(next(os.walk(path)))

    for root, dirs, filenames in os.walk(path):
        for subdir in dirs:
            subdirs.append(os.path.relpath(os.path.join(root, subdir), path))

        for f in filenames:
            files.append(os.path.relpath(os.path.join(root, f), path))

    for f in files:
        index[f] = os.path.getmtime(os.path.join(path, files[0]))

    return dict(files=files, subdirs=subdirs, index=index)

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

fileTypes = {}
fileTypes["Images"] = ["jpg", "gif", "png", "jpeg", "bmp", "dmg"]
fileTypes["Audio"] = ["mp3", "wav", "wma", "aiff", "flac", "aac", "xspf", "mid"]
fileTypes["Video"] = ["m4v", "3gp", "flv", "mpeg", "mov", "mpg", "mpe", "wmv", \
                          "MOV", "mp4", "mkv", "m2ts", "sfl"]
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
#fileTypes["Chrome Downloads"] = ["crdownload"]
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

#a=Index_generator(path)
#file_mtime = os.path.getmtime(os.path.join(path, files[0]))
#print(datetime.fromtimestamp(file_mtime),files[0])
#b=Index_generator(path)
while True:
    dt = datetime.today()
    a=Index_generator(path)
    time.sleep(1)
    b=Index_generator(path)
    data=compute_diff(b,a)
    if data['deleted']!=[]:
        #print("Deleted file : ",data['deleted'])
        if len(data['deleted'])==1:
            #print(len(data['deleted']),"file deleted.")
            toaster.show_toast("Easi",str(len(data['deleted']))+" file deleted.",threaded=True,icon_path=iconpath,duration=None)
        else:
            #print(len(data['deleted']),"files deleted.")
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
                            #print("Detected Downloading")
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
                                #print("Created file : ",path3)
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
                                #print("Created file : ",path3)
                                toaster.show_toast("Easi","File Downloaded : "+file,threaded=True,icon_path=iconpath,duration=None)
                            except OSError:
                                #print("Created file : ",file2)
                                os.rename(file2, path4)
    if data['deleted_dirs']!=[]:
        #print("Deleted Directory : ",data['deleted_dirs'])
        if len(data['deleted_dirs'])==1:
            #print(len(data['deleted_dirs']),"folder deleted.")
            toaster.show_toast("Easi",str(len(data['deleted_dirs']))+" folder deleted.",threaded=True,icon_path=iconpath,duration=None)
        else:
            #print(len(data['deleted_dirs']),"folders deleted.")
            toaster.show_toast("Easi",str(len(data['deleted_dirs']))+" folders deleted.",threaded=True,icon_path=iconpath,duration=None)
