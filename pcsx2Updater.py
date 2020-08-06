import requests
import os
import shutil

def overwrite_oldfiles():
    extracted_folder = ""
    for folder in os.listdir("."):
        if ("pcsx2-" in folder):
            extracted_folder = folder
            break
        
    os.system("xcopy /e /y " + extracted_folder + " .")

    os.system("RMDIR /Q/S " + extracted_folder)
    os.remove("latest.7z")

def download_html():
    html_request = requests.get("https://buildbot.orphis.net/pcsx2/index.php")
    open("index.html", "wb").write(html_request.content)
    return

def zip_extraction():
    command = '\"C:\Program Files\\7-Zip\\7z.exe\" x -y latest.7z'
    os.system(command)

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
        print("You're already on latest version!")
        return True
    else: return False


def main():

    print("Downloading the latest html from https://buildbot.orphis.net/pcsx2/index.php")
    download_html()
    print("index.html downloaded!")

    print("Parsing the latest built version")
    latest_version = latest_version_parser()
    
    if (already_latest(latest_version) == True): 
        os.system("pcsx2.exe")
        return

    print("Requesting {}".format(latest_version))
    new_request = requests.get("https://buildbot.orphis.net/pcsx2/index.php?m=dl&" + latest_version + "&platform=windows-x86")
    open('latest.7z', 'wb').write(new_request.content)
    print("latest.7z created!")
    os.remove("index.html")

    zip_extraction()

    overwrite_oldfiles()
   
    os.system("pcsx2.exe")
    
    return

main()