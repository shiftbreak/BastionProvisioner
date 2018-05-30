#!/usr/bin/python


from winrm.protocol import Protocol


# required: sudo apt install libffi6 libffi-dev python-winrm


def do_winrm(lport, windows_user, windows_password, winrm_cmd):
    # if used with Terraform, there is an issue with backslashes so use the #BACKSLASH# placeholder instead
    winrm_cmd = winrm_cmd.replace("#BACKSLASH#", "\\\\")
    p = Protocol(
        endpoint='http://127.0.0.1:' + str(lport) + '/wsman',
        transport='basic',
        message_encryption='never',
        username=windows_user,
        password=windows_password,
        server_cert_validation='ignore')

    shell_id = p.open_shell()
    command_id = p.run_command(shell_id, 'powershell.exe', [winrm_cmd])
    cmd_output = p.get_command_output(shell_id, command_id)
    for l in cmd_output:
        print (str(l).replace("\r\n", "\n"))
    p.cleanup_command(shell_id, command_id)
    p.close_shell(shell_id)
