SHL2 LXD CHEAT SHEET
====================

Note that most used commands have an `lxc` prefix, only a few use `lxd` directly.

I'm leaving out the basic lxc commands because they're pretty easy to google,
basically there's `lxc launch`, `lxc copy`, `lxc delete`, `lxc start`, `lxc
stop`.  These all work roughly as you'd expect, use `--help` to get syntax.

List containers with status:

    [root@shl2 db57]# lxc list
    +---------------+---------+-----------------------+-----------------------------------------------+------------+-----------+
    |     NAME      |  STATE  |         IPV4          |                     IPV6                      |    TYPE    | SNAPSHOTS |
    +---------------+---------+-----------------------+-----------------------------------------------+------------+-----------+
    | democontainer | RUNNING | 10.102.216.253 (eth0) | fd42:1dce:6c06:d985:216:3eff:fe2d:9d02 (eth0) | PERSISTENT | 0         |
    +---------------+---------+-----------------------+-----------------------------------------------+------------+-----------+

Persistent containers are automatically brought up when the host system reboots.

Enter container shell:

    [root@shl2 db57]# lxc exec democontainer -- /bin/bash
    root@democontainer:~# lsb_release -a
    No LSB modules are available.
    Distributor ID:	Ubuntu
    Description:	Ubuntu 16.04.4 LTS
    Release:	16.04
    Codename:	xenial

Restart lxd:

     [root@shl2 db57]# snap restart lxd

Sometimes it might be necessary to run `snap stop lxd` and then `snap start lxd`,
not sure of the reason why.

Restarting lxd is going to add iptables rules, you can see them with the following
command:

    [root@shl2 db57]# iptables -t nat -L
    Chain PREROUTING (policy ACCEPT)
    target     prot opt source               destination         

    Chain INPUT (policy ACCEPT)
    target     prot opt source               destination         

    Chain OUTPUT (policy ACCEPT)
    target     prot opt source               destination         

    Chain POSTROUTING (policy ACCEPT)
    target     prot opt source               destination         
    MASQUERADE  all  --  localhost.susx.ac.uk/24 !localhost.susx.ac.uk/24  /* generated for LXD network lxdbr0 */

From the host, access a service installed in the container:

    [root@shl2 db57]# curl -s -D- -o/dev/null http://10.102.216.253
    HTTP/1.1 200 OK
    Date: Fri, 22 Jun 2018 11:35:24 GMT
    Server: Apache/2.4.18 (Ubuntu)
    Last-Modified: Thu, 21 Jun 2018 04:13:14 GMT
    ETag: "2c39-56f1f225c83fd"
    Accept-Ranges: bytes
    Content-Length: 11321
    Vary: Accept-Encoding
    Content-Type: text/html

Use iptables to forward ports from the host (shl2) to the container (democontainer):

    iptables -t nat -A PREROUTING -p tcp -i eth0 --dport 3000 -j DNAT \
       --to-destination 10.102.216.253:80

Now you can use this service from outside shl2:

    amoe@cslp019129 $ curl -s -D- -o/dev/null http://shl2.inf.susx.ac.uk:3000/                                                                                                                                 0.02s 
    HTTP/1.1 200 OK
    Date: Fri, 22 Jun 2018 11:38:01 GMT
    Server: Apache/2.4.18 (Ubuntu)
    Last-Modified: Thu, 21 Jun 2018 04:13:14 GMT
    ETag: "2c39-56f1f225c83fd"
    Accept-Ranges: bytes
    Content-Length: 11321
    Vary: Accept-Encoding
    Content-Type: text/html

Port 3000 on the host has been forwarded to port 80 in the container.

LXD is configured using LVM volumes for storage backend, this means that 
containers share storage and cloning them is cheap.

Note IT Helpdesk ticket #379644, should be in your email.  When it runs, puppet
will automatically remove the iptables rules that LXD needs to operate.  To
recreate those rules, you need to restart LXD.  Once this ticket is resolved,
those rules should be preserved by puppet.  The symptom of missing rules is
that your container won't be able to access internet hosts.

I believe that iptables forwarding rules that you create to expose in-container
services will also be wiped on puppet runs.  We don't have a good solution to
this yet.  Thoughts are welcome.

