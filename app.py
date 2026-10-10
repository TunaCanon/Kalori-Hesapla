import streamlit as st
from google import genai
from PIL import Image

# Streamlit Cloud üzerindeki Secrets'tan API anahtarını otomatik alıyoruz
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

st.title("🥗 Yemek Kalori Analizi")

# Artık sol tarafta API Key sorma kutusuna gerek kalmadı!
# Doğrudan fotoğraf yükleme veya kamera seçimi ile başlıyoruz.

secim = st.radio("Fotoğraf Ekleme Yöntemi Seçin", ["Dosya Yükle", "Kamera ile Çek"])

uploaded_file = None

if secim == "Kamera ile Çek":
    uploaded_file = st.camera_input("Yemeğin fotoğrafını çekin")
else:
    uploaded_file = st.file_uploader("Yemeğin fotoğrafını yükleyin", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Analiz Edilecek Fotoğraf", use_column_width=True)

    if st.button("🔥 Kalori Hesapla"):
        with st.spinner("Yemek analiz ediliyor..."):
            try:
                prompt = (
                    "Bu fotoğraftaki yemeği detaylıca analiz et. "
                    "1. Yemeklerin adını ve porsiyon miktarını belirt.\n"
                    "2. İçindeki ana malzemeleri ve tahmini gramajlarını yaz.\n"
                    "3. Toplam kalori miktarını ve besin değerlerini (protein, karbonhidrat, yağ) tahmin et.\n"
                    "Türkçe olarak düzenli bir liste halinde açıkla."
                )
                
                # Güncel Gemini modelini kullanıyoruz
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=[image, prompt]
                )
                
                st.subheader("📊 Analiz Sonucu")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Hata oluştu: {e}")