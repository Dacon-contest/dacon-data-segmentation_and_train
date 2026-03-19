import os
import shutil
from pathlib import Path
from tqdm import tqdm

# 1. 경로 설정 (윈도우 경로이므로 r"" 사용)
SRC_DIR = Path(r"C:\kdy\Dacon\data")
DST_DIR = Path(r"C:\kdy\Dacon\no_seg_data") # 새롭게 정리될 최상위 폴더

splits = ['train', 'dev', 'test']
# 폴더명 매핑 (원본 파일명 : 새로 만들 폴더명)
file_types = {
    'front.png': 'front',
    'top.png': 'top',
    'simulation.mp4': 'mp4'
}

for split in splits:
    split_path = SRC_DIR / split
    if not split_path.exists():
        continue
        
    print(f"🔄 [{split}] 데이터 재배치 시작...")
    
    # 목적지 폴더 미리 생성 (ex: .../train/front)
    for target_folder in file_types.values():
        (DST_DIR / split / target_folder).mkdir(parents=True, exist_ok=True)
        
    # 각 ID 폴더 순회 (예: TRAIN_0001)
    id_folders = sorted([f for f in split_path.iterdir() if f.is_dir()])
    
    for id_folder in tqdm(id_folders):
        id_name = id_folder.name # 'TRAIN_0001'
        
        for file_name, target_folder in file_types.items():
            src_file = id_folder / file_name
            
            if src_file.exists():
                ext = src_file.suffix # .png 또는 .mp4
                
                # CSV 파일과 매칭하기 쉽게 ID 자체를 파일명으로 사용
                # 결과: .../train/front/TRAIN_0001.png
                new_file_name = f"{id_name}{ext}"
                dst_file = DST_DIR / split / target_folder / new_file_name
                
                # 복사 수행
                shutil.copy2(src_file, dst_file)

print("✅ 모든 파일 폴더별 분리 및 복사 완료!")