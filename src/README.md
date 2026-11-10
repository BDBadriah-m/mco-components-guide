# مصادر «دليل مكونات MCO» وملف الثيم

هذه الملفات منشورة مع صفحة الدليل نفسها (مجلد `src/`)، فأي تعديل مستقبلي يبدأ منها بدل إعادة البناء من الصفر.

## مصدر الحقيقة

```
Figma «MCO Design system»
   ↓ مزامنة
artifact «MCO Design System»  (tokens.json · bundle.css · bundle.js · README المكوّنات)
+ ملف التوكنز من Figma: mco-design-tokens-light-dark.css (الألوان الفاتحة والداكنة — مصدر الألوان)
   ↓ build_theme.py
MCO_OutSystems_Theme.css
   ↓ build_guide.py
دليل مكونات MCO  (guide/index.html)
```

القيم (ألوان، مسافات، زوايا، ظلال، أيقونات) تُعدَّل في نظام التصميم فقط، وتنتقل للثيم والدليل بإعادة البناء. ما يُكتب يدوياً هنا هو طريقة البناء في OutSystems.

## الملفات

| الملف | ما فيه | يُعدَّل يدوياً؟ |
| --- | --- | --- |
| `theme/theme_head.css` | الأقسام 1 و3 إلى 6 من الثيم: ربط متغيرات OutSystems UI، وتعديل الودجات، والكلاسات الإضافية | نعم |
| `theme/theme_extra.css` | القسم 8: إضافات البناء في OutSystems، والقسم 9: مكوّنات Figma الجديدة | نعم |
| `theme/extra_icons.json` | أيقونات من مجموعة Vuesax الكاملة غير موجودة في bundle.js (record-circle، archive…) | نعم، عند الحاجة لأيقونة جديدة |
| `build_theme.py` | يولّد القسم 2 من ملف التوكنز الفاتح/الداكن (+ المسافات والظلال من tokens.json)، والقسم 7 من bundle.css، وكلاسات الأيقونات. ويحوّل كل `var(--اسم-قديم)` للتوكن الدلالي حسب دوره (نص/خلفية/حد) | نادراً |
| `theme/token_roles.json` | ربط أسماء tokens.json القديمة بالتوكنز الدلالية حسب الدور | عند إضافة توكن |
| `guide/data.py` | محتوى الدليل: الأقسام والمجموعات، ولكل مكوّن الوصف والمعاينة وشجرة الودجات والخصائص | نعم |
| `guide/previews_extra.py` | معاينات المكوّنات اللي ما لها مقابل في bundle.js (الجديدة من Figma) | نعم |
| `assets/` | صور المعاينات من Figma (الشعار، الشعار المصغّر للتذييل، الرسم التوضيحي) | عند تغيّرها |
| `guide/conventions.html` | قواعد البناء المشتركة و MCO_Status والـ Structures | نعم |
| `guide/shell.html` | تصميم صفحة الدليل | نادراً |
| `build_guide.py` | يبني الصفحة ويرسم المعاينات | نادراً |
| `guide/guide_en.json` + `guide/conventions_en.html` | النسخة الإنجليزية من الدليل، وهي الافتراضية (`guide/index.html`؛ العربية في `guide/ar.html`): ترجمة نصوص data.py وأسطر شجرة الودجات. `build_guide.py` يبني النسختين ويطبع أي نص عربي ما له ترجمة (EN MISSING) | مع كل مكوّن جديد أو نص يتغيّر |
| `deps/` | نسخ من مصادر خارجية (الجدول التالي) | لا، تُستبدل |

## deps/

| الملف | المصدر |
| --- | --- |
| `mco-design-tokens-light-dark.css` | ملف التوكنز المصدَّر من Figma (فاتح وداكن) |
| `tokens.json` · `bundle.css` · `bundle.js` | artifact «MCO Design System»: `project/tokens.json` و`project/components/bundle.css` و`project/components/bundle.js` |
| `osui.css` | OutSystems UI ‏v2.30.0 من GitHub ‏(OutSystems/outsystems-ui)، مترجم من `src/scss/O11.OutSystemsUI.scss` بـ sass. إذا ترقّت المنصة لنسخة أحدث تُترجم من جديد |
| `react.production.min.js` · `react-dom.production.min.js` | React 18.3.1 (UMD)، لرسم معاينات الـ Blocks من bundle.js فقط |

## أنواع التعديل

**تغيير قيمة (لون، مسافة، أيقونة) أو إضافة توكن:** عدّلها في Figma وزامن نظام التصميم، ثم انسخ الملفات الثلاثة إلى `deps/` وشغّل `build_theme.py` ثم `build_guide.py`.

**مكوّن جديد في نظام التصميم:**
1. قرّر: هل يطابقه نمط في OutSystems UI؟ إذا نعم فهو `os`، وإلا `block`.
2. أضف تعريفه في `guide/data.py` داخل `C` وفي مجموعته داخل `SECTIONS` (فردي أو وظيفي).
3. لو احتاج CSS ما هو موجود في bundle.css، أضفه في `theme/theme_extra.css`.
4. شغّل `build_guide.py`.

**تعديل طريقة البناء (شجرة ودجات، Parameter، ملاحظة):** في `guide/data.py` فقط، ثم `build_guide.py`.

