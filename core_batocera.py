from os.path import join

from core_model import FoldersInfo


def get_bc_userdata_root(host='batocera'):
    url = f'/run/user/1000/gvfs/sftp:host={host}/userdata'
    return url


def get_folders_of_bc(bc_url):
    bios_dir = join(bc_url, "bios")
    roms_dir = join(bc_url, "roms")
    return FoldersInfo(bios_dir, roms_dir)
