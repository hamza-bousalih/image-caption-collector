from typing import List, Tuple
from cleaner import concatenate_files
from collector import SUPPORTED_PLATFORM, BasePlatform
from config import SEARCH_PROMPTS, PLATFORMS

search_prompts = SEARCH_PROMPTS.split(";")

def filter_platforms() -> Tuple[List[BasePlatform], List[BasePlatform]]:
    global PLATFORMS
    
    queried_platforms: List[BasePlatform] = []
    simple_platforms: List[BasePlatform] = []

    if len(PLATFORMS) == 0:
        raise RuntimeError("[400] no platform was provided! out")

    for p in PLATFORMS:
        pla = SUPPORTED_PLATFORM[p]
        if pla is None and isinstance(pla, BasePlatform):
            print(f"[400] {p} is not supported")
            continue
        
        if pla.by_query: queried_platforms.append(pla)
        else: simple_platforms.append(pla)
    
    return queried_platforms, simple_platforms

def collect_by_query(api: BasePlatform, q: str):
    api.reset()
    api.set_query(q)
    api.execute()

def collect_simple(api: BasePlatform):
    api.reset()
    api.execute()

if __name__ == "__main__":
    print("=" * 50)
    print(search_prompts)
    print("=" * 50)
    
    quired, simple = filter_platforms()
    
    for p in quired:
        for q in search_prompts:
            if len(q) == 0:
                continue
            collect_by_query(p, q)
        concatenate_files(p)

    for p in simple:
        collect_simple(p)
        concatenate_files(p)

