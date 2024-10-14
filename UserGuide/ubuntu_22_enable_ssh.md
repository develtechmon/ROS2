# Getting Started

This is userguide on how to enable `ssh` in `Ubuntu 22`. So that we can `ssh` to this machine using our windows.

## Step 1: Update your system
```
sudo apt update
sudo apt upgrade
```

## Step 2: Install the OpenSSH Server
```
sudo apt install openssh-server
```

## Step 3: Start the SSH Service
```
sudo systemctl enable --now ssh
```

## Step 4: Verify The installation
```
sudo systemctl status ssh
```
You should see output indicating that the service is active and running.

## Step 5: Allow SSH Through The firewall (if enabled):
```
sudo ufw allow ssh
```


## Step 6: Connect to your server
From another machine, you can now connect to your Ubuntu server via SSH using a command like:
```
ssh jlukas@192.168.247.129
```
