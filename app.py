import streamlit as st
from google import genai
from PIL import Image
import hashlib

# Streamlit Cloud secrets üzerinden API anahtarını alıyoruz
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

st.title("🥗 Hızlı Yemek Kalori Analizi (Önbellekli)")

secim = st.radio("Fotoğraf Ekleme Yöntemi Seçin", ["Dosya Yükle", "Kamera ile Çek"])

uploaded_file = None

if secim == "Kamera ile Çek":
    uploaded_file = st.camera_input("Yemeğin fotoğrafını çekin")
else:
    uploaded_file = st.file_uploader("Yemeğin fotoğrafını yükleyin", type=["jpg", "jpeg", "png"])

# Önbelleğe alacak fonksiyon (Aynı fotoğraf tekrar yüklenirse yapay zekaya gitmeden direkt hafızadan getirir)
@st.cache_data
def analiz_et(image_bytes):
    # Byte verisinden tekrar Pillow Image nesnesi oluşturuyoruz
    from io import BytesIO
    image = Image.open(BytesIO(image_bytes))
    
    prompt = (
        "Bu fotoğraftaki yemeği kısa ve öz şekilde analiz et. "
        "1. Yemeklerin adı ve tahmini porsiyonu.\n"
        "2. İçindeki ana malzemeler.\n"
        "3. Toplam kalori ve makrolar (protein, karbonhidrat, yağ).\n"
        "Türkçe olarak net bir liste ver."
    )
    
    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=[image, prompt]
    )
    return response.text

if uploaded_file is not None:
    # 1. Dosya baytlarını okuyoruz (önbellek ve görsel işleme için)
    bytes_data = uploaded_file.getvalue()
    
    # 2. Fotoğrafı açıp boyutlandırıyoruz
    from io import BytesIO
    image = Image.open(BytesIO(bytes_data))
    image.thumbnail((800, 800))
    
    st.image(image, caption="Analiz Edilen Fotoğraf", use_column_width=True)

    if st.button("🔥 Hızlı Kalori Hesapla"):
        with st.spinner("Yemek analiz ediliyor... (Daha önce yüklendiyse anında gelecek)"):
            try:
                # Fonksiyonu çağırıyoruz (Streamlit aynı byte verisini görürse yapay zekayı es geçip anında sonuç döner)
                sonuc = analiz_et(bytes_data)
                
                st.subheader("📊 Analiz Sonucu")
                st.write(sonuc)
                
            except Exception as e:
                st.error(f"Hata oluştu: {e}")