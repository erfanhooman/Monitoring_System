import os
import subprocess
import shutil
import tarfile

# TODO: fix Hardcoded since its not working on every computer

EASY_RSA_PATH = "/home/erfan/Desktop/Projects/UNI_Project/mserver/easy-rsa/3.2.1"
TA_KEY_PATH = "/home/erfan/Desktop/Projects/UNI_Project/mserver/easy-rsa/3.2.1/ta.key"

def create_openvpn_client(client_name, output_dir="/tmp/openvpn_clients"):
    """
    Fully automates OpenVPN client creation, handles all prompts, and bundles everything.
    """
    # Paths
    easyrsa_dir = os.path.expanduser(EASY_RSA_PATH)  # Path to EasyRSA
    pki_dir = os.path.join(easyrsa_dir, "pki")
    client_output_dir = os.path.join(output_dir, client_name)

    # Ensure directories exist
    os.makedirs(client_output_dir, exist_ok=True)

    try:
        # Step 1: Generate client certificate and key
        print(f"[+++++] Generating client certificates for '{client_name}'...")
        os.chdir(easyrsa_dir)  # Change directory to EasyRSA

        # Generate client request with no prompt
        print(f"[+++++] gen-req'...")
        subprocess.run(
            [f"./easyrsa", "gen-req", client_name, "nopass"],
            input=f"{client_name}\n".encode(),  # Auto-fill commonName
            check=True
        )

        # Sign the client request and auto-confirm 'yes'
        print(f"[+++++] sign-roneq'...")
        subprocess.run(
            [f"./easyrsa", "sign-req", "client", client_name],
            input=f"yes\n".encode(),
            check=True
        )

        # Step 2: Copy necessary files to client output directory
        print("[+] Copying certificates and keys...")
        cert_files = {
            "ca.crt": os.path.join(pki_dir, "ca.crt"),
            f"{client_name}.crt": os.path.join(pki_dir, "issued", f"{client_name}.crt"),
            f"{client_name}.key": os.path.join(pki_dir, "private", f"{client_name}.key")
        }

        # Copy each file and handle permission issues
        for file_name, file_path in cert_files.items():
            shutil.copy(file_path, os.path.join(client_output_dir, file_name))

        # Handle ta.key separately (fix permission error)
        print("[+] Copying ta.key...")
        if os.access(TA_KEY_PATH, os.R_OK):
            shutil.copy(TA_KEY_PATH, os.path.join(client_output_dir, "ta.key"))
        else:
            print("[-] Permission denied for ta.key. Running with sudo...")
            subprocess.run(["sudo", "cp", TA_KEY_PATH, client_output_dir])
            print("1")
            subprocess.run(["sudo", "chown", f"{os.getlogin()}:{os.getlogin()}", os.path.join(client_output_dir, "ta.key")])
            print("2")

        # Step 3: Create client configuration file
        client_conf = f"""
client
dev tun
proto udp
remote 192.168.6.144 1194
resolv-retry infinite
nobind
persist-key
persist-tun
tls-client
remote-cert-tls server
ca ca.crt
cert {client_name}.crt
key {client_name}.key
tls-auth ta.key 1
verb 3
        """
        print("3")
        with open(os.path.join(client_output_dir, "client.conf"), "w") as conf_file:
            conf_file.write(client_conf)
        print("4")
        pub_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC0ljpFywdsCBdxo3praEitW+x+LN1WmEpFqa8JsoqrEfEhTQB6suvMmCW4srKqVVqwwqXeQ85MYwS4aCKwrwW5CikvAjzOh6/Q6t8rprHi7A0eAZli38K9vXRf3+DI9+DKv8byvAPkhsONWWix1LsCB/UI+OuZZ9nWjxjeRatM/0RwUYZSUYYQZd5ZPDIICUngzFz641w0YuYOPJj2x4hYh0VRQYdAMIEx21/mzPPtkLW3aS08BbAlVCKJVsQVYwUWINtoHMR7sTriBGtLjB38tzZy/CASQon8uTP6C6OYHh645eiOWVFE5ZVfCCoHv9DvVoP2kusDwLqcr4V7YnpJ erfan@mserver"

        # Step 4: Create client setup script
        setup_script = f"""#!/bin/bash
# OpenVPN Client Setup Script
sudo yum install epel-release -y
sudo yum install openvpn openssh-server -y

# Copying OpenVPN client files
sudo mkdir -p /etc/openvpn/client/
sudo cp ca.crt {client_name}.crt {client_name}.key ta.key client.conf /etc/openvpn/client/

# Firewall rules
sudo firewall-cmd --permanent --add-service=openvpn
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload

ANSIBLE_USER="ansible_user"
sudo useradd -m -s /bin/bash $ANSIBLE_USER
sudo mkdir -p /home/$ANSIBLE_USER/.ssh
sudo echo "{pub_key}" | sudo tee /home/$ANSIBLE_USER/.ssh/authorized_keys
sudo chown -R $ANSIBLE_USER:$ANSIBLE_USER /home/$ANSIBLE_USER/.ssh
sudo chmod 700 /home/$ANSIBLE_USER/.ssh
sudo chmod 600 /home/$ANSIBLE_USER/.ssh/authorized_keys

# Enable OpenVPN client service
sudo systemctl enable openvpn-client@client
sudo systemctl start openvpn-client@client

echo "[+] OpenVPN setup completed. Client is now connected!"
"""
        setup_script_path = os.path.join(client_output_dir, "setup_client.sh")
        with open(setup_script_path, "w") as script_file:
            script_file.write(setup_script)
        os.chmod(setup_script_path, 0o755)

        # Step 5: Bundle everything into a tar.gz file
        bundle_path = os.path.join(output_dir, f"{client_name}_bundle.tar.gz")
        with tarfile.open(bundle_path, "w:gz") as tar:
            tar.add(client_output_dir, arcname=client_name)

        print(f"[+] Client bundle created: {bundle_path}")
        return True, bundle_path

    except subprocess.CalledProcessError as e:
        print(f"[-] Error running command: {e}")
        return False, None
    except Exception as e:
        print(f"[-] An error occurred: {e}")
        return False, None
    finally:
        if os.path.exists(client_output_dir):
            shutil.rmtree(client_output_dir)
