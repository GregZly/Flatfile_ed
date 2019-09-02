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
        return 'Connection Error'
    
    try:
        sftp = paramiko.SFTPClient.from_transport(t)
        success = sftp.listdir(app.config['SCP_DIR'])
        if(success is not None):
            return "Success"
        else:
            return 'Directory empty'
    except FileNotFoundError:
        return 'Wrong directory'
    