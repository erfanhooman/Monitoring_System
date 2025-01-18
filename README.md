# Zabbix Helper

Zabbix Helper is a wrapper for Zabbix that simplifies the installation and monitoring experience for users unfamiliar with Zabbix. It offers an Ansible-based solution for seamless installation and utilizes the Zabbix API to present monitoring data in a modern and user-friendly interface.

## Features

1. **Simplified Installation**:
   - Provides an Ansible playbook for setting up Zabbix on systems.
   - Currently supports only Rocky Linux.

2. **Enhanced Monitoring Experience**:
   - Fetch and display monitoring data such as CPU, RAM, Disk, Filesystem, and Network metrics.
   - Simplified threshold-based alert system with recommendations.

3. **Role-Based User Management**:
   - **Super Admin**: Manages all users, including creating Admin accounts and managing their details.
   - **Admin**: Manages their own system's monitoring setup and creates sub-users.
   - **User**: Sub-users created by Admins to view specific monitoring details.

4. **Secure Connectivity**:
   - Uses OpenVPN for secure connections between Super Admin and Admin systems.

5. **Notification System**:
   - Threshold-based alerts.
   - Sends email notifications when metrics exceed defined thresholds.

---

## Workflow Overview

### Super Admin Workflow
1. **Login**:
   - Access the Super Admin dashboard.
   - View and manage Admin users.
2. **Create Admin Users**:
   - Generate an initialization bundle (includes init script, public key, and CA for OpenVPN).
   - Provide this bundle to Admin users.
3. **Manage Admin Details**:
   - Update Admin user details as needed.

### Admin Workflow
1. **Setup**:
   - Download the initialization bundle from the Super Admin.
   - Run the script to establish an OpenVPN connection.
   - IP is automatically added to the Admin’s details.
2. **Install Zabbix**:
   - Use the system’s API to set up and configure Zabbix via Ansible.
3. **Input Zabbix Credentials**:
   - Enter the Zabbix username and password.
4. **View Metrics**:
   - Access monitoring data for CPU, RAM, Disk, Filesystem, and Network metrics.
5. **Setup Alerts**:
   - Define thresholds for metrics.
   - Receive email notifications when thresholds are exceeded.

### User Workflow
1. **Login**:
   - Access system metrics as defined by the Admin.
2. **View Metrics**:
   - Explore specific monitoring data.
3. **Receive Alerts**:
   - Get notified when thresholds are breached.

---

## System Architecture

The system is divided into several components:

1. **User Roles**:
   - Super Admin, Admin, User.
2. **Secure Communication**:
   - OpenVPN ensures encrypted communication between Admin systems and the Super Admin server.
3. **Ansible Automation**:
   - Simplifies Zabbix installation and configuration on supported systems.
4. **Monitoring Interface**:
   - Leverages the Zabbix API to fetch and display monitoring data.
5. **Notification System**:
   - Alert mechanisms with email notifications.

---

## State Diagram
Below is an outline of the state charts involved:

1. **Super Admin State Diagram**:
   - **States**: Login, Dashboard, Create Admin, Manage Admin.
   - **Transitions**: Login → Dashboard → Create Admin/Manage Admin.

2. **Admin State Diagram**:
   - **States**: Login, Setup, Zabbix Installation, Metrics Overview, Alert Setup.
   - **Transitions**: Login → Setup → Zabbix Installation → Metrics Overview → Alert Setup.

3. **User State Diagram**:
   - **States**: Login, Metrics Overview, Receive Alerts.
   - **Transitions**: Login → Metrics Overview → Receive Alerts.

---

## Why Zabbix Helper?
While Zabbix offers comprehensive monitoring features, its complexity can be a barrier for non-technical users. Zabbix Helper bridges this gap by providing:

1. **Simplified Setup**:
   - Automates Zabbix installation with Ansible.
2. **User-Friendly Monitoring**:
   - Modern interface for accessing essential metrics.
3. **Actionable Alerts**:
   - Threshold-based recommendations and notifications.

---

## Limitations
- Currently supports only Rocky Linux for installation.
- Limited feature set compared to the full Zabbix platform.

---

## Future Plans
- Expand Ansible playbook support to other Linux distributions.
- Enhance the user interface with more visualization tools.
- Add more detailed alert customization and reporting.
- Integrate AI tools for generating intelligent recommendations and enhancing Zabbix functionality with AI-driven insights.

---

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to get started.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

