import subprocess

def get_memorable_password():
    output = subprocess.check_output(["/usr/bin/gpw", "1", "10"])
    return output.decode('utf-8').rstrip() + "1!"



