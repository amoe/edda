# EDDA Documentation Index

## Create container

You create a container using an _image_ for the OS.  Please consult the list of
[available images](https://us.images.linuxcontainers.org/).

You specify an image using a `DISTRIBUTION/RELEASE/ARCHITECTURE` string, like
`debian/stretch/amd64`.

Here are some examples:

    lxc init -s main images:ubuntu/bionic/amd64 mycontainer
    lxc launch -s main images:debian/buster/amd64 spiral
    lxc init -s main images:ubuntu/xenial/amd64 mycontainer2

The last argument to the command specifies the name of the container.  `images/`
is a necessary prefix.

Using `launch` will both create the container and start it.  `init` will just
create the container.  You can start it later using `lxc start`.

Container names should use kebab case, i.e. `names-like-this`.

## Entering the container environment

You use `lxc exec` and pass a shell.

    lxc exec mycontainer -- /bin/bash

## Configuring containers

There's no standard way to configure containers.  You can do them yourself by
hand, or use a configuration management tool like Puppet or Ansible.
Alternatively, if the container should be managed by another user, you can grant
the user SSH access directly.


## More info on command

Use the --verbose --debug options at the end of your `lxc` command line.

## Restarting the LXD

 snap restart lxd

This can take up to 5 minutes.  All containers need to be shutdown.  They will
restart shortly after the daemon has itself restarted.

## Force a container to stop

lxc stop mycontainer --force

The order of the options is important.

## Granting SSH access to a user

The containers are not visible externally to their host.  Rather, they run on an
internal network `10.179.127.x`: I refer to this as the "LXD bridge".  Also, the
use of `lxc exec` requires root privileges on the container host, so it's not an
option for untrusted users.

To grant SSH access to a container, the user must first have regular login
rights to `shl1`.  That can be given by requesting that the user's Sussex
username is added to the group ` fs-informatics_shl1_group`.  You can check the
current membership of this group by running this command:

    $ getent group fs-informatics_shl1_group

Once they have logged in to shl1 as a regular user, they will be able to access
hosts on the LXD bridge.  So all that's required is to find the IP of the
relevant container (which is shown using the `lxc list` command), and ssh into
that container:

     ssh root@10.179.127.60

Note that this requires two things:

1.  sshd is running inside the container (you will have to install it yourself,
just as in a regular Linux environment).

2.  sshd is configured to accept logins as root (using `PermitRootLogin yes` in
    sshd_config)

3.  a password has been set for root.

## Exposing HTTP services

You need to modify files in /etc/httpd on shl1 itself.  Look at the existing
files under /etc/httpd/conf.d for a template.  As of November 2019, a reasonable
configuration looks like this:

    <VirtualHost aegir.inf.susx.ac.uk:443>
        ServerName aegir.inf.susx.ac.uk
        SSLEngine on
        SSLCertificateFile "/usr/local/share/ssl/edda-multiple-san/certificate.pem"
        SSLCertificateKeyFile "/usr/local/share/ssl/edda-multiple-san/key.pem"
        SSLCACertificateFile "/usr/local/share/ssl/edda-multiple-san/root.pem"
        SSLCertificateChainFile "/usr/local/share/ssl/edda-multiple-san/chain.pem"


        ProxyPass "/" "http://10.179.127.20:80/" retry=0
        ProxyPassReverse "/" "http://10.179.127.20:80/"
        ProxyPreserveHost on

        Header always set Strict-Transport-Security "max-age=15768000"
    </VirtualHost>

In this case the in-container service is exposed on port 80 of the container.

You can test your service from the command line by setting the Host header.

    curl -D- -H "Host: eir.inf.susx.ac.uk" http://10.179.127.3/


## Getting SSL certificates

You can use acme.sh

acme.sh --issue --alpn --standalone -d foo.erwin.org

Port 80 is firewalled off by ITS.  This should actually be changed and replaced
with 80 -> 443 redirects.

[Thu 30 Jan 13:55:39 GMT 2020] Your cert is in  /root/.acme.sh/archive.reanimatingdata.co.uk/archive.reanimatingdata.co.uk.cer 
[Thu 30 Jan 13:55:39 GMT 2020] Your cert key is in  /root/.acme.sh/archive.reanimatingdata.co.uk/archive.reanimatingdata.co.uk.key 
[Thu 30 Jan 13:55:39 GMT 2020] The intermediate CA cert is in  /root/.acme.sh/archive.reanimatingdata.co.uk/ca.cer 
[Thu 30 Jan 13:55:39 GMT 2020] And the full chain certs is there:  /root/.acme.sh/archive.reanimatingdata.co.uk/fullchain.cer 



Put certs in /usr/local/share/ssl/subdir.

    SSLEngine on
    SSLCertificateFile "/usr/local/share/ssl/archive.reanimatingdata.co.uk/certificate.pem"
    SSLCertificateKeyFile "/usr/local/share/ssl/archive.reanimatingdata.co.uk/key.pem"
    SSLCACertificateFile "/usr/local/share/ssl/archive.reanimatingdata.co.uk/root.pem"
    SSLCertificateChainFile "/usr/local/share/ssl/archive.reanimatingdata.co.uk/chain.pem"

## Check group memberships

The relevant group for access to the shl1 server is the below.

    -bash-4.2$ getent group fs-informatics_shl1_group

Requests for access currently have to go through paulk.


## Set up SSH key for a user

The .ssh directory file needs to exist, which normally lives under
`/its/home/<username>`

    mkdir /its/home/ca296/.ssh
    chmod 0700 /its/home/ca296/.ssh
    cat > /its/home/ca296/.ssh/authorized_keys
    foo
    ^D
    chmod 0600 /its/home/ca296/.ssh/authorized_keys
    chown -R ca296:ca296_g /its/home/ca296/.ssh


## lxc list is slow?

Try to use `lxc list --fast` instead.

## Add extra storage / disk space for a user's container

See the instructions [here](add_storage.md).
