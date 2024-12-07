import requests
from collector import BasePlatform
from config import PIXLR_MAX_ITERATON

class PixlrPlatform(BasePlatform):
    def __init__(self, base_url: str, max_iteration: int):
        super().__init__(base_url, by_query=False, max_iteration=max_iteration)
        self.page = 1
        
    def reset(self):
        self.page = 1

    def next(self):
        self.page = self.page + 1

    def _fetch_data(self):
        print(self.base_url + f"/{self.page}")
        response = requests.get(self.base_url + f"/{self.page}")
        response.raise_for_status()
        return response.json()
    
    def name(self):
        return "pixlr"

    def _parse_data(self, json_response):
        data_list = []
        items = json_response.get("data", {}).get("docs", [])
        for item in items:
            data_list.append({
                "id": item.get("primary"),
                "description": self._clean_text(item.get("prompt", "")),
                "image_web": item.get("images", [])[0].get("preview"),
                "image_url": item.get("images", [])[0].get("medium"),
                "width": item.get("width"),
                "height": item.get("height"),
            })
        return data_list
