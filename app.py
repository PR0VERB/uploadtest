# https://www.youtube.com/watch?v=aruInGd-m40&t=278s
# https://www.youtube.com/watch?v=H8Ars15wGRM

import streamlit as st
import pandas as pd
import time
import datetime
import streamlit.components.v1 as components
# from PIL import Image

######################### Import UPLOADING Libraries ####################
# https://www.youtube.com/watch?v=fkWM7A-MxR0
import os
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload   


from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from src import (
    upload_files_to_gdrive,
    list_out_file_from_gdrive,
    download_files_from_gdrive,
    create_file_and_write_text_init,
    )
######################### Import UPLOADING Libraries ####################


# initialise stakeholder dataframe

stake_df= pd.read_excel('DATA/stakes_df.xlsx')
stake_addresses = list(stake_df['Email Address'])

# verify email
enter_email = st.text_input("Please enter your email address", value="")

if enter_email not in stake_addresses:
    st.write('It seems like your email address does not have access to this plaform. Please contact Bill - bseota@gmail.com')
else:
    st.write('Email verified')

    drive_directory_df = pd.read_excel('DATA/GoogleDriveIndicatorMetroFolderID.xlsx', sheet_name='main')
    # metro list
    metros = list(drive_directory_df.Metro.unique())
    metros.insert(0,'Make a Selection')
    # indicator list
    indicators = list(drive_directory_df.Indicator.unique())
    indicators.insert(0,'Make a Selection')

    metro_selected = st.selectbox("Select a metro", tuple(metros), key=1)
    if metro_selected != 'Make a Selection':
        indicator_selected = st.selectbox("Select an indicator", tuple(indicators), key = 2)
        if indicator_selected != 'Make a Selection':
            uploaded_file = st.file_uploader("Choose an xlsx or csv file")
            if uploaded_file is not None:
                def chosen_sheet(uploaded_file: str):
                    return pd.read_excel(uploaded_file,sheet_name = 'Sheet1')
                df_ = chosen_sheet(uploaded_file)
            print("UPLOADED FILE ##############################", uploaded_file)
            #assign the corresponding folder id
            folder_id = drive_directory_df[(drive_directory_df.Metro == metro_selected) & (drive_directory_df.Indicator == indicator_selected)].FolderID.values[0]

    # TODO: make file type agnostic


    #TODO Columns validation 

    # if uploaded_file is not None:
    #     df_ = chosen_sheet(uploaded_file)
    # metros = list(drive_directory_df.Metro.unique())
    # metros.insert(0,'Make a Selection')
    # # indicator list
    # indicators = list(drive_directory_df.Indicator.unique())
    # indicators.insert(0,'Make a Selection')

    # metro_selected = st.selectbox("Select a metro", tuple(metros), key = 3)
    # if metro_selected != 'Make a Selection':
    #     indicator_selected = st.selectbox("Select an indicator", tuple(indicators), key = 4)
    
    # uploaded_file = st.file_uploader("Choose an xlsx or csv file")
    # print("UPLOADED FILE ##############################", uploaded_file)

    # # TODO: make file type agnostic
    # def chosen_sheet(uploaded_file: str):
    #    return pd.read_excel(uploaded_file,sheet_name = 'Sheet1')

    # #TODO Columns validation 

    # if uploaded_file is not None:
    #     df_ = chosen_sheet(uploaded_file)
        
                                                            ######################### UPLOADING #########################

    SCOPES = ['https://www.googleapis.com/auth/drive'] # if we want to change the scope then we need to delete the current token and create a new one





    # creds = None
    # # retreive folder id of the appropriate metro & indicator
    #     # for some reason, the below works without the .FolderID.values[0] 
    # if os.path.exists("token.json"):
    #          #if the token exists 
    #     print("exist")
    #     creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # if not creds or not creds.valid:
    #     #in the case of creds not valid
    #     if creds and creds.expired and creds.refresh_token:
    #         creds.refresh(Request())
    #     else:
    #         # create app flow from credentials file 
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             "web_credentials.json", SCOPES)
    #         # run
            
    #         creds = flow.run_local_server(port=0)
            
    #     with open("token.json", "w") as token:
    #         token.write(creds.to_json())
    try:
        # service = build("drive", "v3", credentials = creds)
        #### temporary solution to upload since we are using google drive and not an actual database ####
        
        # 1. get the current working directory
        # file_dir = os.getcwd()
        file_dir = "DATA/"
        # 2. append current working directory to the file name
        # file_path = os.path.join(file_dir,uploaded_file.name)
        file_path = f"{file_dir}{uploaded_file.name}"
        # 3. take the dataframe to excel and save to file directory 
        df_.to_excel(file_path)
        del df_
        # 4. upload the file with name file_path to drive
        # file_metadata = {
        #     "name": uploaded_file.name,
        #     "parents": [folder_id]
        # }
        # print("FILE PATH IS " + file_path)
        # print("FILE type IS ", type(file_path))
        
        # print("folder PATH IS " + str(folder_id))
        # print("folder type IS ", type(folder_id))
        
        # media = MediaFileUpload(file_path)
        # print(type(media))
        # upload_file = service.files().create(
        #     body = file_metadata, fields = "id", media_body = media).execute()
        
        # media = MediaFileUpload(filename =  "G:/My Drive/GOOGLEDRIVE_CODE/CODE/STREAMLIT/UPLOADFOLDER/backupfiles/fe.txt") # , mimetype='application/vnd.ms-excel' , resumable=True
        # print(media)
        
        # upload_drive_file = service.files().create(body = file_metadata, fields = "id", media_body = media)
        # upload_drive_file.execute()
        
        print("Backed up file" + uploaded_file.name)
        
        ################pydrive########################
        gauth = GoogleAuth()           
        drive = GoogleDrive(gauth)
        # driveId = '1MVjVp-O-vIth4dynbOiPZ0AOFRQNYq22' #folderId og Google Drive you are working with
        # upload_file_list = ['samplefile1.txt', 'samplefile2.txt'] #List of file to be uploaded.


        upload_files_to_gdrive([file_path], drive, folder_id)#
        print("uploaded")
################pydrive########################
        
    except HttpError as e:
        print("Error:" + str(e))        
        # 5. delete file in cwd
        
        #### temporary solution to upload since we are using google drive and not an actual database ####
        
       
        

        


                                                        ######################### end UPLOADING #########################
