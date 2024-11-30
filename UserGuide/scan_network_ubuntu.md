# Getting Started

This is userguide to scan network in your area incase you forget the IP address. Please
follow this step

````
sudo apt install arp-scan
````

and run this command
```
sudo arp-scan --localnet
```

You will see the following IP address
````
Interface: wlp4s0, type: EN10MB, MAC: 60:f6:77:90:33:c8, IPv4: 192.168.102.89
Starting arp-scan 1.9.7 with 256 hosts (https://github.com/royhills/arp-scan)
192.168.102.3	d0:37:45:54:88:db	TP-LINK TECHNOLOGIES CO.,LTD.
192.168.102.247	82:71:21:a5:85:2a	(Unknown: locally administered)
192.168.102.150	e4:5f:01:4e:2e:d6	(Unknown)
192.168.102.150	e4:5f:01:4e:2e:d6	(Unknown) (DUP: 2)

4 packets received by filter, 0 packets dropped by kernel
Ending arp-scan 1.9.7: 256 hosts scanned in 1.979 seconds (129.36 hosts/sec). 4 responded
````

Then ssh
```
sssh <your name>@192.168.102.150
```
