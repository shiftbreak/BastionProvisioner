from smb.SMBConnection import SMBConnection

import os


def do_smb(lport, windows_user, windows_password, local_file_name, remote_file_name, share="C$"):
    if os.path.exists(local_file_name):
        print "Uploading (from, to): " + local_file_name + ", " + remote_file_name

        conn = SMBConnection(windows_user, windows_password, "localhost", "localhost", use_ntlm_v2=True, is_direct_tcp=True)
        assert conn.connect("127.0.0.1", lport)

        f = open(local_file_name)
        conn.storeFile(share, remote_file_name, f)

        print "Uploaded"

    else:
        print "Local file does not exist: " + local_file_name


