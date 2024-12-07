from dotenv import load_dotenv
import os

load_dotenv()

OPENART_BASE_URL = "https://openart.ai/api/search"
PIXLR_BASE_URL = "https://pixlr.com/api/image-generator/feeds/popular"
FREEPIK_BASE_URL = "https://www.freepik.com/api/regular/search"

COLLECTED_DIR = os.getenv('SCRAPPING_DIR',"collected")
DATASET_DIR = os.getenv('DATASET_DIR',"dataset")

CONSIDER_MAX_ITERATON = os.getenv('CONSIDER_MAX_ITERATON',"1")
MAX_ITERATON = int(os.getenv('MAX_ITERATON',5))

DOWNLOAD_BATCH = int(os.getenv('DOWNLOAD_BATCH',100))
EPOCH = int(os.getenv('EPOCH',10))

TRY_MANY = int(os.getenv('TRY_MANY',3))
WATING = os.getenv('WATING',"1")

SEARCH_PROMPTS = os.getenv('SEARCH_PROMPTS',"")

PLATFORMS: list[str] = os.getenv('PLATFORMS', "").split(",")

PIXLR_MAX_ITERATON = int(os.getenv('PIXLR_MAX_ITERATON',50))
