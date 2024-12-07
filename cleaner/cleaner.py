from collector import APIBase
import os
import pandas as pd
from datetime import datetime
from config import COLLECTED_DIR

def concatenate_files(collector: APIBase):
    dir_path = collector.dir()
    
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        print(f"Cleaning directory: {dir_path}")
        combined_data = pd.DataFrame()
        files_to_delete = []
        
        files = os.listdir(dir_path)
        
        for file in files:
            file_path = os.path.join(dir_path, file)
            
            if file.endswith('.csv'):
                try:
                    df = pd.read_csv(file_path)
                    print(f"Processing file: {file_path}")
                    combined_data = pd.concat([combined_data, df], ignore_index=True)
                    files_to_delete.append(file_path)
                
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
        
        if not combined_data.empty:
            time = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            output_file = os.path.join(COLLECTED_DIR, f"{collector.name()}_data_{time}.csv")
            
            try:
                combined_data.to_csv(output_file, index=False)
                print(f"Combined data saved to {output_file}")
                
                # Delete the files
                for file_path in files_to_delete:
                    try:
                        os.remove(file_path)
                        print(f"Deleted file: {file_path}")
                    except Exception as e:
                        print(f"Error deleting file {file_path}: {e}")
            
            except Exception as e:
                print(f"Error saving combined data to {output_file}: {e}")
        else:
            print("No data to combine.")
    else:
        print(f"Directory does not exist: {dir_path}")

def remove_repeated():
    files = os.listdir(COLLECTED_DIR)
    for file_name in files:
        file_path = os.path.join(COLLECTED_DIR, file_name)
        
        if file_name.endswith('.csv'):
            try:
                df = pd.read_csv(file_path)
                origin_size = df.shape[0]
                print(f"[CLEANING] {file_name}")

                # Remove duplicates based on the 'id' column
                if 'id' in df.columns:
                    df_unique = df.drop_duplicates(subset='id')
                    print(f"[UPDATE] [REMOVE] [{origin_size - df_unique.shape[0]}] rows")

                    # Save the cleaned data back to the same file
                    df_unique.to_csv(file_path, index=False)
                else:
                    print(f"[400] 'id' column not found in {file_name}, skipping...")
            except Exception as e:
                print(f"[ERROR] {file_name}: {e}")
