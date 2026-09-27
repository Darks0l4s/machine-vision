import cv2
import face_recognition
import numpy as np
import re
import time

with open("encod.txt", 'r', encoding='utf-8') as f:
    content = f.read()

pattern = r'([^:]+):\[(.*?)\]'
matches = re.findall(pattern, content, re.DOTALL)

known_names = []
known_embeddings = []

for name, numbers_str in matches:
    emb = np.array([float(x) for x in numbers_str.split()])
    known_names.append(name.strip())
    known_embeddings.append(emb)

video = cv2.VideoCapture(0)

k = 10
frame_count = 0

face_locations = []
face_names = []

prev_time = time.time()
fps = 0

while True:
    ret, frame = video.read()
    if not ret:
        break

    frame_count += 1

    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    if frame_count % k == 0:
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        face_names = []

        for face_emb in face_encodings:
            name = "Unknown"

            if len(known_embeddings) > 0:
                distances = face_recognition.face_distance(known_embeddings, face_emb)
                best_match_index = np.argmin(distances)

                if distances[best_match_index] < 0.5:
                    name = known_names[best_match_index][:-6]

            face_names.append(name)

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        color = (0, 200, 0) if name != "Unknown" else (0, 0, 200)

        cv2.rectangle(frame, (left, top), (right, bottom), color, 3)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    cv2.putText(frame, f"FPS: {int(fps)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Video", frame)

    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()