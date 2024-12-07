import requests
from collector import APIBase

class FreepikAPI(APIBase):
    def __init__(self, base_url):
        super().__init__(base_url)
        self.page = 1
        
    def reset(self):
        self.page = 1

    def next(self):
        self.page = self.page + 1

    def _fetch_data(self):
        params = {
            "filters[license]": "free",
            "locale": "en",
            "term": self.query,
            "page": self.page,
        }
        print(self.base_url, f"params {params}", sep=" :: ")
        response = requests.get(self.base_url, cookies=self.cookies, params=params)
        response.raise_for_status()
        return response.json()
    
    def name(self):
        return "freepik"

    def _parse_data(self, json_response):
        data_list = []
        for item in json_response.get("items", []):
            data_list.append({
                "id": item.get("id"),
                "description": self._clean_text(item.get("name", "")),
                "image_url": item.get("preview", {}).get("url"),
                "image_web": item.get("preview", {}).get("url"),
                "width": item.get("image", {}).get("width"),
                "height": item.get("image", {}).get("height"),
            })
        return data_list
