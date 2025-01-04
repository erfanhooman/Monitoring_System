import os
import subprocess
import shutil
import tarfile
import logging

from django.conf import settings

logger = logging.getLogger("ms")

EASY_RSA_PATH = settings.EASY_RSA_PATH
TA_KEY_PATH = settings.TA_KEY_PATH
PUBLIC_KEY = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDRco87pX7BxiODgo1Nf3yjsfkul63ut7hyfqz3WwHPTLwsWAeyebvdKXCOpj+qXoX5YRnwPfl31liGGqz7hVZWtdlPNZ2BNIcb8xhz41x8m8uJZP9qihyz80ij95+4RWV6WNShBLqrPj7SPIid996GEqT8iqNcvhJWPCPRsw1Ds96Xjleo+IYwf98lQ+hq2EWhu2mVJPnkQfpQqPfXgaIFkomjVV6z9/dYQLWxIbqxdfYI1Ta19UxlT8M6dSuROekMeZBd+DubwTfilVfPypXbEhurM01XzvWfrYVkKX3QznBWCECR/FmALNPU0Rs1w6Yu3cgXvVAnGi35IpDDs4t5q74uKEjqkPSAfzxiQpsvUtpC5oJdhe+2NfVV4uf81qwJUk77cdWIewa/0wuieCfFkGOIiik+CFKlZqO/bXvxa8FP9qpFTrWi+JeObMxr0bDplq4mYRsnE7a2gmNZCsF5/pedwBG88S3WUo4MIEbAaPeCpCV7mz30ZVHl+CO5Dlz60o/YBEEj/vzBMh1SaexMQ7+7afT7l+k+e8h1RSs978bXhPXjynBW3+vpUPMSP8lWSdb0x0vZcRYWHEuZcaLk2cErywVFsnP9Mpe8Ei6rHK8b8eI5eWAjRXRBx9oHQ7uEZxxAmoLtoDR4SA6odVCvTH6s2lPamYTQkIbT9rArhw== er.callof.007875@gmail.com"
SERVER_IP_ADDR = settings.SERVER_IP_ADDR

def generate_client_conf(client_name):
    return f"""
client
dev tun
proto udp
remote {SERVER_IP_ADDR} 1194
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
