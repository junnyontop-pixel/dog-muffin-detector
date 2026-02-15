import cv2
import numpy as np
import joblib
import sys

def predict():
    # 1. 저장된 모델 불러오기
    try:
        data = joblib.load('dog_muffin_model.pkl')
        model = data['model']
        categories = data['categories']
    except:
        print("❌ 모델 파일을 찾을 수 없어!")
        return

    # 2. 테스트할 이미지 경로 입력
    img_path = input("검사할 사진 경로를 입력해 (예: data/dog/0.jpg): ")
    
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("❌ 사진을 불러올 수 없어. 경로를 확인해줘.")
        return

    # 3. 전처리 (학습할 때랑 똑같이!)
    img_resized = cv2.resize(img, (64, 64))
    img_flatten = img_resized.flatten() / 255.0
    img_input = img_flatten.reshape(1, -1)

    # 4. 예측
    prediction = model.predict(img_input)[0]
    proba = model.predict_proba(img_input)[0] # 확률 확인

    result = categories[prediction]
    confidence = proba[prediction] * 100

    print("\n" + "="*30)
    print(f"🤖 AI의 판단: 이건 [{result}] 입니다!")
    print(f"📊 확신도: {confidence:.2f}%")
    print("="*30)

if __name__ == "__main__":
    predict()