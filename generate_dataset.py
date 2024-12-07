import time
import requests
import os
import pandas as pd
from cleaner import remove_repeated
from config import COLLECTED_DIR, DATASET_DIR, DOWNLOAD_BATCH, EPOCH, WATING

def download_images(file_name: str, epoch: int):
    file_path = os.path.join(COLLECTED_DIR, file_name)
    images_dir = os.path.join(DATASET_DIR, 'images')
    os.makedirs(images_dir, exist_ok=True)

    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading {file_name}: {e}")
        return

    downloaded_ids = []
    download_count = 0

    for _, row in df.iterrows():
        if download_count >= DOWNLOAD_BATCH:
            print(f"[STOP] Reached max download limit of {DOWNLOAD_BATCH}.")
            break

        step_msg = f"epoch {epoch}/{EPOCH} | {download_count + 1}/{DOWNLOAD_BATCH}"

        image_url = row['image_url']
        id = row['id']
        platform = row['platform']
        image_name = platform + "_" + str(id)
        image_path_dir = os.path.join(images_dir, platform)
        image_path = os.path.join(image_path_dir, f"{image_name}.png")

        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()

            os.makedirs(image_path_dir, exist_ok=True)
            with open(image_path, 'wb') as file:
                file.write(response.content)
            print(f"[DOWNLOADED] [{step_msg}] [{image_name}] {image_url}")
            downloaded_ids.append(id)
            download_count += 1
        except requests.exceptions.RequestException as e:
            print(f"[FAILED] [{platform}] [{id}] {image_url}: {e}")
            continue
        
        # if (WATING == "1" and download_count % DOWNLOAD_BATCH == 0):
        #     print(f"[WAIT] wating 5s ...")
        #     time.sleep(5)

    # Save the list of downloaded IDs
    if downloaded_ids:
        downloaded_csv = os.path.join(DATASET_DIR, file_name)
        combined_df = df[df['id'].isin(downloaded_ids)]

        if os.path.exists(downloaded_csv):
            existing_df = pd.read_csv(downloaded_csv)
            combined_df = pd.concat([combined_df, existing_df])

        combined_df.to_csv(downloaded_csv, index=False)
        print(f"[UPDATE] [ADD] {downloaded_csv}")

    # Update the original CSV
    if downloaded_ids:
        remaining_df = df[~df['id'].isin(downloaded_ids)]
        if not remaining_df.empty:
            remaining_df.to_csv(file_path, index=False)
            print(f"[UPDATE] [REMOVE] [{df.shape[0] - remaining_df.shape[0]}] {file_path}")
        else:
            os.remove(file_path)
            print(f"[DELETE] {file_path}")

def main():
    if not os.path.exists(COLLECTED_DIR):
        print(f"[404] {COLLECTED_DIR}")
        return

    print("-" * 50)
    remove_repeated()
    print("-" * 50)
    print("-" * 50)
    print("-" * 50)

    for epoch in range(1, EPOCH + 1, 1):
        print(f"[EPOCH] {epoch}/{EPOCH}")
        for file_name in os.listdir(COLLECTED_DIR):
            if file_name.endswith('.csv'):
                print("-" * 50)
                print(f"[FILE] {file_name}")
                download_images(file_name, epoch)
                print("-" * 50)

if __name__ == "__main__":
    main()
