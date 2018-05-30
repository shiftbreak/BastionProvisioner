import argparse
from smb_tunnel import do_smb
from winrm_tunnel import do_winrm
import atexit

# python SSH
from sshtunnel import SSHTunnelForwarder

server = None  # type: SSHTunnelForwarder


def killserver():
    global server
    if server:
        server.stop()


atexit.register(killserver)


def main():
    global server
    parser = argparse.ArgumentParser()
    parser.add_argument("key", help="SSH Private Key")
    parser.add_argument("target", help="Target Windows Host")
    parser.add_argument("bastion", help="Bastion host IP")
    parser.add_argument("username", help="Windows Username")
    parser.add_argument("password", help="Windows Password")

    subparsers = parser.add_subparsers(help='SMB or WinRM', dest="module")
    winrm_parser = subparsers.add_parser("winrm", help="WinRM PowerShell Command")
    smb_parser = subparsers.add_parser("smb", help="SMB File Transfer")

    winrm_parser.add_argument("command", help="PowerShell Command to Execute")
    smb_parser.add_argument("local", help="Local file to copy")
    smb_parser.add_argument("remote", help="Remote file to create")
    smb_parser.add_argument("-s", "--share", help="Share to transfer to.", default="C$")

    args = parser.parse_args()

    # shared arguments
    private_key = args.key
    windows_host = args.target
    jumphost = args.bastion
    windows_user = args.username
    windows_password = args.password

    local_file_name = None
    remote_file_name = None
    rport = None
    winrm_cmd = None

    # module specific arguments
    if args.module == "winrm":
        winrm_cmd = args.command
        rport = 5985
    if args.module == "smb":
        local_file_name = args.local
        remote_file_name = args.remote
        share = args.share
        rport = 445

    # start SSH tunnel
    server = SSHTunnelForwarder(
        jumphost,
        ssh_username="ubuntu",
        ssh_pkey=private_key,
        remote_bind_address=(windows_host, rport),
    )

    server.start()
    lport = server.local_bind_port

    # run the module
    if args.module == "winrm":
        do_winrm(lport, windows_user, windows_password, winrm_cmd)
    if args.module == "smb":
        do_smb(lport, windows_user, windows_password, local_file_name, remote_file_name, share)


    killserver()