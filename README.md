# EDDA Documentation Index

## Create container

You create a container using an _image_ for the OS.  Please consult the list of
[available images](https://us.images.linuxcontainers.org/).

You specify an image using a `DISTRIBUTION/RELEASE/ARCHITECTURE` string, like
`debian/stretch/amd64`.

Here are some examples:

    lxc init -s main images:ubuntu/bionic/amd64 mycontainer
    lxc launch -s main images:debian/stretch/amd64 spiral

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

## Granting SSH access to a user

The containers are not visible externally to their host.  Rather, they run on an
internal network `10.179.127.x`: I refer to this as the "LXD bridge".  Also, the
use of `lxc exec` requires root privileges on the container host, so it's not an
option for untrusted users.

To grant SSH access to a container, the user must first have regular login
rights to `shl1`.  That can be given by requesting that the user's Sussex
username is added to the group ` fs-informatics_shl1_group`.

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
