import streamlit as st
from google import genai
from PIL import Image

# Streamlit Cloud secrets üzerinden API anahtarını alıyoruz
api_key = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=api_key)

st.title("🥗 Hızlı Yemek Kalori Analizi")

secim = st.radio("Fotoğraf Ekleme Yöntemi Seçin", ["Dosya Yükle", "Kamera ile Çek"])

uploaded_file = None

if secim == "Kamera ile Çek":
    uploaded_file = st.camera_input("Yemeğin fotoğrafını çekin")
else:
    uploaded_file = st.file_uploader("Yemeğin fotoğrafını yükleyin", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 1. Fotoğrafı açıyoruz
    image = Image.open(uploaded_file)
    
    # 2. HIZLANDIRMA ADIMI: Fotoğrafın boyutunu yapay zekayı yormayacak şekilde küçültüyoruz (Max 800 piksel)
    image.thumbnail((800, 800))
    
    st.image(image, caption="Analiz Edilen Fotoğraf (Boyutlandırıldı)", use_column_width=True)

    if st.button("🔥 Hızlı Kalori Hesapla"):
        with st.spinner("Yemek çok daha hızlı analiz ediliyor..."):
            try:
                prompt = (
                    "Bu fotoğraftaki yemeği kısa ve öz şekilde analiz et. "
                    "1. Yemeklerin adı ve tahmini porsiyonu.\n"
                    "2. İçindeki ana malzemeler.\n"
                    "3. Toplam kalori ve makrolar (protein, karbonhidrat, yağ).\n"
                    "Türkçe olarak net bir liste ver."
                )
                
                # Gemini modelini çağırıyoruz
                response = client.models.generate_content(
                    model='gemini-2.5-flash',  # Hızlı ve verimli model sürümü
                    contents=[image, prompt]
                )
                
                st.subheader("📊 Analiz Sonucu")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Hata oluştu: {e}")