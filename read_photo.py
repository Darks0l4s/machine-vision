import re

def process_embeddings_file(filename):
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'([^:]+):\[(.*?)\]'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for i, (image_name, numbers_str) in enumerate(matches, 1):
        # Преобразуем в список чисел
        embedding = [float(x) for x in numbers_str.split()]
        
        print(f"\n{'='*50}")
        print(f"Блок {i}: {image_name.strip()}")
        print(f"{'='*50}")
        print(f"Данные: {embedding}")

process_embeddings_file("encod.txt")