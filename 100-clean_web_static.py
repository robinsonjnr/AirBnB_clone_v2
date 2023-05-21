#!/usr/bin/python3
""" deletes out-of-date archives"""

from fabric.api import *
from os import path
from datetime import datetime
from shlex import split

env.user = 'ubuntu'
env.hosts = ['34.74.70.205', '34.224.30.177']


def do_pack():
    """Packing a dir in .tgz"""
    print("Packing web_static to versions/web_static_20170314233357.tgz")
    if not path.exists('versions') or (
                                       path.exists('versions') and
                                       not path.isdir('versions')):
        local('mkdir -p versions')
    d_now = datetime.now()
    cmd_tar = 'tar -cvzf '
    p_name = 'versions/web_static_'
    p_name += '{:4}{:02}{:02}'.format(d_now.year, d_now.month, d_now.day)
    p_name += '{:02}{:02}{:02}'.format(d_now.hour, d_now.minute, d_now.second)
    p_name += '.tgz'
    cmd_tar += p_name
    cmd_tar += ' web_static'
    try:
        local(cmd_tar)
        return p_name
    except:
        return None


def do_deploy(archive_path):
    """Deplay the archive tgz"""
    if not path.exists(archive_path) or (
                                         path.exists(archive_path) and
                                         path.isdir(archive_path)):
        return False
    try:
        put(archive_path, '/tmp/')
        name_file_ext = archive_path.split("/")[1]
        name_file = name_file_ext.split(".")[0]
        cmd_mkdir = 'mkdir -p /data/web_static/releases/{}'.format(name_file)
        run(cmd_mkdir)
        cmd_uncom = 'tar -xzf /tmp/{}'.format(name_file_ext)
        cmd_uncom += ' -C /data/web_static/releases/{}'.format(name_file)
        run(cmd_uncom)
        cmd_rm_file = 'rm /tmp/{}'.format(name_file_ext)
        run(cmd_rm_file)
        cmd_mv = 'mv /data/web_static/releases/'
        cmd_mv += '{}/web_static/*'.format(name_file)
        cmd_mv += ' /data/web_static/releases/{}/'.format(name_file)
        run(cmd_mv)
        cmd_rm_dir = 'rm -rf /data/web_static/releases/{}'.format(name_file)
        cmd_rm_dir += '/web_static'
        run(cmd_rm_dir)
        run('rm -rf /data/web_static/current')
        cmd_cre_sym = 'ln -s /data/web_static/releases/{}/'.format(name_file)
        cmd_cre_sym += ' /data/web_static/current'
        run(cmd_cre_sym)
        print("New version deployed!")
        return True
    except:
        return False


def deploy():
    """creates and distributes an archive to your web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    check_ok = do_deploy(archive_path)
    return check_ok


def do_clean(number=0):
    """deletes out-of-date archives"""
    if number == '0':
        number = int(number) + 1
    else:
        number = int(number)

    cmd_clean_local = 'find versions -type f -name \'web*\'| sort -Vr | '
    cmd_clean_local += 'tail -n +{}'.format(number + 1)
    cmd_clean_local += ' | awk {print} | xargs rm'
    local(cmd_clean_local)

    cmd_clean_server = 'find /data/web_static/releases '
    cmd_clean_server += '-maxdepth 1 -type d -name \'web*\''
    cmd_clean_server += ' | sort -Vr | tail -n +{}'.format(number + 1)
    cmd_clean_server += ' | awk {print} | xargs rm -rf'
    run(cmd_clean_server)
