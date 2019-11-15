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
