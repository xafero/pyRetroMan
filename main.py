import argparse
from os.path import join
from core_batocera import get_bc_userdata_root, get_folders_of_bc, read_bioses_readme
from core_basic import load_dict_if_exists

if __name__ == "__main__":
    bc_userdata = get_bc_userdata_root()
    bc_folders = get_folders_of_bc(bc_userdata)
    print(f"Bios folder => {bc_folders.bios}")
    print(f"Roms folder => {bc_folders.roms}")
