# 📈 סימולטור מסחר אוטונומי מבוסס AI (פרויקט גמר ב-OOP)

## 👤 מגישים: איתי חדאד , נועה זמיר , עדן קוגן 
**המסלול האקדמי המכללה למינהל** | **B.A. בניהול מערכות מידע**

---

## 📝 סקירת הפרויקט
פרויקט זה הוא **סימולטור למסחר במניות** מורכב שפותח כעבודת גמר בקורס "פיתוח מונחה עצמים ופייתון". המערכת מדמה סביבת מסחר אמיתית על ידי שילוב של **נתוני שוק בזמן אמת** (באמצעות Yahoo Finance) ו**בינה מלאכותית** (באמצעות Google Gemini 2.0) כדי לספק המלצות מסחר וניתוח סנטימנט שוק באופן אוטומטי.

המערכת בנויה לפי תבנית הארכיטקטורה **MVC (Model-View-Controller)**, המבטיחה הפרדה נקייה בין לוגיקת הנתונים, ממשק המשתמש והבקרה על המערכת.

---

## 🚀 תכונות מרכזיות
* **סנכרון נתונים בזמן אמת**: משיכת מחירי מניות חיים (AAPL, TSLA, NVDA וכו') באמצעות ספריית `yfinance`.
* **תובנות מבוססות AI**: שימוש ב-SDK של `google-genai` ליצירת כותרות חדשות פיננסיות וסיגנלים אגרסיביים למסחר (BUY/SELL) בהתאם למגמות השוק.
* **מסחר אוטונומי**: בוט AI המסוגל לבצע עסקאות באופן אוטומטי תוך שימוש באחוז מוגדר מהמזומן הפנוי בתיק.
* **ניתוח ויזואלי**: הפקת שלוש היסטוגרמות (גרפי עמודות) דינמיות באמצעות `matplotlib` לניתוח צמיחת הפורטפוליו, ביצועי המניות (אחוזי רווח/הפסד) ופיזור הנכסים.
* **ניהול נתונים**: כל העסקאות מתועדות במסד נתונים מקומי מסוג **SQLite** לצורך מעקב היסטורי.

---

## 🏗 ארכיטקטורת המערכת (MVC & OOP)
הפרויקט משמש כחלון ראווה ליישום עקרונות מתקדמים בתכנות מונחה עצמים:

### 1. שכבת המודל (Model)
* **`Stock`**: מייצגת את ישות המניה ומנהלת את עדכוני המחירים.
* **`Portfolio`**: מנהלת את אחזקות המשתמש והמזומן. מיישמת **אנקפסולציה** ו**העמסת אופרטורים** (`__add__`, `__len__`, `__getitem__`).
* **`DatabaseManager`**: אחראית על שמירת הנתונים תוך שימוש ב-**Decorator Pattern** (`@audit_logger`) לצורך תיעוד אוטומטי.

### 2. שכבת התצוגה (View)
* **`CLIView`**: מנהלת את ממשק שורת הפקודה (CLI) ואת הפלט הגרפי. משתמשת ב-`tabulate` להצגת נתונים בטבלאות וב-`matplotlib` להפקת דוחות ויזואליים.

### 3. שכבת הבקרה (Controller)
* **`MainController`**: ה"מוח" של האפליקציה. מתזמר את זרימת המידע בין ה-AI, השוק ותיק ההשקעות של המשתמש.

---

## 🧪 עקרונות OOP שיושמו
בהתאם לדרישות הפרויקט (נספח א'), המושגים הבאים הוטמעו בקוד:
* **אנקפסולציה (Encapsulation)**: שימוש בתכונות פרטיות (למשל `_cash`) המוגנות על ידי Properties ומתודות.
* **פולימורפיזם ותבנית Strategy**: מחלקת בסיס אבסטרקטית `TradingStrategy` המאפשרת התנהגויות שונות לבוטים (Random, Momentum).
* **פונקציות Dunder**: מימושים מותאמים אישית של `__str__`, `__repr__`, `__len__` ו-`__add__`.
* **ניהול חריגות (Exceptions)**: טיפול בשגיאות באמצעות מחלקות ייעודיות כמו `InsufficientFundsError` ו-`InsufficientSharesError`.

---

## 🛠 התקנה והרצה
1. **שיבוט המאגר (Clone):**
   ```bash
   git clone [git clone https://github.com/edenk5/oop-final-project.git)
