import streamlit as st
from google import genai
from PIL import Image

# Sayfa Yapılandırması
st.set_page_config(page_title="Yemek Kalori Analizi", page_icon="🥗", layout="centered")

st.title("🥗 Yemek Kalori Tahmin Uygulaması")
st.write("Yemeğinizin fotoğrafını çekin veya yükleyin, yapay zeka kalori değerlerini çıkarsın!")

# API Anahtarı Girdisi
api_key = st.sidebar.text_input("Gemini API Key Giriniz:", type="password")

# Fotoğraf Alımı (Kamera veya Dosya Yükleme)
upload_option = st.radio("Fotoğraf Kaynağı Seçin:", ("Kamera ile Çek", "Dosya Yükle"))

image_data = None
if upload_option == "Kamera ile Çek":
    camera_file = st.camera_input("Yemeğin fotoğrafını çekin")
    if camera_file:
        image_data = Image.open(camera_file)
else:
    uploaded_file = st.file_uploader("Görsel yükleyin...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image_data = Image.open(uploaded_file)

# Ekran Üzerinde Fotoğrafı Gösterme
if image_data:
    st.image(image_data, caption="Analiz Edilecek Fotoğraf", use_column_width=True)
    
    if st.button("🔥 Kalori Hesapla"):
        if not api_key:
            st.error("Lütfen sol taraftaki menüden Gemini API anahtarınızı girin!")
        else:
            with st.spinner("Yemek analiz ediliyor..."):
                try:
                    # Gemini İstemcisi Oluşturma
                    client = genai.Client(api_key=api_key)
                    
                    # Yapay Zekaya Gönderilecek Komut
                    prompt = """
                    Sen uzman bir diyetisyensin. Fotoğraftaki yemeği detaylıca analiz et ve yanıtı Türkçe olarak ver.
                    Lütfen şu formatta bir çıktı sağla:
                    1. **Yemeğin Adı:** (Tahmini tabağın/yemeğin ismi)
                    2. **Tahmini Porsiyon Miktarı:** (Örn: 1 porsiyon, ~250 gram vb.)
                    3. **Toplam Tahmini Kalori:** (Örn: ~450 kcal)
                    4. **Besin Değerleri (Makrolar):**
                       - Karbonhidrat: X gram
                       - Protein: Y gram
                       - Yağ: Z gram
                    5. **Kısa Diyetisyen Yorumu:** (Sağlık açısından kısa bir değerlendirme)
                    """
                    
                    # Modeli Çağırma
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=[image_data, prompt]
                    )
                    
                    # Sonucu Ekrana Basma
                    st.success("Analiz Tamamlandı!")
                    st.markdown("---")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Hata oluştu: {e}")