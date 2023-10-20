## Getting Started

This is userguide on how to install `ssh into Raspberry Pi` Ubuntu

Visit this link: https://www.cyberciti.biz/faq/ubuntu-linux-install-openssh-server/

Step 1
```
sudo apt-get install openssh-server
```

Step 2
```
sudo systemctl enable ssh
## OR enable and start the ssh service immediately ##
sudo systemctl enable ssh --now
```

Step 3
```
sudo systemctl start ssh
```

Step 4
```
ssh userName@Your-server-name-IP
ssh ec2-user@ec2-aws-ip-here
```