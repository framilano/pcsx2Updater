import requests
import os

def overwrite_oldfiles():
    extracted_folder = ""
    for folder in os.listdir("."):
        if ("pcsx2-" in folder):
            extracted_folder = folder
            break
        
    os.system("xcopy /e /y " + extracted_folder + " .")
    os.system("rmdir /q /s " + extracted_folder)
    os.system("del /q /s latest.7z")
    return

def download_html():
    html_request = requests.get("https://buildbot.orphis.net/pcsx2/index.php")
    open("index.html", "wb").write(html_request.content)
    return

def latest_version_parser():
    html_parser = open("index.html")
    latest_link = ""
    for line in html_parser.readlines():
        line = line.lower()
        if ("rev=" in line): 
            latest_link = line
            break
    html_parser.close()
    return latest_link.split(";")[1].replace("&amp", "")

def already_latest(latest_version):
    try:
        search = open("version.txt", "r")
    except (FileNotFoundError):
        print("version.txt not found, creating it")
        search = open("version.txt", "w")
        search.write(latest_version)
        return False
    actual_version = search.readlines()
    if (actual_version[0] == latest_version):
        print("You're already using the latest version!")
        return True
    else: 
        search = open("version.txt", "w")
        search.write(latest_version)
        return False

def download_latest_zip(latest_version):
    print("Requesting {}".format(latest_version))
    new_request = requests.get("https://buildbot.orphis.net/pcsx2/index.php?m=dl&" + latest_version + "&platform=windows-x86")
    open('latest.7z', 'wb').write(new_request.content)
    print("latest.7z created!")
    os.system("del /q /s index.html")

def main():
    print("Downloading the latest .html from https://buildbot.orphis.net/pcsx2/index.php")
    download_html()
    print("index.html downloaded!")

    print("Parsing the latest built version")
    latest_version = latest_version_parser()
    
    #Check if we're already running the latest pcsx2 version
    if (already_latest(latest_version) == True): 
        os.remove("index.html")
        os.popen("pcsx2.exe")
        return

    #Download and write in latest.7z the latest version content
    download_latest_zip(latest_version)

    #Extract the downloaded archive in the current folder
    os.system('\"C:\Program Files\\7-Zip\\7z.exe\" x -y latest.7z')

    #Merges downloaded files with the old ones, eventually deletes the extract folder and latest.7z
    overwrite_oldfiles()
   
   #Launch pcsx2 emulator without cmd as a subprocess
    os.popen("pcsx2.exe")
    
    return

main()
