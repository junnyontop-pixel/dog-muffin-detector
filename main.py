import os
import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier # 1. 모델 변경 (SVC 대신 이거!)
from sklearn.model_selection import train_test_split
import joblib

def train_ai():
    X = []
    y = []
    categories = ['dog', 'muffin']
    base_path = 'data' 

    print("🚀 [1/3] 이미지 데이터를 불러오는 중입니다...")
    
    for idx, cat in enumerate(categories):
        path = os.path.join(base_path, cat)
        if not os.path.exists(path):
            print(f"⚠️ 폴더가 없어요: {path}")
            continue
            
        file_list = os.listdir(path)
        print(f"📂 {cat} 폴더에서 {len(file_list)}개의 파일을 찾았습니다.")
        
        for i, img_name in enumerate(file_list):
            try:
                img_path = os.path.join(path, img_name)
                # BGR이 아니라 그레이스케일(흑백)로 읽어서 형태에 집중하게 만들기
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is None: continue
                
                img = cv2.resize(img, (64, 64))
                # 2. 정규화와 플래기(1차원화)를 동시에!
                X.append(img.flatten() / 255.0)
                y.append(idx)
                
                if (i + 1) % 10 == 0:
                    print(f"   ㄴ {cat} 이미지 변환 중... ({i+1}/{len(file_list)})")
            except:
                continue

    if len(X) == 0:
        print("❌ 학습할 데이터가 없습니다.")
        return

    X = np.array(X)
    y = np.array(y)

    print("\n🧠 [2/3] RandomForest 모델 학습을 시작합니다! (나무 100그루 심는 중...)")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. 모델 교체: 나무 100그루가 투표해서 결정하는 방식이야
    model = RandomForestClassifier(n_estimators=100, max_depth=12, random_state=42)
    model.fit(X_train, y_train)

    print("✅ [3/3] 학습 완료! 성능 검사 중...")
    score = model.score(X_test, y_test)
    print(f"🎯 새로운 정확도: {score * 100:.2f}%")

    joblib.dump({'model': model, 'categories': categories}, 'dog_muffin_model.pkl')
    print("💾 업그레이드된 'dog_muffin_model.pkl' 저장 완료!")

if __name__ == "__main__":
    train_ai()