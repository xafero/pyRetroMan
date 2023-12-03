from __future__ import annotations
from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard


@dataclass
class FoldersInfo:
    bios: str
    roms: str


@dataclass
class MachineInfo(JSONWizard):
    id: str
    label: str
    exts: list[str] = field(default_factory=list)


@dataclass
class GameInfo(JSONWizard):
    id: str
    label: str
    size: int
    mach: str
    file: str
    scraped: dict
