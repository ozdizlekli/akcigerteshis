import gradio as gr
import tensorflow as tf
import numpy as np
from PIL import Image

# 1. Modeli ve etiketleri yükle
# Bu kod, uygulama başlarken sadece bir kez çalışır.
print("Model yükleniyor...")
model = tf.keras.models.load_model('akciger_modeli_v2_7packs.keras')
print("Model başarıyla yüklendi.")

# Projemizdeki 14 hastalık etiketini buraya yazalım
labels = [
    'Atelectasis', 'Cardiomegaly', 'Consolidation', 'Edema', 'Effusion', 
    'Emphysema', 'Fibrosis', 'Hernia', 'Infiltration', 'Mass', 'Nodule', 
    'Pleural_Thickening', 'Pneumonia', 'Pneumothorax'
]

# 2. Tahmin fonksiyonunu tanımla
# Bu fonksiyon, kullanıcı bir resim yüklediğinde çalışır.
def predict_xray(input_image: Image.Image):
    """
    Girdi olarak bir görüntü alır, modeli çalıştırır ve
    hastalık olasılıklarını bir sözlük olarak döndürür.
    """
    # Görüntüyü modelin istediği formata getir (224x224, ölçeklenmiş)
    img = input_image.resize((224, 224))
    img_array = np.array(img)
    
    # Görüntü siyah-beyaz ise 3 kanala dönüştür
    if len(img_array.shape) == 2:
        img_array = np.stack([img_array] * 3, axis=-1)

    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Tahmin yap
    predictions = model.predict(img_array)
    
    # Sonuçları etiketlerle eşleştirip bir sözlük oluştur
    # Gradio'nun Label bileşeni bu formatı çok sever
    results = {labels[i]: float(predictions[0][i]) for i in range(len(labels))}
    
    return results

# 3. Gradio arayüzünü oluştur
iface = gr.Interface(
    fn=predict_xray,
    inputs=gr.Image(type="pil", label="Akciğer Röntgeni Yükleyin"),
    outputs=gr.Label(num_top_classes=5, label="Tahmin Sonuçları"),
    title="Akciğer Röntgeni Teşhis Asistanı",
    description="Bu yapay zeka modeli, bir akciğer röntgeni görüntüsünden 14 farklı radyolojik bulguyu tahmin etmek için eğitilmiştir. Lütfen bir görüntü yükleyin ve sonuçları görün.",
    examples=[["ornek_resim.png"]] # Eğer örnek resim eklediysen
)

# 4. Arayüzü başlat
iface.launch()