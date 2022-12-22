from sciflow.localsettings import *
from substances.models import *
from datafiles.models import *
import paramiko


def remotelogin():
    """ remote login to the scidata.unf.edu server"""
    ip = rserverip
    u = rserveruser
    p = rserverpass
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=u, password=p)
    return client


def uploadfile(lpath, rpath, subid=0):
    """
    this function uploads a file to a remote server using paramiko
    users are advised to store server authentication (and other data as appropriate)
    in a localsettings file that does not get store on any code hosting service
    """
    client = remotelogin()

    if lpath == 'https://sds.coas.unf.edu/sciflow/files/facet/' and subid == 0:
        return False
    elif lpath == 'https://sds.coas.unf.edu/sciflow/files/facet/':
        sub = Substances.objects.values('facet_lookup_id', 'inchikey').get(id=subid)
        # use curl
        flid = str(sub['facet_lookup_id'])
        cmd = "curl -o " + rpath + " " + lpath + flid + '/down'
        _stdin, _stdout, _stderr = client.exec_command(cmd)
        print(_stdout.read().decode())
        print(cmd)
    else:
        # upload local file
        print("complete my code!")

    client.close()
    return


def getremotetwins():
    """
    this function uploads a file to a remote server using paramiko
    users are advised to store server authentication (and other data as appropriate)
    in a localsettings file that does not get store on any code hosting service
    """
    client = remotelogin()
    cmd = "ls -al /var/uploads/tranche/chalklab/chemtwin/"
    _stdin, _stdout, _stderr = client.exec_command(cmd)
    print(_stdout.read().decode())
    client.close()
    twins = []
    for line in _stdout:
        print(line)
        exit()
    return twins

