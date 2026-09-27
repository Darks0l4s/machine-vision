import cv2
import numpy as np
import re

def normalize_face(face):
    """Нормализация лица: фиксированный размер + выравнивание освещения"""
    # Фиксированный размер (убирает зависимость от расстояния)
    face = cv2.resize(face, (128, 128))
    
    # CLAHE (адаптивное выравнивание гистограммы) - борется с освещением
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    face = clahe.apply(face)
    
    # Нормализация контраста
    face = cv2.normalize(face, None, 0, 255, cv2.NORM_MINMAX)
    
    return face

def get_face_embedding_fixed(img):
    """Извлечение признаков, НЕ зависящих от расстояния"""
    if img is None or img.size == 0:
        return None
    
    try:
        # 1. Нормализуем лицо (убираем зависимость от расстояния)
        face = normalize_face(img)
        
        # 2. Используем LBP (Local Binary Patterns) - устойчив к масштабу и освещению
        from skimage.feature import local_binary_pattern
        
        radius = 2
        n_points = 8 * radius
        lbp = local_binary_pattern(face, n_points, radius, method='uniform')
        
        # Гистограмма LBP (инвариантна к масштабу)
        n_bins = n_points + 2
        hist, _ = np.histogram(lbp.ravel(), bins=n_bins, range=(0, n_bins))
        hist = hist.astype("float")
        hist /= (hist.sum() + 1e-6)
        
        return hist
        
    except Exception as e:
        print(f"LBP error: {e}")
        return None

def get_face_embedding_orb(img):
    """Используем ORB дескрипторы - устойчивы к масштабу и повороту"""
    if img is None or img.size == 0:
        return None
    
    try:
        # Нормализуем размер
        face = normalize_face(img)
        
        # ORB детектор
        orb = cv2.ORB_create(nfeatures=100)
        
        # Находим ключевые точки и дескрипторы
        keypoints, descriptors = orb.detectAndCompute(face, None)
        
        if descriptors is None or len(descriptors) == 0:
            return None
        
        # Усредняем дескрипторы для получения фиксированного вектора
        mean_descriptor = np.mean(descriptors, axis=0)
        
        # Нормализуем
        norm = np.linalg.norm(mean_descriptor)
        if norm > 0:
            return mean_descriptor / norm
        return mean_descriptor
        
    except Exception as e:
        print(f"ORB error: {e}")
        return None

# Выбираем метод (LBP проще и стабильнее)
try:
    from skimage.feature import local_binary_pattern
    get_face_embedding = get_face_embedding_fixed
    print("✅ Используем LBP метод")
except ImportError:
    get_face_embedding = get_face_embedding_orb
    print("✅ Используем ORB метод")
    print("Для лучшего результата установите: pip install scikit-image")

# Инициализация камеры
video = None
camera_indexes = [0, 1, 2]

for idx in camera_indexes:
    print(f"Пробуем открыть камеру {idx}...")
    test_video = cv2.VideoCapture(idx)
    if test_video.isOpened():
        video = test_video
        print(f"✅ Камера {idx} открыта!")
        break
    else:
        test_video.release()

if video is None:
    print("❌ Не удалось открыть камеру!")
    exit()

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Загружаем эталонные эмбеддинги
try:
    with open("encod.txt", 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print("❌ Файл encod.txt не найден!")
    exit()

pattern = r'([^:]+):\[(.*?)\]'
matches = re.findall(pattern, content, re.DOTALL)

reference_embeddings = []
reference_names = []
for image_name, numbers_str in matches:
    try:
        embedding = np.array([float(x) for x in numbers_str.split()])
        reference_embeddings.append(embedding)
        name = image_name.strip().split(':')[0]
        reference_names.append(name)
    except Exception as e:
        print(f"Ошибка загрузки {image_name}: {e}")

print(f"✅ Загружено {len(reference_embeddings)} эталонов")

# Параметры распознавания
DISTANCE_THRESHOLD = 0.5  # Более строгий порог для LBP
MIN_FACE_SIZE = 80

while True:
    good, img = video.read()
    if not good:
        break
    
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(img_gray, 1.1, 5, minSize=(MIN_FACE_SIZE, MIN_FACE_SIZE))
    
    for x, y, w, h in faces:
        margin = int(0.1 * w)
        x1 = max(0, x - margin)
        y1 = max(0, y - margin)
        x2 = min(img.shape[1], x + w + margin)
        y2 = min(img.shape[0], y + h + margin)
        
        face_roi = img_gray[y1:y2, x1:x2]
        
        if face_roi.shape[0] < MIN_FACE_SIZE or face_roi.shape[1] < MIN_FACE_SIZE:
            cv2.rectangle(img, (x,y), (x+w, y+h), (100, 100, 100), 2)
            continue
        
        current_emb = get_face_embedding(face_roi)
        
        if current_emb is not None:
            best_match = None
            best_distance = float('inf')
            
            for idx, ref_emb in enumerate(reference_embeddings):
                min_len = min(len(current_emb), len(ref_emb))
                if min_len > 0:
                    # Используем косинусное расстояние (лучше для признаков)
                    dot_product = np.dot(current_emb[:min_len], ref_emb[:min_len])
                    cos_sim = dot_product / (np.linalg.norm(current_emb[:min_len]) * np.linalg.norm(ref_emb[:min_len]) + 1e-6)
                    distance = 1 - cos_sim  # Превращаем схожесть в расстояние
                    
                    if distance < best_distance:
                        best_distance = distance
                        best_match = idx
            
            if best_match is not None and best_distance < DISTANCE_THRESHOLD:
                name = reference_names[best_match]
                confidence = max(0, (1 - best_distance) * 100)
                
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
                cv2.putText(img, f"{name} ({confidence:.1f}%)", (x, y-10), 
                           cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
            else:
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)
                cv2.putText(img, f"Unknown ({best_distance:.2f})", (x, y-10), 
                           cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255), 1)
    
    cv2.imshow("Face Recognition", img)
    
    key = cv2.waitKey(30) & 0xFF
    if key == ord('q') or key == 27:
        break

video.release()
cv2.destroyAllWindows()