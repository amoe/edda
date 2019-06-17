APACHE CHEAT SHEET

Use ProxyPass, ProxyPassReverse, ProxyPreserveHost.  Then your lxd container
should use the main::apache Puppet class and its vhost should have a ServerName
matching the given hostname.  This way, traffic will flow as such:

1.  HTTP request enters shl1 httpd (CentOS)
2.  HTTP request is proxied to _some internal lxc ip_ while keeping its Host header.
3.  Apache on _some container_ checks its request for the Host header.
4.  Apache on _some container_ matches the host header and serves the vhost.

This approach avoids using `mod_headers` to modify the headers in httpd, and also
avoid doing hacks using the /etc/hosts file.

The downside is that the outer hostname has to be specified in two places, once
in-container and once outside-of-container.

Bear in mind that timeouts that exist at the perimeter Apache on shl1 will apply,
so if you want to adjust the timeouts, you may need to adjust them 'all the way
down' so to speak.
