# The edda tool

## Secret files

There's a directory called `secret` that is present within gitignore.

## Requirements

python3-lxc, version 2.0.7+

You can find it at <https://github.com/lxc/python3-lxc>.

However LXD should also have its own commands, and its own python bindings?
There is also pylxd, see <https://github.com/lxc/pylxd>

## How to install pylxd

    pip3 install pylxd

## Give user storage capacity

> edda grant-storage dave 20GB

What will this command do?  It will create a storage volume `dave-extra1` and
attach it to the container `dave`..  The size limit will be passed to the
container.  The space will be mounted under /data.  The size limit will only
work on certain storage pool backends.

## Target platform

lxc/lxd version 3.4
