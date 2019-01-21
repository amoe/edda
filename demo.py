import lxc

container = lxc.Container("test")

# container has some methods
print(dir(container))

create_args = {
    'template': 'download',
    'flags': lxc.LXC_CREATE_QUIET,
    'args': {
        'dist': 'ubuntu',
        'release': 'trusty',
        'arch': 'i386'
    }
}

result = container.create(**create_args)
print(result)

if not result:
    print("Something went wrong...")
