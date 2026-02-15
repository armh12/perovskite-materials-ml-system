from typing import Tuple

import pandas as pd

from ml_prediction_web_service.entities.dictionary import Element, SpaceGroup, Site, Dimension


def calculate_effective_radii_for_site(row: pd.Series, site: Site) -> float:
    input_dict = row.to_dict()
    r_eff = 0.
    sites = [key for key in input_dict if key.startswith(f'{site.value}_') and not key.endswith("_coef")]
    
    for _site in sites:
        element_name = input_dict[_site]
        if element_name is None or pd.isna(element_name):
            continue
        coef = float(input_dict[f'{_site}_coef'])
        if _site.startswith(site.value):
            coef = coef / 3.0
        element_entity = Element.get_element_by_name(element_name)       
        r_eff += coef * element_entity.ionic_radii
        
    return r_eff


def compute_dimensionality_indicator(r_a_eff: float) -> int:
    """
    Compute the dimensionality indicator (1 for 2D if r_A_eff > 3.0, 0 for 3D).
    Returns:
        int: Dimensionality indicator (1 or 0).
    """
    return 1 if r_a_eff > 3.0 else 0


def compute_ionic_radius_ratios(r_A_eff: float, r_B: float, r_C_eff: float) -> Tuple[float, float]:
    """
    Compute additional ionic radius ratios.

    Args:
        r_A_eff (float): Effective A-site radius.
        r_B (float): B-site radius.
        r_C_eff (float): Effective C-site radius.

    Returns:
        Tuple[float, float]: (r_A_eff/r_C_eff, r_B/r_A_eff)
    """
    r_A_to_C = r_A_eff / r_C_eff if r_C_eff != 0 else float('inf')
    r_B_to_A = r_B / r_A_eff if r_A_eff != 0 else float('inf')
    return r_A_to_C, r_B_to_A


def compute_space_group(tolerance_factor: float, dimension: float, is_inorganic: bool) -> str | None:
    if pd.isna(tolerance_factor):
        return pd.NA

    # 3D Perovskites
    if dimension == Dimension.THREE_DIM.nm:
        if 0.9 <= tolerance_factor <= 1.0:
            return SpaceGroup.CUBIC.nm  # Cubic
        elif 0.8 <= tolerance_factor < 0.9:
            return SpaceGroup.ORTHOROMBIC.nm if is_inorganic else SpaceGroup.TETRAGONAL.nm  # Orthorhombic or tetragonal
        elif tolerance_factor < 0.8:
            return SpaceGroup.ORTHOROMBIC.nm  # Orthorhombic
        else:  # t > 1.0
            return SpaceGroup.HEXAGONAL.nm  # Hexagonal

    # 2D Perovskites
    elif dimension == Dimension.TWO_DIM.nm:
        return SpaceGroup.RUDDLESDEN_POPEN.nm  # Layered structure

    # 2D3D Mixture
    elif dimension == Dimension.TWO_THREE_DIM_MIXTURE.nm:
        return SpaceGroup.RUDDLESDEN_POPEN.nm if tolerance_factor < 0.9 else SpaceGroup.ORTHOROMBIC.nm
    # 0D Perovskites
    elif dimension == Dimension.ZERO_DIM.nm:
        return 'Unknown'  # Often molecular, not well-defined

