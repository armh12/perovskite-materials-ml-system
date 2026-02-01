import enum


class Element(str, enum.Enum):
    # A-Site Ions
    MA = "MA"
    FA = "FA"
    CS = "Cs"
    BA = "BA"
    PEA = "PEA"
    PA = "PA"
    RB = "Rb"
    GU = "GU"
    EA = "EA"
    TMA = "TMA"
    IPEA = "IPEA"
    FEA = "FEA"
    BEA = "BEA"
    BDA = "BDA2"
    HEA = "HEA"
    GA = "GA"
    NA = "NA"
    IA = "IA"
    CH3S = "CH3S"
    TFEA = "TFEA"
    NH4 = "NH4"
    DMA = "DMA"
    GABR3 = "GABr3"
    THA = "THA"
    PDA = "PDA2"
    EU = "EU"
    ACTA = "ACTA"
    CIEA = "CIEA"
    AN = "AN"
    TEA = "TEA"
    GNA = "GNA"
    PNA = "PNA"

    # B-Site Ions
    PB = "Pb"
    SN = "Sn"
    PBO = "PbO"
    BI = "Bi"
    SB = "Sb"
    AG = "Ag"
    BA_B = "Ba2"
    GE = "Ge"
    CU = "Cu"
    MN = "Mn"
    LA = "La"
    TL = "Tl"
    ZN = "Zn"

    # X-Site Ions
    BR = "Br"
    CL = "Cl"
    I = "I"

    @classmethod
    def get_element_by_name(cls, name: str):
        """
        Retrieves an Element enum member by its name (e.g., 'MA', 'Pb', 'Br').

        Args:
            name (str): The name of the element/ion to find.

        Returns:
            Element: The matching Element enum member.

        Raises:
            ValueError: If no element with the given name is found.
        """
        try:
            return cls(name)
        except ValueError:
            raise ValueError(f"No element found with name '{name}'")


@enum.unique
class Layers(enum.Enum):
    """
    Layers used in perovskite solar cells.
    """

    @property
    def layer_name(self):
        return self.value[0]

    SLG = "SLG"
    FTO = "FTO"
    ITO = "ITO"
    TIO2_C = "TiO2-c"
    SNO2_NP = "SnO2-np"
    TIO2_MP = "TiO2-mp"
    PEROVSKITE = "Perovskite"
    SPIRO_MEOTAD = "Spiro-MeOTAD"
    AU = "Au"
    AG = "Ag"


@enum.unique
class Site(enum.Enum):
    """
    Perovskite sites
    """
    A = "A"
    B = "B"
    C = "C"


@enum.unique
class CellArchitecture(enum.Enum):
    """
    Cell architecture
    """

    NIP = "nip"
    PIN = "pin"


@enum.unique
class BackContact(enum.Enum):
    """
    Back contact stacks
    """

    Au = "Au"
    Ag = "Ag"


@enum.unique
class SpaceGroup(enum.Enum):
    """
    Spacegroups of perovskite materials.
    """

    RUDDLESDEN_POPEN = "I4/mmm"
    CUBIC = "Pm3m"
    TETRAGONAL = "I4/mcm"
    ORTHOROMBIC = "Pnma"
    HEXAGONAL = 'P6/mmc'


class Dimensions(enum.Enum):
    """
    Dimensions of perovskite materials.
    """

    ZERO_DIM = "0D"
    TWO_DIM = "2D"
    THREE_DIM = "3D"
    TWO_THREE_DIM_MIXTURE = "2D3D_mixture"


@enum.unique
class ETLStacks(enum.Enum):
    """
    ETL Stacks
    """
    
    TWO_TI_O2_c_mp = "TiO2-c | TiO2-mp"
    TI_O2_c = "TiO2-c"
    PCBM_60 = "PCBM-60"
    PCBM_60_BCP = "PCBM-60 | BCP"
    SN_O2_np = "SnO2-np"
    SN_O2_c = "SnO2-c"
    C60_BCP = "C60 | BCP"


@enum.unique
class StabilityProtocol(enum.Enum):
    """
    Stability protocols
    """

