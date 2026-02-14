# 🐶 Chihuahua vs Muffin Detector 🧁

> 셀레니움 이미지 크롤링부터 사이킷런 머신러닝 학습, 그리고 Hugging Face 배포까지 완료한 AI 프로젝트입니다.

## 🚀 프로젝트 개요
치와와와 머핀의 시각적 유사성을 머신러닝으로 구분해내는 인공지능 서비스입니다. 65.00%의 초기 정확도로 시작하여 지속적으로 데이터를 업데이트하고 있습니다.

## 🛠 Tech Stack
- **Language**: Python
- **Libraries**: Selenium, Scikit-learn, OpenCV, Joblib, Gradio
- **Deployment**: Hugging Face Spaces

## 📖 사용 방법
### 1. 이미지 수집
```bash
python collector.py
```

### 2. 모델 학습
```bash
python main.py
```

### 3. API 호출 테스트
```python
from gradio_client import Client, handle_file
client = Client("ayj8201/dog-muffin-detector")
result = client.predict(img=handle_file('test.png'), api_name="/predict")
print(result)
```

## 🔗 Demo
[Hugging Face Space 바로가기](https://huggingface.co/spaces/ayj8201/dog-muffin-detector)
