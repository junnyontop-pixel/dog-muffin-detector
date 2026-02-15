import cv2
import numpy as np
import joblib
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import io

app = FastAPI()

# 1. 모델 미리 로드 (서버 켤 때 딱 한 번만!)
try:
    data = joblib.load('dog_muffin_model.pkl')
    model = data['model']
    categories = data['categories']
    print("✅ AI 모델 로드 완료!")
except:
    print("❌ 모델 파일을 찾을 수 없습니다.")

@app.post("/predict")
async def predict_api(file: UploadFile = File(...)):
    # 2. 업로드된 파일 읽기
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        return JSONResponse(content={"error": "유효하지 않은 이미지입니다."}, status_code=400)

    # 3. 전처리 (학습할 때와 동일하게 64x64)
    img_resized = cv2.resize(img, (64, 64))
    img_flatten = img_resized.flatten() / 255.0
    img_input = img_flatten.reshape(1, -1)

    # 4. AI 판독
    prediction = model.predict(img_input)[0]
    proba = model.predict_proba(img_input)[0]
    
    result = categories[prediction]
    confidence = float(proba[prediction] * 100)

    return {
        "result": result,
        "confidence": f"{confidence:.2f}%",
        "message": f"이 사진은 {confidence:.2f}% 확률로 {result}입니다!"
    }

if __name__ == "__main__":
    import uvicorn
    # 코드스페이스 환경에서는 0.0.0.0으로 열어야 외부 접속이 가능해
    uvicorn.run(app, host="0.0.0.0", port=8000)