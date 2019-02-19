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

try:
    do_all()
except invoke.exceptions.UnexpectedExit:
    print("Fail")
    sys.exit(1)

