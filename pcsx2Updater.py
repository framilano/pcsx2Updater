import requests
import os

def overwrite_oldfiles():
    extracted_folder = ""
    for folder in os.listdir("."):
        if ("pcsx2-" in folder):
            extracted_folder = folder
            break
    for files in os.listdir(extracted_folder):
        os.system("move /y " + extracted_folder + "\\" + files + " .")

    os.rmdir(extracted_folder)
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

def main():
    print("Downloading the latest html from https://buildbot.orphis.net/pcsx2/index.php")
    download_html()
    print("index.html downloaded!")

    print("Parsing the latest built version")
    latest_version = latest_version_parser()

    print("Requesting {}".format(latest_version))
    new_request = requests.get("https://buildbot.orphis.net/pcsx2/index.php?m=dl&" + latest_version + "&platform=windows-x86")
    open('latest.7z', 'wb').write(new_request.content)
    print("latest.7z created!")
    os.remove("index.html")

    zip_extraction()

    overwrite_oldfiles()
   
    
    return

main()