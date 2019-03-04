# Add an IP address

Visit /etc/sysconfig/network-scripts.  You'll find many configuration files.

The file that you want is `ifcfg-eth0`.

You add IP addresses in this file with a series of specifications.

This adds two IP addresses to the `eth0` interface:

    IPADDR0=139.184.49.242
    PREFIX0=23
    GATEWAY0=139.184.48.1
    IPADDR1=139.184.48.71
    PREFIX1=23
    GATEWAY1=139.184.48.1

So, every individual IP `n` (which is just an integer you increase yourself)
needs these lines `IPADDRn`, `PREFIXn`, `GATEWAYn`.

All these remain the same, except for `IPADDRn`.  Don't touch `DNS1` and `DNS2`.

To reload the configuration, run `systemctl restart network`.
