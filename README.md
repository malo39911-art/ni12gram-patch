# ni12gram (patch)

ni12gram = [Niagram](https://github.com/HSSkyBoy/Niagram) (commit `bc99e5e9907a2ea47d9e6ed432469b8ff553644f`) + `ni12gram.patch`.
Unofficial, not affiliated with or endorsed by Telegram. Licensed under **GPL-3.0** (see `LICENSE`);
copyright of the original code stays with the authors of Telegram for Android, Nekogram, Nagram, NagramX and Niagram.

## What the patch changes
- App name `ni12gram`, package `com.ni12gram.app` (installs next to the original Niagram/Telegram)
- Welcome screen: title "الادمن مر من هنا" + the ni12 logo instead of the Telegram plane
- Launcher icon from the ni12 logo
- Login screen (⋮ menu): **Log in with bot token** (`auth.importBotAuthorization`)
- New built-in theme **ni12** in the logo colors (default theme)
- Settings > About: credits / GPL notice / source link

## الطريقة (من Termux)
1. خذ مفاتيحك من https://my.telegram.org ← API development tools ← أنشئ تطبيق ← انسخ `api_id` و `api_hash`.
2. ارفع المشروع (يكون **public** عشان البناء مجاني وبدون حد):
```bash
cd ~ && unzip -o ni12gram-patch.zip -d ni12gram-patch && cd ni12gram-patch
git init -b main && git add -A && git commit -m "init"
gh repo create ni12gram-patch --public --source=. --push
```
3. أضف المفاتيح (يطلب منك تلصق القيمة):
```bash
gh secret set TELEGRAM_APP_ID -R malo39911-art/ni12gram-patch
gh secret set TELEGRAM_APP_HASH -R malo39911-art/ni12gram-patch
```
4. شغّل البناء (الأول ياخذ وقت طويل، ساعة تقريباً):
```bash
gh workflow run build.yml -R malo39911-art/ni12gram-patch
gh run list -R malo39911-art/ni12gram-patch -L 1
```
5. لما يصير `✓`:
```bash
rm -rf ~/ni12apk && gh run download -R malo39911-art/ni12gram-patch -n ni12gram-APK -D ~/ni12apk
cp $(find ~/ni12apk -name "*.apk" | head -1) ~/storage/downloads/ni12gram.apk
```
6. **مهم لتحديث التطبيق لاحقاً بدون ما تفقد حسابك:** أول بناء يسوي مفتاح توقيع جديد ويرفعه كملف `ni12gram-keystore`. نزّله واحفظه كسر:
```bash
gh run download -R malo39911-art/ni12gram-patch -n ni12gram-keystore -D ~/ni12ks
base64 -w0 ~/ni12ks/ni12gram.keystore | gh secret set KEYSTORE_BASE64 -R malo39911-art/ni12gram-patch
```
بعدها كل البناءات تنوقّع بنفس المفتاح وتتحدّث فوق النسخة المثبتة.

## إذا فشل البناء
```bash
gh run view -R malo39911-art/ni12gram-patch --log-failed | tail -80
```
انسخ النص وأرسله.

## ملاحظات
- لم يُجرَّب البناء ولا التطبيق على جهاز حقيقي، فقد يحتاج تصحيحات.
- إشعارات Google (FCM) ما تشتغل لأن الحزمة جديدة وبدون مشروع Firebase خاص فيك.
- البوت يسجّل دخول بمفاتيح `api_id/api_hash` حقتك.
