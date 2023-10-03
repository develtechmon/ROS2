## Getting Started

Refer to link
```
https://askubuntu.com/questions/972215/a-start-job-is-running-for-wait-for-network-to-be-configured-ubuntu-server-17-1
```

You can disable the `systemd-networkd-wait-online.service`, which is responsible for waiting for the network to be configured, using the following command:
```
sudo systemctl disable systemd-networkd-wait-online.service
```

To prevent the service from starting if requested by another service, you can mask it using:
```
systemctl mask systemd-networkd-wait-online.service
```