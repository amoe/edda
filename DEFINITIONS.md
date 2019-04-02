Lxd version is pinned to 3.6

lxd   3.6        9263  stable    canonical✓  -

You can find it in rarewares, or with a canonical link.

Here is the 3.6 release [25MB]:

https://github.com/lxc/lxd/releases/download/lxd-3.6/lxd-3.6.tar.gz


It comes with a makefile.

You must run 'make deps'.

Install build dependencies:

    aptitude install tcl libuv1-dev libcap-dev libacl1-dev

You need golang 1.9+, which is not in Debian.  Do not fuck around with building
it from source; there's a bootstrapping process involved.  Also do not use the
upstream binary release as it has some ;;;;; idiosyncrasies.

The best is to set up stretch-backports and install from there.

go get -d -v github.com/amoe/lxd/lxd
cd $GOPATH/src/github.com/lxc/lxd
make deps
make


`make deps`

It will ask you to set some environment variables, set them.

Then run 

The snap is included but you have to install it with the --dangerous switch.

The client should have the md5sum `a83c21420b87a55977391ca287522617`.
