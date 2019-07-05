remote lxc
lxc remote list -- show the list of remotes.

From the client host:

    amoe@cslp019129 $ sudo nmap -p 8443 192.168.56.102                                               0.01s 

    Starting Nmap 7.40 ( https://nmap.org ) at 2019-07-05 09:25 BST
    Nmap scan report for 192.168.56.102
    Host is up (0.00028s latency).
    PORT     STATE SERVICE
    8443/tcp open  https-alt
    MAC Address: 08:00:27:CB:02:25 (Oracle VirtualBox virtual NIC)

    Nmap done: 1 IP address (1 host up) scanned in 0.65 seconds


The admin password is given by `core.trust-password`.

lxc config set core.trust_password xyzzy

lxc remote add 192.168.56.102



    amoe@cslp019129 $ lxc remote switch 192.168.56.102

Using lxc exec you can then get a shell across the network.

However it's clearly unacceptable to give all users access to the lxd host in
this way.
