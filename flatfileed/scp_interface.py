from flask import Flask, render_template, request, redirect, url_for, Blueprint
from flask import current_app as app
import csv
import datetime
import glob
import paramiko
from scp import SCPClient



from pathlib import Path

bp = Blueprint('scp_interface', __name__)

@bp.route('/test_scp_connection')
def test_connection():
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    try:
        t = paramiko.Transport(app.config['SCP_HOST'], app.config['SCP_PORT'])
        t.connect(username=app.config['SCP_LOGIN'],password=app.config['SCP_PASSWORD'])
    except paramiko.SSHException:
        app.logger.Error('Test connection failed!')
        return 'Connection Error'
    
    try:
        sftp = paramiko.SFTPClient.from_transport(t)
        success = sftp.listdir(app.config['SCP_DIR'])
        if(success is not None):
            app.logger.info('Test connection passed!')
            return "Success"
        else:
            app.logger.Error('Test connection failed! Directory empty')
            return 'Directory empty'
    except FileNotFoundError:
        app.logger.Error('Test connection failed! Wrong directory')
        return 'Wrong directory'

@bp.route('/download_file', methods=['GET','POST'])
def download_file():
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    try:
        t = paramiko.Transport(app.config['SCP_HOST'], app.config['SCP_PORT'])
        t.connect(username=app.config['SCP_LOGIN'],password=app.config['SCP_PASSWORD'])
    except paramiko.SSHException:
        app.logger.Error('Download file - Test connection failed!')
        return 'Connection Error'

    try:
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(app.config['SCP_DIR'] + '/' + app.config['SCP_CSV_NAME'],app.config['CSV_NAME'])
    except paramiko.SSHException:
        app.logger.Error('Download file error! Wrong Configuration of directory')
        return 'Error'
    finally:
        sftp.close()
        t.close() 
    app.logger.info('Flat File successfully downloaded')
    return "File downloaded"
    

@bp.route('/upload_file', methods=['GET','POST'])
def upload_file():
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    try:
        t = paramiko.Transport(app.config['SCP_HOST'], app.config['SCP_PORT'])
        t.connect(username=app.config['SCP_LOGIN'],password=app.config['SCP_PASSWORD'])
    except paramiko.SSHException:
        app.logger.Error('Upload file - Test connection failed!')
        return 'Connection Error'
    try:
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(app.config['CSV_NAME'],app.config['SCP_DIR'] + '/' + app.config['SCP_CSV_NAME'])
    except paramiko.SSHException:
        app.logger.Error('Upload file error! Wrong Configuration of directory')
        return 'Error'
    finally:
        sftp.close()
        t.close()
    app.logger.info('Flat File successfully uploaded!')
    return "File uploaded"
    