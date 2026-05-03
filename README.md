# Metodist Listener

Bu Python skripti [Metodist portalında](https://www.metodist.edu.az/) sizin hesabınızı mütəmadi olaraq yoxlayır və oxunmamış yeni bildirişlər olduqda onları avtomatik olaraq Telegram botunuz vasitəsilə sizə göndərir.

## Necə işləyir?
1. Skript arxa planda Metodist portalına daxil olur.
2. Sizin təqdim etdiyiniz UTİS kodu və şifrə ilə sistemə avtorizasiya olunur.
3. Dashboard səhifəsindəki oxunmamış bildirişləri tapır.
4. Təkrarlanmanın qarşısını almaq üçün bildirişlərin ID-lərini yadda saxlayır və yalnız **yeni** bildirişləri Telegram-a göndərir.
5. Bu proses hər 5 dəqiqədən bir (istəyə uyğun dəyişdirilə bilər) davam edir.

---

## Qurulum Qaydası

### 1. Tələblər
- Kompüterinizdə **Python** (3.7 və ya daha yenisi) quraşdırılmış olmalıdır. Əgər yoxdursa, [python.org](https://www.python.org/downloads/) ünvanından yükləyə bilərsiniz.
- Layihəni terminalda (Command Prompt / PowerShell) aça bilməlisiniz.

### 2. Kitabxanaların yüklənməsi
Layihə qovluğunda terminal açın və aşağıdakı əmri daxil edərək lazımi paketləri yükləyin:
```bash
pip install -r requirements.txt
```

### 3. Konfiqurasiya (.env faylı)
Təhlükəsizlik məqsədilə şifrə və Telegram məlumatlarınız kodun içində deyil, xüsusi `.env` faylında saxlanılır.
Layihə qovluğunda **`.env`** adlı yeni fayl yaradın (əgər yoxdursa) və içərisinə bu məlumatları özünüzə uyğun doldurub yadda saxlayın:

```env
UTIS=SİZİN_UTİS_KODUNUZ
PASSWORD=SİZİN_ŞİFRƏNİZ
TELEGRAM_BOT_TOKEN=SİZİN_BOT_TOKENİNİZ
TELEGRAM_CHAT_ID=SİZİN_CHAT_ID_NİZ
```

> **Qeyd:**
> - `TELEGRAM_BOT_TOKEN` əldə etmək üçün Telegram-da **[@BotFather](https://t.me/BotFather)** botuna `/newbot` yazın və yeni bot yaradın.
> - `TELEGRAM_CHAT_ID` əldə etmək üçün Telegram-da **[@getmyid_bot](https://t.me/getmyid_bot)** botuna daxil olub `/start` vurun.
> - Özünüz yaratdığınız bota daxil olub `/start` düyməsini sıxmağı unutmayın ki, bot sizə mesaj göndərə bilsin!

### 4. Skriptin işə salınması
Hər şey hazırdırsa, terminalda aşağıdakı əmri yazaraq proqramı işə salın:
```bash
python listener.py
```

Ekranda "Metodist Listener işə salındı!" yazısını görəcəksiniz. Proqramı dayandırmaq istəsəniz terminalda `CTRL + C` düymələrini sıxa bilərsiniz.

---
**Təhlükəsizlik Xəbərdarlığı:**
`.env` faylını heç vaxt GitHub-a və ya digər açıq platformalara yükləməyin. Bu layihədəki `.gitignore` faylı avtomatik olaraq bunu əngəlləmək üçün nizamlanıb.
