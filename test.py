from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials

# Before the premission for the folder that you are going to upload to need to be given on the user account.
# Upload function can than be ran. This program demostrates how to upload a file via a service account to a shared file space.

def upload(folderName,filename,mycread):
    # marking out the JSON file in the directory of the program. This is for the service account.
    JSON_FILE = "client_secrets.json"
    

    print(folderName)
    print(filename)


    # get authrisation
    gauth = GoogleAuth()
    scope = ["https://www.googleapis.com/auth/drive"]

    # if you don't have this file already, don't worry it will create one, this is what will stop the web browser login promote.
    gauth.LoadCredentialsFile(mycread)


    if gauth.credentials is None:

        # Authenticate if they're not there
        gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_FILE, scope)

    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
        
    else:
        #     Initialize the saved creds
        gauth.Authorize()

    # Save the current credentials to a file
    gauth.SaveCredentialsFile(mycread)

    # start driver instance
    drive = GoogleDrive(gauth)

    # get the list of folders in the service account, i.e. these are the directories that the user shared.
    folders = drive.ListFile(
        {'q': "title='" + folderName + "' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
    # search for the directory, this may upload to multiple locations if they have the same folder name.
    for folder in folders:
        if folder['title'] == folderName: 
            file1 = drive.CreateFile({'title': filename,'parents': [{'id': folder['id']}]})
            file1.SetContentString('So this text file would have been uploaded without asking you to sign-in or that you have a shared file!') # Set content of the file from given string.
            file1.Upload()

upload('catched','teste.txt',"mycreds.txt")


