import argparse
from time import sleep
from smb_tunnel import do_smb
from winrm_tunnel import do_winrm
from requests.exceptions import ConnectionError
from winrm.exceptions import WinRMOperationTimeoutError
from smb.base import NotConnectedError
from smb.smb_structs import OperationFailure
import atexit
import socket
import signal
import sys



# python SSH
from sshtunnel import SSHTunnelForwarder

server = None  # type: SSHTunnelForwarder


def killserver():
    global server
    if server:
        server.stop()

def signal_handler(sig, frame):                                                                                                                                                                                  
  print ('Ctrl-C detected - exciting')                                                                                                                                                                           
  killserver()                                                                                                                                                                                                   
  sys.exit(0)                                                                                                                                                                                                    
                 
signal.signal(signal.SIGINT, signal_handler)
atexit.register(killserver)


def main():
    global server
    parser = argparse.ArgumentParser()

    parser.add_argument("target", help="Target Windows Host")
    parser.add_argument("bastion", help="Bastion host IP")
    parser.add_argument('-u', '--ssh_username', help="SSH target username", default="ubuntu")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--ssh_password', help="SSH target password")
    group.add_argument('-k', '--ssh_key', help="SSH Private Key")
    parser.add_argument("username", help="Windows Username")
    parser.add_argument("password", help="Windows Password")
    parser.add_argument('-w', "--wait", action="store_true", help="Wait for connection to open before executing command", required=False)

    subparsers = parser.add_subparsers(help='exec or upload', dest="module")
    winrm_parser = subparsers.add_parser("exec", help="WinRM PowerShell Command")
    smb_parser = subparsers.add_parser("upload", help="SMB File Transfer")

    winrm_parser.add_argument("command", help="PowerShell Command to Execute")
    smb_parser.add_argument("local", help="Local file to copy")
    smb_parser.add_argument("remote", help="Remote file to create")
    smb_parser.add_argument("-s", "--share", help="Share to transfer to.", default="C$")

    args = parser.parse_args()

    # shared arguments
    windows_host = args.target
    jumphost = args.bastion
    ssh_username = args.ssh_username
    windows_user = args.username
    windows_password = args.password

    local_file_name = None
    remote_file_name = None
    rport = None
    winrm_cmd = None

    # module specific arguments
    if args.module == "exec":
        winrm_cmd = args.command
        rport = 5985
    if args.module == "upload":
        local_file_name = args.local
        remote_file_name = args.remote
        share = args.share
        rport = 445

    # start SSH tunnel
    if args.ssh_key:
        private_key = args.ssh_key
        server = SSHTunnelForwarder(
            jumphost,
            ssh_username=ssh_username,
            ssh_pkey=private_key,
            remote_bind_address=(windows_host, rport),
        )
    else:
        password = args.ssh_password
        server = SSHTunnelForwarder(
            jumphost,
            ssh_username=ssh_username,
            ssh_password=password,
            remote_bind_address=(windows_host, rport),
        )

    server.start()
    lport = server.local_bind_port

    # run the module
    if args.module == "exec":
      if args.wait:
        o = False
        while not o:
          try:
            do_winrm(lport, windows_user, windows_password, winrm_cmd)
          except (WinRMOperationTimeoutError, ConnectionError) as e:
            sleep(2)
            continue
          o = True
    if args.module == "upload":
      if args.wait:
        o = False
        while not o:
          try:
            do_smb(lport, windows_user, windows_password, local_file_name, remote_file_name, share)
          except (OperationFailure, NotConnectedError) as e:
            sleep(2)
            continue
          o = True


    killserver()
