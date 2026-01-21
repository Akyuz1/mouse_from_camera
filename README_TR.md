# Mouse From Camera

Kamera üzerinden el hareketleriyle mouse kontrolü sağlayan bir Python projesidir.
---
 
### Gereksinimler
- Python 3.11
- OpenCV
- MediaPipe
- PyAutoGUI
- keyboard

### Kurulum
```bash
pip install opencv-python mediapipe pyautogui keyboard
```

### Ayarlar 

Proje başlangıçta **varsayılan ayarlar** ile çalışır.

Ayarları değiştirmek için:
- **Ctrl + Shift + "** → Ayar panelini (HTML) açar
- Tarayıcıdan değişiklikleri yapıp **Save** butonuna bas
- İndirilen `.json` dosyasını projeye uygulamak için:
- **Ctrl + Shift + R**

> ⚠️ Tuş kombinasyonlarının çalışması için projenin **çalışır durumda** olması gerekir.

> 🔎 **Not:** Proje çalıştırıldığında kameraya erişip sağ elinize göre imlecinizi yönetir. Compiled edition kullanımı önerilir.

### Hareketler ve Kullanım
####  Sol Tıklama
- Avuç içi kameraya bakmalı
- Parmaklar ayrık ve el açık olmalı
- **İşaret parmağını** ileri–aşağı hareket ettir

####  Sağ Tıklama
- Avuç içi kameraya bakmalı
- Parmaklar ayrık ve el açık olmalı
- **Orta parmağını** ileri–aşağı hareket ettir

####  Fare Tekerleği (Scroll)
- Elinizi kameraya **yan çevirin**
- Parmaklarınızı **birleştirin**
- **Baş parmak ucu** ile **işaret parmağı ucu** arasındaki mesafe scroll hızını belirler
> 💡 İpucu: Scroll hareketi için elinizi sabit tutmanız daha pürüzsüz sonuç verir.


### ⚠️ Dikkat edilmesi gerekenler ⚠️
> Proje halen mükemmel çalışmamakla birlikte bazı hız ve takılma sorunları mevcuttur.
> Başka bir nesneyi el olarak algılama gibi hatalar olabilir.
> Kameranızın performansına göre algılama ve işleyiş hızı değişkenlik gösterecektir.
> Karanlık ortamlarda da düşük performans göstermektedir.
> Proje ayarları HTML üzerinden değiştirildiğinde, proje her başlatıldığında bu işlemin tekrar yapılması gerekir.
> Sabit ayarlar için proje kodundaki değişken değerlerini değiştiriniz
> **Esc** tuşu projenin çalışmasını sonlandırır
