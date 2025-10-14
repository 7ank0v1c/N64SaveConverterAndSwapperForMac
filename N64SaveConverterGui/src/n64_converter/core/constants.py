# core/constants.py
EEP_EXT = ".eep"
SRA_EXT = ".sra"
FLA_EXT = ".fla"
MPK_EXT = ".mpk"
SRM_EXT = ".srm"

SIZE_EEP = 2048
SIZE_SRA = 32768
SIZE_FLA = 131072
SIZE_MPK = 131072
SIZE_SRM = 296960

SIZE_SRA_SRM_OFFSET = 133120
SIZE_FLA_SRM_OFFSET = SIZE_SRM - SIZE_FLA
SIZE_MPK_SRM_OFFSET = 2048

EEP_LABEL = "EEPROM (.eep)"
SRA_LABEL = "SRAM (.sra)"
FLA_LABEL = "FlashRAM (.fla)"
MPK_LABEL = "Controller Pak (.mpk)"
SRM_LABEL = "Retroarch Save (.srm)"

NATIVE_LABEL = "Native / Cart Dump"
PJ64_LABEL = "Project64/Mupen64"
RA_LABEL = "Retroarch"
WII_LABEL = "Wii/WiiU/Everdrive64"

file_types = [EEP_LABEL, SRA_LABEL, FLA_LABEL, MPK_LABEL, SRM_LABEL]
source_list = [NATIVE_LABEL, PJ64_LABEL, RA_LABEL, WII_LABEL]
target_list = [NATIVE_LABEL, PJ64_LABEL, RA_LABEL, WII_LABEL]
