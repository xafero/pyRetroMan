from os.path import join, exists

from core_model import FoldersInfo


def get_bc_userdata_root(host='batocera'):
    url = f'/run/user/1000/gvfs/sftp:host={host}/userdata'
    return url


def get_folders_of_bc(bc_url):
    bios_dir = join(bc_url, "bios")
    roms_dir = join(bc_url, "roms")
    return FoldersInfo(bios_dir, roms_dir)


def read_bioses_readme(dir_path, bios_list):
    if len(bios_list) >= 1:
        return bios_list
    if not exists(dir_path):
        print(f"The directory '{dir_path}' does not exist!")
        return bios_list
    bios_meta = join(dir_path, "readme.txt")
    last_mach_name = ''
    bmark = 'bios/'
    with open(bios_meta) as meta_file:
        for line in meta_file:
            if line.endswith(':' + '\n'):
                mach_name = line.strip().rstrip(':')
                last_mach_name = mach_name
                continue
            if bmark not in line:
                continue
            lineP = line.strip().split(bmark)
            lineHash = ''
            lineFile = ''
            if len(lineP) == 1:
                lineFile = lineP[0].strip()
            elif len(lineP) == 2:
                lineHash = lineP[0].strip()
                lineFile = lineP[1].strip()
            current_mach = {}
            if last_mach_name in bios_list:
                current_mach = bios_list[last_mach_name]
            else:
                bios_list[last_mach_name] = current_mach
            current_hashes = []
            if lineFile in current_mach:
                current_hashes = current_mach[lineFile]
            else:
                current_mach[lineFile] = current_hashes
            current_hashes.append(lineHash)
    return bios_list
