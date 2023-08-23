# 2023 임베디드 SW 경진대회
* 팀명: Carisma
* 주제: 비행기 수하물 적재 시스템

# H/W Used
* Jetson TX2
    * Jetpack 3.3.1 
* OpenCR
    * OpenManipulator 
* Arduino Uno
    * <a href="https://ideaplay6173.cafe24.com/product/%EC%BB%A8%EB%B2%A0%EC%9D%B4%EC%96%B4%EB%B2%A8%ED%8A%B8-%ED%8A%B9%EB%8C%80%ED%98%95%EC%95%84%EB%91%90%EC%9D%B4%EB%85%B8%EC%82%AC%EC%9A%A9-100-200mm/370/"> 컨베이어 벨트 키트 </a>

# Technologies Used
- OpenCV == 4.8.0.74
- matplotlib == 3.7.1
- numpy == 1.24.3
- pyzbar == 0.1.9
- pyserial == 3.5

# How to use
1. code를 복사합니다.
```console
git clone https://github.com/wonchan-lee/embedded-SW.git
```
2. Technologies Used에 사용된 library를 다운로드 합니다.
```console
pip install opencv-python matplotlib numpy pyzbar pyserial
```
3. Arduino Uno에 arduino_uno_code 폴더 속 코드를 업로드 합니다.
4. OpenCR에 open_cr_code 폴더 속 코드를 업로드 합니다. 
5. host PC에 Arduino와 OpenCR을 Serial로 연결합니다.
6. main.py 속 Arduino Uno와 OpenCR과 연결하는 Serial 객체들의 Port 번호를 host PC에 연결된 포트로 변경합니다.
7. main.py를 실행합니다.
   * cv2.VideoCapture(0)으로 변경하면 우선순위가 높은 카메라를 사용할 수 있습니다.
