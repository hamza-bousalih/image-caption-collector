import requests
from collector import APIBase

class OpenArtAPI(APIBase):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.cursor = 0

    def reset(self):
        self.cursor = 0

    def next(self):
        self.cursor = self.cursor + 100
    
    def _fetch_data(self):
        params = {
            "query": self.query,
            "cursor": self.cursor,
            "method": "prompt",
            "apply_filter": "true",
        }
        print(self.base_url, f"params {params}", sep=" :: ")
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json()
    
    def name(self):
        return "openart"

    def _parse_data(self, json_response):
        data_list = []
        for item in json_response.get("items", []):
            data_list.append({
                "id": item.get("id"),
                "description": self._clean_text(item.get("prompt", "")),
                "image_url": item.get("image_url"),
                "image_web": item.get("image", {}).get("url"),
                "title": self._clean_text(item.get("title", "")),
                "width": item.get("image_width"),
                "height": item.get("image_height"),
            })
        return data_list
