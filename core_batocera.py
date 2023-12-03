from os import listdir, stat
from os.path import join, exists, isdir

import humanize
import xmltodict

from core_basic import get_dir_size, set_non_null
from core_model import FoldersInfo, MachineInfo, GameInfo


def get_bc_userdata_root(host='batocera'):
    url = f'/run/user/1000/gvfs/sftp:host={host}/userdata'
    return url


def get_folders_of_bc(bc_url):
    bios_dir = join(bc_url, "bios")
    roms_dir = join(bc_url, "roms")
    return FoldersInfo(bios_dir, roms_dir)


def read_gamelist(dir_path, meta_list):
    if len(meta_list) >= 1:
        return meta_list
    if not exists(dir_path):
        print(f"The directory '{dir_path}' does not exist!")
        return meta_list
    info_path = join(dir_path, "gamelist.xml")
    if not exists(info_path):
        return meta_list
    with open(info_path, 'r') as info_file:
        doc = xmltodict.parse(info_file.read())
        gla = doc["gameList"]["game"]
        if not isinstance(gla, list):
            gla = [gla]
        for entry in gla:
            entry_path = entry['path'].strip('./')
            entry_file = join(dir_path, entry_path)
            if not exists(entry_file):
                continue
            m_item = dict()
            set_non_null(m_item, "id", entry.get("@id", None))
            set_non_null(m_item, "md5", entry.get("md5", None))
            set_non_null(m_item, "region", entry.get("region", None))
            set_non_null(m_item, "developer", entry.get("developer", entry.get("publisher", None)))
            set_non_null(m_item, "name", entry["name"])
            set_non_null(m_item, "genre", entry.get("genre", "").split(' / '))
            set_non_null(m_item, "lang", entry.get("lang", "").split(','))
            meta_list[entry_path] = m_item
    return meta_list


def read_roms_infos(dir_path, mach_list):
    if len(mach_list) >= 1:
        return mach_list
    if not exists(dir_path):
        print(f"The directory '{dir_path}' does not exist!")
        return mach_list
    for machine in sorted(listdir(dir_path)):
        machine_path = join(dir_path, machine)
        info_path = join(machine_path, "_info.txt")
        with open(info_path, 'r') as info_file:
            lines = info_file.readlines()
            info_mach = lines[0].split("## SYSTEM ")[1].split('##')[0].rstrip()
            info_exts = lines[2].split("accepted: ")[1].replace('"', ' ').strip().split(' ')
            item = MachineInfo(machine, info_mach, info_exts)
            mach_list[machine] = item.to_dict()
    return mach_list


def find_roms(dir_path, mach_list, rom_list):
    if len(rom_list) >= 1:
        return rom_list
    if not exists(dir_path):
        print(f"The directory '{dir_path}' does not exist!")
        return rom_list
    for machine in mach_list:
        mach_data = MachineInfo.from_dict(mach_list[machine])
        mach_path = join(dir_path, mach_data.id)
        xml_data = read_gamelist(mach_path, dict())
        mach_txt = mach_data.label
        mach_shown = False
        for game in sorted(listdir(mach_path)):
            game_path = join(mach_path, game)
            for ext in mach_data.exts:
                if not game_path.endswith(ext):
                    continue
                if not mach_shown:
                    print(f' * machine [{machine}] {mach_txt}')
                    mach_shown = True
                game_name_raw = game.replace(ext, '').strip()
                game_name = game_name_raw.split(' (', maxsplit=1)[0].strip()
                if isdir(game_path):
                    game_size = get_dir_size(game_path)
                else:
                    game_stats = stat(game_path)
                    game_size = game_stats.st_size
                game_hsize = humanize.naturalsize(game_size)
                print(f'    # game "{game_name}" is {game_hsize}')
                rom_mach = dict()
                if machine in rom_list:
                    rom_mach = rom_list[machine]
                else:
                    rom_list[machine] = rom_mach
                g_id = game.replace('-', ' ').replace('_', ' ').replace(',', ' ').replace("'", ' ') \
                    .replace('(', '_').replace(')', '_').replace('.', ' ').replace('!', ' ') \
                    .replace('&', ' ').replace('[', ' ').replace(']', ' ').replace(' ', '').strip()
                g_xml = xml_data.get(game, None)
                g_item = GameInfo(g_id.lower(), game_name, game_size, machine, game, g_xml)
                rom_mach[g_item.id] = g_item.to_dict()
    return rom_list


def read_bioses_readme(dir_path, bios_list):
    if len(bios_list) >= 1:
        return bios_list
    if not exists(dir_path):
        print(f"The directory '{dir_path}' does not exist!")
        return bios_list
    bios_meta = join(dir_path, "readme.txt")
    last_mach_name = ''
    bmark = 'bios/'
    with open(bios_meta, 'r') as meta_file:
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
