import sys
import os
import paramiko

if len(sys.argv) < 3:
    print('Usage: python uploadSceneData.py path/to/privateKey path/to/data/folder')
    exit(1)

privateKeyPath = sys.argv[1]
dataFolderPath = sys.argv[2]

if not os.path.isdir(dataFolderPath):
    print(str(dataFolderPath) + ' is not a directory or does not exist')
    exit(1)

def runCmd(ssh, cmd):
    print('Running command: ' + cmd)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    print(ssh_stdout.read().decode("utf-8"))
    print(ssh_stderr.read().decode("utf-8"))

def chown(ssh, item):
    runCmd(ssh, 'sudo chown wordpress:www-data "' + item + '"')

def mkdir(sftp, path, mode=511):
    ''' Augments mkdir by adding an option to not fail if the folder exists  '''
    print('Creating directory ' + path)
    try:
        sftp.mkdir(path, mode)
        chown(ssh, path)
    except IOError:
        pass

def put_dir(sftp, ssh, source, target):
    ''' Uploads the contents of the source directory to the target path. The
        target directory needs to exists. All subdirectories in source are
        created under target.
    '''
    for item in os.listdir(source):
        sourceItem = os.path.join(source, item)
        targetItem = '%s/%s' % (target, item)
        if os.path.isfile(sourceItem):
            print('Uploading file ' + sourceItem + ' to ' + targetItem)
            sftp.put(sourceItem, targetItem)
            chown(ssh, targetItem)
        else:
            print('Uploading directory ' + sourceItem + ' to ' + targetItem)
            mkdir(sftp, targetItem)
            put_dir(sftp, ssh, sourceItem, targetItem)

def rm_dir(ssh, dir):
    runCmd(ssh, 'rm -rf ' + dir)

def mv_dir(sftp, source, target):
    print('Moving folder ' + source + ' to ' + target)
    sftp.rename(source, target)

key = paramiko.RSAKey.from_private_key_file(sys.argv[1])
ssh = paramiko.SSHClient()
try:
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='54.214.206.232', username='ubuntu', pkey=key)
    sftp = ssh.open_sftp()
    try:
        rootPath = '/webroot/keyshot/wordpress/startup/common/'
        uploadPath = rootPath + 'uploadInProgress'
        destinationPath = rootPath + 'scenes'
        rm_dir(ssh, uploadPath)
        mkdir(sftp, uploadPath)
        put_dir(sftp, ssh, dataFolderPath, uploadPath)
        rm_dir(ssh, destinationPath)
        mv_dir(sftp, uploadPath, destinationPath)
    finally:
        sftp.close()
finally:
    ssh.close()