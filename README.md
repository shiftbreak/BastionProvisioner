# BastionProvisioner
A Python project to provision WinRM and SMB via an SSH tunnel

## Installation
To install from pip
> pip install wintunnel

# Usage
Wintunnel supports two modes - exec and upload. Upload uses SMB and exec uses WinRM
```
usage: wintunnel [-h] [-u SSH_USERNAME] (-p SSH_PASSWORD | -k SSH_KEY) [-w]                                                                                                                                      
                 target bastion username password {exec,upload} ...                                                                                                                                              
                                                                                                                                                                                                                 
positional arguments:                                                                                                                                                                                            
  target                Target Windows Host                                                                                                                                                                      
  bastion               Bastion host IP                                                                                                                                                                          
  username              Windows Username                                                                                                                                                                         
  password              Windows Password                                                                                                                                                                         
  {exec,upload}         exec or upload                                                                                                                                                                           
    exec                WinRM PowerShell Command                                                                                                                                                                 
    upload              SMB File Transfer                                                                                                                                                                        
                                                                                                                                                                                                                 
optional arguments:                                                                                                                                                                                              
  -h, --help            show this help message and exit                                                                                                                                                          
  -u SSH_USERNAME, --ssh_username SSH_USERNAME                                                                                                                                                                   
                        SSH target username                                                                                                                                                                      
  -p SSH_PASSWORD, --ssh_password SSH_PASSWORD                                                                                                                                                                   
                        SSH target password                                                                                                                                                                      
  -k SSH_KEY, --ssh_key SSH_KEY                                                                                                                                                                                  
                        SSH Private Key                                                                                                                                                                          
  -w, --wait            Wait for connection to open before executing command   
```

