#!/bin/bash
# OpenVPN Client Setup Script
sudo yum install epel-release -y
sudo yum install openvpn openssh-server -y

# Copying OpenVPN client files
sudo mkdir -p /etc/openvpn/client/
sudo cp ca.crt {CLIENT_CERT} {CLIENT_KEY} ta.key client.conf /etc/openvpn/client/

# Firewall rules
sudo firewall-cmd --permanent --add-service=openvpn
sudo firewall-cmd --permanent --add-service=ssh
sudo firewall-cmd --reload

ANSIBLE_USER="ansible_user"
sudo useradd -m -s /bin/bash $ANSIBLE_USER

sudo mkdir -p /home/$ANSIBLE_USER/.ssh
sudo echo "{PUBLIC_KEY}" | sudo tee /home/$ANSIBLE_USER/.ssh/authorized_keys
sudo chown -R $ANSIBLE_USER:$ANSIBLE_USER /home/$ANSIBLE_USER/.ssh
sudo chmod 700 /home/$ANSIBLE_USER/.ssh
sudo chmod 600 /home/$ANSIBLE_USER/.ssh/authorized_keys

sudo bash -c "echo '$ANSIBLE_USER ALL=(ALL) NOPASSWD: /usr/bin/yum, /bin/systemctl, /usr/bin/cp, /usr/bin/python3, /usr/bin/pip3, /bin/mkdir' > /etc/sudoers.d/ansible_user"
sudo chmod 440 /etc/sudoers.d/ansible_user

sudo bash -c "echo '$ANSIBLE_USER ALL=(ALL) NOPASSWD: ALL' >> /etc/sudoers"

# Enable OpenVPN client systemd-service
sudo systemctl enable openvpn-client@client
sudo systemctl start openvpn-client@client

echo "[+] OpenVPN setup completed. Client is now connected!"