**تعديل سلوك ودجت من OutSystems UI (زر، حقل، جدول…):** في `theme/theme_head.css` القسم 5، ثم البناءان.

بعد كل تعديل: يُنشر الدليل على نفس الرابط (مع `src/` و`MCO_OutSystems_Theme.css`)، ويُرسل الثيم الجديد للمطورين، ويُحدَّث الدليل المكتوب إذا تغيّر شي في الخريطة.

## التشغيل

```
pip install beautifulsoup4 playwright tinycss2
python build_theme.py      # ← ../MCO_OutSystems_Theme.css
python build_guide.py      # ← ../guide/index.html
```

## مكوّنات أُضيفت مباشرة من Figma

القسم 9 من الثيم (أكتوبر 2026) مأخوذ من ملف Figma مباشرة، وما مرّ بنظام التصميم بعد: MCO_StatTile، والتبويبات الرئيسية، وMCO_UserCard، وMCO_SummaryCard، وMCO_SlideCard، وMCO_DetailsCard، وMCO_ExpandableText، وMCO_Gallery، وMCO_PersonCard، وMCO_AddBanner، وMCO_FormSection، وMCO_EmptyState، وMCO_Footer، وMCO_RecordCard، وMCO_Loader (9.15: الشعار كـ mask، وتوكنا التدرّج color-bg-loader-start وcolor-bg-loader-end مضافة لملف التوكنز ولمتغيرات Figma). فيه تدرّجات وظلال جديدة مكتوبة كقيم ثابتة، ويستاهل تُضاف كتوكنز في نظام التصميم في المزامنة الجاية. في `guide/data.py` كل مكوّن منها عليه `figma` = رقم العقدة، و`NEW` يحدد شارة «جديد».

## أخطاء وقعنا فيها، لا تتكرر

- **أسماء كلاسات تتعارض مع OutSystems UI:** كان كلاس التحميل `btn-loading` وهو موجود في OutSystems UI ويخفي الزر، فصار `mco-btn-loading`. وكلاسا `row` و`top` في صفحة الدليل تعارضا مع كلاسات المنصة. أي كلاس جديد يبدأ بـ `mco-` (أو `pv-` و`gd-` داخل صفحة الدليل).
- **السكرول في الصفحات اللي تحمّل osui.css:** OutSystems UI يقفل السكرول على `html`، لأن الشاشة في التطبيق تتمرّر داخل حاوية خاصة. صفحة الدليل تفتحه بـ `html { overflow: auto !important }`. هذا التعديل لصفحات المعاينة فقط، وما يدخل ملف الثيم.
- **أيقونات داخل عناصر المكتبات (القائمة المنسدلة مثلاً):** في القوالب يُكتب `url(@icon:chevron-down)` و build_theme.py يحوّله لـ data URI من نفس مجموعة الأيقونات.
- **الأيقونات كـ data URI:** رمز `#` لازم يُرمَّز (`%23`)، وإلا تختفي الأيقونة. build_theme.py يتكفّل بهذا.
- **أصول Figma:** روابط الأصول المؤقتة في Figma محجوبة من بيئة العمل، فالصور أُخذت كلقطات PNG من get_screenshot (تُحفظ تلقائياً في tool-results). للإنتاج يُصدَّر SVG من Figma مباشرة.
- **الاتجاه:** OutSystems UI يثبّت `body` على `ltr`، والثيم يقلبه بكلاس `is-rtl` اللي تضيفه المنصة مع اللغة العربية. أي قاعدة جديدة تُكتب بخصائص منطقية (`padding-inline`، `inset-inline-start`، `text-align: start`). وإذا ما أمكن (clip-path، أيقونة اتجاه)، تُضاف نسختها في القسم 10 تحت `:is(body:not(.is-rtl):not(.mco-guide), [dir="ltr"])`. صفحة الدليل تضع `mco-guide` على body وكل معاينة تحمل اتجاهها، وزر «عربي / EN» بجانب كل مكوّن يبدّل اتجاه معاينته فقط.

**تحديث مكتبة Figma (نوفمبر 2026) — القسم 11 من الثيم:** شريط التنقل الجديد (تدرّج وتموّجات ونوع stepper)، MCO_StepsBar (مؤشر الخطوات الدائري)، بطاقة السجل بحد متدرّج وأنواع الزيارة والاستقبال، شريط الإضافة بزرّين، وMCO_Avatar وMCO_InfoField وMCO_DateTile وMCO_FactItem وMCO_CardHeader وMCO_ActivityCard وMCO_FileItem وMCO_DetailHeader، وشكل card في MCO_EmptyState. كل الألوان متغيرات دلالية من ملف التوكنز.

**الأيقونات:** الثيم فيه الأيقونات المستخدمة في المكوّنات فقط. المجموعة الكاملة (900 أيقونة Vuesax outline من `deps/vuesax-outline.json`) يولّدها `build_theme.py` في `MCO_Icons_All.css` (حوالي 1.4 ميجابايت)، ويُضاف في الـ Theme كـ Style Sheet ثاني بعد ملف الثيم عند الحاجة. الأسماء اللي فيها رموز تتحوّل لشرطات (`ruler&pen` ← `ruler-pen`).
