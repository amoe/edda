import fabric
import invoke
import getpass
import shlex
import sys

new_password = getpass.getpass()
connect_kwargs = {'password': new_password}

config = fabric.Config(
    overrides={'sudo': {'password': new_password}}
)

c = fabric.Connection(
    'shl1.inf.susx.ac.uk', config=config, connect_kwargs=connect_kwargs
)

print("testing connection")
c.sudo("/bin/true")
print("success")

LXC_BINARY_PATH = "/var/lib/snapd/snap/bin/lxc"
STORAGE_POOL_NAME = "main"
BASE_IMAGE_NAME = "images:ubuntu/bionic/amd64"
CONTAINER_NAME = "demo"

def sudo_template(c, tmpl, *rest):
    quoted = [shlex.quote(s) for s in rest]
    expanded = tmpl.format(*quoted)
    c.sudo(expanded)


def do_all():
    sudo_template(c, "{} init -s {} {} {}", LXC_BINARY_PATH, STORAGE_POOL_NAME, BASE_IMAGE_NAME, CONTAINER_NAME)
    sudo_template(c, "{} -v start {}", LXC_BINARY_PATH, CONTAINER_NAME)
    sudo_template(c, "{} -v start {}", LXC_BINARY_PATH, CONTAINER_NAME)

try:
    do_all()
except invoke.exceptions.UnexpectedExit:
    print("Fail")
    sys.exit(1)


# The containers are initialized with a 10GB root partition.
# There are several things, storagge pools and storage volumes.

# Storage volumes exist.
# These are not lxd-specific.

# Storage volumes exist within a pool, it seems.

# Our LVM storage pool is main.

# So to list storage volumes, we do
# `lxc storage volume list main`
# It won't tell you the allocated size.

# Each volume for a container name is prefixed with container/

# To show storage volume for ajs86, do

# lxc -v storage volume show main container/ajs86

# This will give

# config:
#   block.filesystem: ext4
#   block.mount_options: discard
#   size: 10GB
# description: ""
# name: ajs86
# type: container
# used_by:
# - /1.0/containers/ajs86
# location: none


# Here note that we have config.size.

# Resizing won't work:
# lxc -v storage volume set main container/demo size 80GB
# Error: The [size] properties cannot be changed for "lvm" storage volumes


# REcommended way is to attach a new storage volume as such.

# Storage pool prefix is /var/snap/lxd/common/lxd/storage-pools
# So full path will end up as
# /var/snap/lxd/common/lxd/storage-pools/main/custom/ajs86-1
# Not sure what uid:gid to do it to.

# Documentation on uid/gid mapping:
# https://stgraber.org/2017/06/15/custom-user-mappings-in-lxd-containers/

# lxc storage volume create main ajs1
# sudo chown -R uid:gid /var/lib/lxd/storage-pools/main/custom/<storage-volume-name>
# lxc storage volume attach <pool-name> <storage-volume-name> <container-name> <device-name> <path>

# There are some potential issues with this, notably the one that we don't know
# what uid and gid would be correct.  Also those directories seem to be empty
# which is a touch worrying.

# https://asciinema.org/a/128584
# Actually it doesn't seem to be needed.  See https://asciinema.org/a/128585

#" By default LXD will make an attached storage volume writable by the container it is attached to. This means it will change the ownership of the storage volume to the container’s id mapping"

#This is all from https://blog.ubuntu.com/2017/07/12/storage-management-in-lxd-2-15
