from typing import Dict
from config import FREEPIK_BASE_URL, OPENART_BASE_URL, PIXLR_BASE_URL, PIXLR_MAX_ITERATON
from .api_base import APIBase
from .openart_api import OpenArtAPI
from .freepik_api import FreepikAPI
from .pixlr_api import PixlrAPI

SUPPORTED_PLATFORM: Dict[str, APIBase] = {
    "openart": OpenArtAPI(base_url=OPENART_BASE_URL),
    "freepik": FreepikAPI(base_url=FREEPIK_BASE_URL),   
    "pixlr": PixlrAPI(base_url=PIXLR_BASE_URL, max_iteration=PIXLR_MAX_ITERATON),
}
