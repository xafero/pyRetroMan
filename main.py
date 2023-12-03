from core_basic import load_dict_if_exists
from core_batocera import get_bc_userdata_root, get_folders_of_bc, read_bioses_readme, read_roms_infos

if __name__ == "__main__":
    bc_userdata = get_bc_userdata_root()
    bc_folders = get_folders_of_bc(bc_userdata)
    print(f"Bios folder => {bc_folders.bios}")
    bc_bios_index = load_dict_if_exists("bc_bios_index", lambda d: read_bioses_readme(bc_folders.bios, d))
    print(f"Roms folder => {bc_folders.roms}")
    bc_mach_index = load_dict_if_exists("bc_mach_index", lambda d: read_roms_infos(bc_folders.roms, d))
