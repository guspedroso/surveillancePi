import os

#change these variables as needed
sPiDir = "/home/pi/scripts/surveillancePi/"
path = sPiDir + "content/"
message = "The surveillance system has been triggered. "
message += "View the content here: https://www.dropbox.com/home/Apps/SurveilancePi"
reciever = "8175555555@vtext.com"

def prepare_files():
    if not os.path.exists(path):
        print path + ' does not exist'
        return
    os.chdir(path)
    print '---------------------------------------------------'
    os.system("echo '[ '`date`' ] Preparing the files'")
    cmd = 'COUNT=`ls -1 *.jpg 2>/dev/null | wc -l` ; '
    cmd += 'if [ "$COUNT" != 0 ]; then '
    cmd += 'echo "Creating tar ball of $COUNT jpgs.." ; '
    cmd += 'tar -cf pics_`date +%Y%m%d_%H%M%S`.tar *jpg ; '
    cmd += 'sudo rm *jpg ; '
    cmd += 'echo "Tar complete, current files:" ; '
    cmd += 'else echo "No jpgs to tar, current files:" ; fi ; ls ;'
    os.system(cmd)

def upload_files():
    if not os.path.exists(path):
        print path + ' does not exist'
        return
    dir_list = os.listdir(path)
    first_10 = dir_list[:10]
    amt = len(first_10)
    for file_name in first_10:
        file_full_path = path + file_name
        cmd = sPiDir + "Dropbox-Uploader/dropbox_uploader.sh upload " + file_full_path + " " + file_name
        os.system(cmd)
        os.remove(file_full_path)
    return amt

def send_text(amtIn):
    if amtIn > 0:
        print 'Sending text'
        cmd = 'echo "' + message + '" | mail -s "" "' + reciever + '"'
        os.system(cmd)
    else:
        print 'Not sending text'
    os.system("echo '[ '`date`' ] Finished'")

if __name__ == "__main__":
    prepare_files()
    amt = upload_files()
    send_text(amt)
