import os
import subprocess
import shutil
import tarfile
import logging

from django.conf import settings

logger = logging.getLogger("ms")

EASY_RSA_PATH = settings.EASY_RSA_PATH
TA_KEY_PATH = settings.TA_KEY_PATH
PUBLIC_KEY = settings.PUBLIC_KEY

def generate_client_conf(client_name):
    return f"""
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

def generate_setup_script(client_name, client_output_dir):
    setup_script_path = os.path.join(client_output_dir, "setup_client.sh")

    file_path = os.path.join(os.path.dirname(__file__), "setup_client_template.sh")
    with open(file_path, "r") as template_file:
        setup_script = template_file.read()

    # Replace placeholders with actual values
    setup_script = setup_script.replace("{CLIENT_CERT}", f"{client_name}.crt")
    setup_script = setup_script.replace("{CLIENT_KEY}", f"{client_name}.key")
    setup_script = setup_script.replace("{PUBLIC_KEY}", PUBLIC_KEY)

    with open(setup_script_path, "w") as script_file:
        script_file.write(setup_script)

    os.chmod(setup_script_path, 0o755)
    return setup_script_path


def create_openvpn_client(client_name, output_dir="/tmp/openvpn_clients"):
    """
    Fully automates OpenVPN client creation, handles all prompts, and bundles everything.
    """
    easyrsa_dir = os.path.expanduser(EASY_RSA_PATH)  # Path to EasyRSA
    pki_dir = os.path.join(easyrsa_dir, "pki")
    client_output_dir = os.path.join(output_dir, client_name)

    os.makedirs(client_output_dir, exist_ok=True)

    try:
        logger.info(f"Generating client certificates for '{client_name}'...  gen-req'...")
        subprocess.run(
            [f"./easyrsa", "gen-req", client_name, "nopass"],
            input=f"{client_name}\n".encode(),
            cwd=easyrsa_dir,
            check=True
        )

        logger.info(f"[+++++] sign-roneq' for client {client_name}...")
        subprocess.run(
            [f"./easyrsa", "sign-req", "client", client_name],
            input=f"yes\n".encode(),
            cwd=easyrsa_dir,
            check=True
        )

        cert_files = {
            "ca.crt": os.path.join(pki_dir, "ca.crt"),
            f"{client_name}.crt": os.path.join(pki_dir, "issued", f"{client_name}.crt"),
            f"{client_name}.key": os.path.join(pki_dir, "private", f"{client_name}.key")
        }

        for file_name, file_path in cert_files.items():
            shutil.copy(file_path, os.path.join(client_output_dir, file_name))

        if os.access(TA_KEY_PATH, os.R_OK):
            shutil.copy(TA_KEY_PATH, os.path.join(client_output_dir, "ta.key"))
        else:
            subprocess.run(["sudo", "cp", TA_KEY_PATH, client_output_dir])
            subprocess.run(["sudo", "chown", f"{os.getlogin()}:{os.getlogin()}", os.path.join(client_output_dir, "ta.key")])

        # Generate client configuration
        client_conf = generate_client_conf(client_name)
        with open(os.path.join(client_output_dir, "client.conf"), "w") as conf_file:
            conf_file.write(client_conf)

        # Generate setup script
        generate_setup_script(client_name, client_output_dir)

        bundle_path = os.path.join(output_dir, f"{client_name}_bundle.tar.gz")
        with tarfile.open(bundle_path, "w:gz") as tar:
            tar.add(client_output_dir, arcname=client_name)

        logger.info(f"[+] Client bundle created: {bundle_path}")
        return True, bundle_path

    except subprocess.CalledProcessError as e:
        logger.error(f"Error running command: {e}")

        return False, None
    except ValueError as e:
        logger.error(f"[-] An error occurred: {e}")
        return False, None
    finally:
        if os.path.exists(client_output_dir):
            shutil.rmtree(client_output_dir)
