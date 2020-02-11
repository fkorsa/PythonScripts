import sys
import os
import boto3

if len(sys.argv) < 4:
    print('Usage: python uploadSceneData.py path/to/data/folder key_id key_secret')
    exit(1)

class Uploader:
    def __init__(self, dataFolderPath, keyId, keySecret):
        self.dataFolderPath = dataFolderPath
        self.keyId = keyId
        self.keySecret = keySecret
        self.jsonFileName = 'scenes.json'
        self.rootKey = 'startup/scenes/'
        self.dataFolderName = 'data'
        self.jsonFileKey = self.rootKey + self.jsonFileName
        self.dataKey = self.rootKey + self.dataFolderName + '/'
        self.inputDataFolderPath = os.path.join(dataFolderPath, self.dataFolderName)
        self.inputJsonFilePath = os.path.join(dataFolderPath, self.jsonFileName)
        self.bucketName = 'media.keyshot.com'
        self.region = 'us-west-2'

    def checkFolders(self):
        if not os.path.isdir(self.dataFolderPath):
            print(str(self.dataFolderPath) + ' is not a directory or does not exist')
            exit(1)

        if not os.path.isdir(self.inputDataFolderPath):
            print(str(self.inputDataFolderPath) + ' is not a directory or does not exist')
            exit(1)

        if not os.path.isfile(self.inputJsonFilePath):
            print(str(self.inputJsonFilePath) + ' is not a file or does not exist')
            exit(1)

    def initS3(self):
        session = boto3.session.Session(aws_access_key_id=self.keyId, aws_secret_access_key=self.keySecret,
                                        region_name = self.region)
        self.s3 = session.resource('s3', self.region)
        self.bucket = self.s3.Bucket(self.bucketName)

    def deletePrevious(self):
        print('Deleting previous data...')
        self.bucket.objects.filter(Prefix=self.rootKey).delete()

    def bytesTransferred(self, numberOfBytes):
        self.currentDownloadedBytes += numberOfBytes
        print('\rProgress: ' + str(int(self.currentDownloadedBytes / self.currentFileSize * 100)) + '%', end='')

    def uploadFile(self, filePath):
        uploadKey = self.rootKey + os.path.relpath(filePath, self.dataFolderPath)
        uploadKey = uploadKey.replace('\\', '/')
        print('Uploading ' + os.path.basename(filePath) + '...')
        self.currentFileSize = os.path.getsize(filePath)
        self.currentDownloadedBytes = 0
        self.bucket.upload_file(filePath, uploadKey, ExtraArgs={'ACL': 'public-read'}, Callback=self.bytesTransferred)
        print('\n')

    def uploadData(self):
        for dirname, _, filenames in os.walk(self.inputDataFolderPath):
            for filename in filenames:
                filePath = os.path.join(dirname, filename)
                self.uploadFile(filePath)

    def uploadMetadata(self):
        self.uploadFile(self.inputJsonFilePath)

    def upload(self):
        self.checkFolders()
        self.initS3()
        self.deletePrevious()
        self.uploadData()
        self.uploadMetadata()

uploader = Uploader(dataFolderPath=sys.argv[1], keyId=sys.argv[2], keySecret=sys.argv[3])
uploader.upload()
