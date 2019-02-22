# SHL1

We have one LVM-backed storage pool.  This is called `main`.  We have 1.50TB
of space on this volume.

[root@shl1 db57]# lxc storage volume create main ajs86_extra size=20GB

THis will work with LVM (not with dir).  Dir just gives all available space
to the container.
