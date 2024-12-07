from typing import Dict
from config import FREEPIK_BASE_URL, OPENART_BASE_URL, PIXLR_BASE_URL, PIXLR_MAX_ITERATON
from .api_base import BasePlatform
from .openart_api import OpenartPlatform
from .freepik_api import FreepikPlatform
from .pixlr_api import PixlrPlatform

SUPPORTED_PLATFORM: Dict[str, BasePlatform] = {
    "openart": OpenartPlatform(base_url=OPENART_BASE_URL),
    "freepik": FreepikPlatform(base_url=FREEPIK_BASE_URL),   
    "pixlr": PixlrPlatform(base_url=PIXLR_BASE_URL, max_iteration=PIXLR_MAX_ITERATON),
}
