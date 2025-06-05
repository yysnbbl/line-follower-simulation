# Çizgi Takipçi Robot Simülasyonu

Bu proje, çizgi takipçi robotun davranışını simüle eden bir Python uygulamasıdır. Robot, sensörleri kullanarak çizgiyi takip eder ve PID kontrol sistemi ile hareketini düzenler.

## Kurulum Adımları

### 1. Python Kurulumu
1. Python'u [python.org](https://www.python.org/downloads/) adresinden indirin
2. İndirme sayfasında "Download Python" butonuna tıklayın (en son sürümü indirin)
3. İndirilen kurulum dosyasını çalıştırın
4. Kurulum sırasında "Add Python to PATH" seçeneğini işaretlemeyi unutmayın
5. Kurulumu tamamlayın

### 2. Proje Dosyalarının İndirilmesi
1. Bu projeyi bilgisayarınıza indirin
2. İndirdiğiniz dosyaları istediğiniz bir klasöre çıkartın

### 3. Gerekli Kütüphanelerin Kurulumu
1. Komut istemini (Command Prompt) açın
2. Proje klasörüne gidin:
   ```bash
   cd proje_klasörünün_yolu
   ```
3. Gerekli kütüphaneleri kurun:
   ```bash
   pip install -r requirements.txt
   ```

## Programı Çalıştırma

1. Komut isteminde proje klasöründe olduğunuzdan emin olun
2. Programı başlatmak için:
   ```bash
   python line_follower.py
   ```

## Program Kullanımı

Program başlatıldığında size üç seçenek sunulacaktır:

1. **Kurulum (Setup)**
   - İlk kez çalıştırırken bu seçeneği seçin
   - Robot ve sensörlerin konumunu belirleyin
   - Kurulum tamamlandığında otomatik olarak kaydedilecektir

2. **Çalıştır (Run)**
   - Kurulum yapıldıktan sonra simülasyonu başlatmak için bu seçeneği kullanın
   - Robot çizgiyi takip etmeye başlayacaktır
   - Ekranda hata, PID değeri ve motor hızları görüntülenecektir

3. **Çıkış (Exit)**
   - Programdan çıkmak için bu seçeneği kullanın

## Önemli Notlar

- Programı çalıştırmadan önce mutlaka kurulum yapmalısınız
- Kurulum sırasında robot ve sensörlerin konumunu dikkatli belirleyin
- Simülasyon sırasında robot haritadan çıkarsa program otomatik olarak duracaktır
- Programı kapatmak için pencereyi kapatabilir veya menüden "Çıkış" seçeneğini kullanabilirsiniz

## Gerekli Dosya Yapısı

Programın düzgün çalışması için aşağıdaki dosya yapısına sahip olmalısınız:

```
line_follower_simulation/
│
├── line_follower.py
├── requirements.txt
├── classes.py
├── utils.py
│
└── images/
    ├── robot.png
    └── map.png
```

## Sorun Giderme

1. **Python bulunamadı hatası alıyorsanız:**
   - Python'un doğru kurulduğundan emin olun
   - PATH değişkenlerinin doğru ayarlandığını kontrol edin

2. **Kütüphane kurulum hataları:**
   - İnternet bağlantınızı kontrol edin
   - pip'i güncelleyin: `python -m pip install --upgrade pip`

3. **Görüntü dosyaları bulunamıyor hatası:**
   - `images` klasörünün ve içindeki dosyaların doğru konumda olduğunu kontrol edin

## İletişim ve Destek

Herhangi bir sorun veya öneriniz için lütfen GitHub üzerinden issue açın veya proje sahibiyle iletişime geçin. 