import os
import cv2
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import joblib

def train_ai():
    X = []
    y = []
    categories = ['dog', 'muffin']
    base_path = 'data' # data 폴더 경로 확인!

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
                img = cv2.imread(img_path)
                if img is None: continue
                
                img = cv2.resize(img, (64, 64))
                X.append(img.flatten() / 255.0)
                y.append(idx)
                
                # 10개마다 진행 상황 출력
                if (i + 1) % 10 == 0:
                    print(f"   ㄴ {cat} 이미지 변환 중... ({i+1}/{len(file_list)})")
            except:
                continue

    if len(X) == 0:
        print("❌ 학습할 데이터가 없습니다. data 폴더를 확인해주세요!")
        return

    X = np.array(X)
    y = np.array(y)

    print("\n🧠 [2/3] 모델 학습을 시작합니다. (데이터가 많으면 여기서 좀 걸려요!)")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # SVC 학습 (여기서 CPU를 많이 써서 팬 소리가 날 수도 있어!)
    model = SVC(kernel='linear', probability=True)
    model.fit(X_train, y_train)

    print("✅ [3/3] 학습 완료! 성능 검사 중...")
    score = model.score(X_test, y_test)
    print(f"🎯 정확도: {score * 100:.2f}%")

    joblib.dump({'model': model, 'categories': categories}, 'dog_muffin_model.pkl')
    print("💾 'dog_muffin_model.pkl' 저장 완료!")

if __name__ == "__main__":
    train_ai()