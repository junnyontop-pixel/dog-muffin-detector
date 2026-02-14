from gradio_client import Client, handle_file

# 1. 네 Space 주소로 클라이언트 연결
client = Client("ayj8201/dog-muffin-detector")

def get_ai_prediction(image_path):
    # 2. 이미지 전송 및 예측 요청
    result = client.predict(
        img=handle_file(image_path),
        api_name="/predict"
    )
    
    # 3. 결과 출력
    print(f"🤖 판독 결과: {result}")
    return result

get_ai_prediction("./test.png")