# Add storage

    lxc storage volume create main jc_extra size=20GB
    lxc storage volume attach main jc_extra jc

Note that the `size=` specification will only work when using the non-directory
backends, eg `lvm`.  Hence you need to use the `main` storage pool in practice.
    
