import streamlit as st
import cv2
import mediapipe as mp
import os

def upload_files(key):
    uploaded_files = st.sidebar.file_uploader(
        "Выберите видео для обработки", type=["mp4", "MOV", "mov"], accept_multiple_files=True, key=key)
    if uploaded_files:
        st.markdown(f"_Выбрано файлов: {len(uploaded_files)}_")

    return uploaded_files

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Функция для обработки видео
def process_MP(video_file):
    # Инициализация Pose
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
    
    cap = cv2.VideoCapture(video_file)
    stframe = st.empty()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Конвертация изображения в RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # Обработка изображения с помощью MediaPipe
        results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Отрисовка точек на изображении
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Отображение обработанного изображения в Streamlit
        stframe.image(image, channels="BGR", use_column_width=True)

    cap.release()

def PD_process(config):
    uploaded_files = upload_files('PD_process')
    if uploaded_files:
        with open("temp_video.mp4", "wb") as f:
            f.write(uploaded_files[0].getbuffer())
        process_MP("temp_video.mp4")
    if os.path.exists("temp_video.mp4"):
    
        os.remove("temp_video.mp4")