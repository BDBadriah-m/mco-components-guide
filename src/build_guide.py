# -*- coding: utf-8 -*-
"""يبني صفحة «دليل مكونات MCO» (guide/index.html).

المحتوى كله في guide/data.py (المكوّنات، الأقسام، شجرة الودجات، الخصائص).
القالب في guide/shell.html، وقواعد البناء المشتركة في guide/conventions.html.
يحتاج: Python 3 مع beautifulsoup4 وplaywright (Chromium)، وملفات deps/ (README.md).
شغّل build_theme.py أولاً، لأن المعاينات تستخدم الثيم الناتج.
"""
import json, os, re, html, sys, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'guide'))
from data import SECTIONS, C, OS, BLOCK, MIX, NEW
import previews_extra
FIGMA = 'https://www.figma.com/design/Ka5SJhV7MC80LJucRUtFl9/MCO-Design-system?node-id='
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

DEPS = os.path.join(HERE, 'deps')
GUIDE = os.path.join(HERE, 'guide')
# الإنجليزي هو الافتراضي (index.html)، والعربي في ar.html
OUT = os.path.join(HERE, '..', 'guide', 'ar.html')
OUT_EN = os.path.join(HERE, '..', 'guide', 'index.html')

# ---------- النسخة الإنجليزية (guide/index.html، الافتراضية؛ العربية في guide/ar.html) ----------
# نصوص data.py وأسطر شجرة الودجات تُترجم من guide/guide_en.json، ونصوص الصفحة من CHROME_EN تحت.
LANG = 'ar'
_EN = json.load(open(os.path.join(GUIDE, 'guide_en.json'), encoding='utf-8'))
MISSING = set()
CHROME_EN = {
 'جديد': 'New', 'فتح في Figma': 'Open in Figma', 'تبديل المعاينة بين العربي والإنجليزي': 'Switch the preview between Arabic and English',
 'معاينة': 'Preview', 'الاستخدام': 'Usage', 'الحالة': 'Case', 'في OutSystems': 'In OutSystems', 'ملاحظة': 'Note',
 'الاسم': 'Name', 'النوع': 'Type', 'الوصف': 'Description', 'كلاسات إضافية على الجذر': 'Extra classes on the root',
 'يمرّر': 'Passes', 'يوضع فيه': 'Holds', 'شجرة الودجات': 'Widget tree', 'مثال في Service Studio': 'Example in Service Studio',
 'نمط OutSystems UI': 'OutSystems UI pattern', 'Block مخصّص': 'Custom Block', 'ودجت المنصة + Block': 'Platform widget + Block',
 'القسم': 'Section', 'الأول': '1', 'الثاني': '2', 'مكوّناً': 'components',
}

SHELL_EN = [
 ('<title>دليل مكونات MCO</title>', '<title>MCO Components Guide</title>'),
 ('<div class="gd" dir="rtl">', '<div class="gd" dir="ltr" lang="en">'),
 ('<span class="eyebrow">منصة تواصل الوزراء · OutSystems 11 Reactive</span>', "<span class=\"eyebrow\">Ministers' Communication Platform · OutSystems 11 Reactive</span>"),
 ('<h1>دليل مكونات MCO</h1>', '<h1>MCO Components Guide</h1>'),
 ('<p>كل مكوّن في نظام التصميم مع طريقة بنائه في Service Studio: الودجت أو الـ Block المستخدم، وشجرة الودجات بكلاساتها، والخصائص. المعاينات مرسومة بـ CSS ‏OutSystems UI 2.30 وثيم MCO نفسه.</p>',
  '<p>Every design system component with how to build it in Service Studio: the widget or Block to use, the widget tree with its classes, and the properties. Previews are drawn with the OutSystems UI 2.30 CSS and the MCO theme itself. This English version shows the previews in English (LTR); the “عربي / EN” button on each component switches it back to Arabic.</p>'),
 ('id="copy-theme">نسخ ملف الثيم</button>', 'id="copy-theme">Copy theme file</button>'),
 ('<span>الوضع الداكن</span>', '<span>Dark mode</span>'),
 ('rel="noopener">الدليل المكتوب</a>', 'rel="noopener">Written guide (Arabic)</a>'),
 ('href="index.html" lang="en" hreflang="en">English</a>', 'href="ar.html" lang="ar" hreflang="ar">عربي</a>'),
 ('آخر تحديث:', 'Last updated:'),
 ('aria-label="محتوى ملف الثيم"', 'aria-label="Theme file contents"'),
 ('<dt>مكوّن</dt>', '<dt>Components</dt>'), ('<dt>نمط OutSystems UI</dt>', '<dt>OutSystems UI patterns</dt>'), ('<dt>Block مخصّص</dt>', '<dt>Custom Blocks</dt>'),
 ('aria-label="فهرس الدليل"', 'aria-label="Guide contents"'),
 ("'تم نسخ رابط SVG للأيقونة «' + name + '». '", "'Copied the SVG link for “' + name + '”. '"), ("'رابط SVG للأيقونة «' + name + '»: '", "'SVG link for “' + name + '”: '"),
 ("'تنزيل ' + name + '.svg'", "'Download ' + name + '.svg'"), ("'الاسم: ' + name", "'Name: ' + name"),
 ("'جارٍ التحميل…'", "'Loading…'"), ("'انسخ المحتوى من المربع (Ctrl+C).'", "'Copy the contents from the box (Ctrl+C).'"),
 ("'تم نسخ ملف الثيم كاملاً، الصقه في Style Sheet الخاص بالـ Theme.'", "'Theme file copied. Paste it into the Theme Style Sheet.'"),
 ("'تعذّر تحميل ملف الثيم من هنا. افتحه مباشرة: '", "'Couldn\\'t load the theme file from here. Open it directly: '"),
 ("'تعذّر النسخ التلقائي هنا. نزّل الملف أو افتحه وانسخ محتواه: '", "'Automatic copy isn\\'t allowed here. Download the file, or open it and copy its contents: '"),
 ("'تنزيل MCO_OutSystems_Theme.css'", "'Download MCO_OutSystems_Theme.css'"), ("'فتح الملف'", "'Open file'"),
 ("'عرض أقل' : 'عرض المزيد'", "'Show less' : 'Show more'"), ("'طي' : 'توسيع'", "'Collapse' : 'Expand'"),
 ("'فتح القائمة' : 'طي القائمة'", "'Expand menu' : 'Collapse menu'"), ("'الوضع الفاتح' : 'الوضع الداكن'", "'Light mode' : 'Dark mode'"),
 ('<h3 class="mco-dcard__title">أبرز عوامل النجاح</h3>', '<h3 class="mco-dcard__title">Key success factors</h3>'),
 ('<p class="mco-xtext__text">تحقيق التكامل بين الجهات المشاركة، ووضوح الرسائل الرئيسية، والالتزام بالجدول الزمني المعتمد للأنشطة.</p>', '<p class="mco-xtext__text">Integration between the participating entities, clear key messages, and keeping to the approved activity schedule.</p>'),
 ("'وزارة الخارجية'", "'Ministry of Foreign Affairs'"), ("'وزارة المالية'", "'Ministry of Finance'"), ("'وزارة الصحة'", "'Ministry of Health'"),
 ("'وزارة الإعلام'", "'Ministry of Media'"), ("'وزارة الثقافة'", "'Ministry of Culture'"), ("'وزارة التعليم'", "'Ministry of Education'"),
 ("textDirection: 'rtl', placeholder: 'اختر', searchPlaceholderText: 'بحث'", "textDirection: 'ltr', placeholder: 'Select', searchPlaceholderText: 'Search'"),
 ("noOptionsText: 'لا توجد خيارات', noSearchResultsText: 'لا توجد نتائج'", "noOptionsText: 'No options', noSearchResultsText: 'No results'"),
]
def T(s):
    return CHROME_EN.get(s, s) if LANG == 'en' else s
def tr(s):
    if LANG != 'en' or not isinstance(s, str) or not re.search(r'[؀-ۿ]', s): return s
    v = _EN['data'].get(s)
    if v is None: MISSING.add(s); return s
    return v
def tr_tree(src):
    if LANG != 'en': return src
    out = []
    for l in src.split('\n'):
        if re.search(r'[؀-ۿ]', l):
            # المفتاح هو السطر بدون المسافة البادئة، فتبقى الترجمة صالحة لو تغيّر عمق السطر
            v = _EN['tree'].get(l.strip())
            if v is None: MISSING.add(l.strip())
            else: l = l[:len(l) - len(l.lstrip())] + v.strip()
        out.append(l)
    return '\n'.join(out)
rd = lambda *p: open(os.path.join(*p), encoding='utf-8').read()
react = rd(DEPS, 'react.production.min.js')
rdom = rd(DEPS, 'react-dom.production.min.js')
bundle = rd(DEPS, 'bundle.js')
osui = rd(DEPS, 'osui.css')
theme = rd(HERE, '..', 'MCO_OutSystems_Theme.css').replace(
    '@import url("https://fonts.googleapis.com/css2?family=Almarai:wght@300;400;700;800&display=swap");', '')

def _icons_from_bundle():
    m = re.search(r'var ICONS = (\{.*?\});\n', bundle, re.S)
    raw = json.loads(m.group(1))
    # نفس شكل SVG بعد رسمه في المتصفح (self-closing → عنصر كامل)
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        out = pg.evaluate("""(icons)=>{const r={};for(const k in icons){const s=document.createElementNS('http://www.w3.org/2000/svg','svg');s.innerHTML=icons[k];r[k]=s.innerHTML;}return r}""", raw)
        b.close()
    return out
ICONS = _icons_from_bundle()
EXTRA_ICONS = sorted(json.load(open(os.path.join(HERE, 'theme', 'extra_icons.json'))))
INV = {v: k for k, v in ICONS.items()}

def svgdata(s):
    return 'data:image/svg+xml,' + urllib.parse.quote(s)
FLAG_AE = svgdata('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 6"><rect width="12" height="2" fill="#00732f"/><rect y="2" width="12" height="2" fill="#fff"/><rect y="4" width="12" height="2" fill="#000"/><rect width="3" height="6" fill="#ff0000"/></svg>')
FLAG_KW = svgdata('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 6"><rect width="12" height="2" fill="#007a3d"/><rect y="2" width="12" height="2" fill="#fff"/><rect y="4" width="12" height="2" fill="#ce1126"/><path d="M0 0 3 1.5V4.5L0 6z" fill="#000"/></svg>')
FLAG_BH = svgdata('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 15 9"><rect width="15" height="9" fill="#ce1126"/><path d="M0 0h4l1.5 .9-1.5.9 1.5.9-1.5.9 1.5.9-1.5.9 1.5.9-1.5.9 1.5.9L4 9H0z" fill="#fff"/></svg>')

# ---------- React previews → static HTML ----------
REACT_ITEMS = {k: v['preview_js'] for k, v in C.items() if 'preview_js' in v}
helpers = r"""
var h=React.createElement,M=window.MCO;
function row(kids,cls){return h('div',{className:'pv-row'+(cls?' pv-'+cls:'')},kids);}
var FLAG_SA='%s',FLAG_AE='%s',FLAG_EG='%s';
""" % (FLAG_AE, FLAG_KW, FLAG_BH)
# CountryTag names should match drawn flags
REACT_ITEMS['ctag'] = "row([h(M.CountryTag,{key:1,name:'الإمارات',flag:FLAG_SA}),h(M.CountryTag,{key:2,name:'الكويت',flag:FLAG_AE}),h(M.CountryTag,{key:3,name:'البحرين',flag:FLAG_EG})])"
EXTRA_REACT = {
 'POPUP': "h('div',{className:'popup-dialog mco-popup-default pv-popup'},h(M.Popup,{status:'success',title:'تم إرسال الخطة',actions:[h(M.Button,{key:1},'العودة للخطط'),h(M.Button,{key:2,variant:'cancel'},'إغلاق')]},'أُرسلت خطة التواصل إلى الجهة المعنية للاعتماد.'))",
 'FORMPOPUP': "h('div',{className:'popup-dialog mco-popup-form pv-popup'},h(M.FormPopup,{title:'إضافة عضو',actions:[h(M.Button,{key:1},'حفظ'),h(M.Button,{key:2,variant:'cancel'},'إلغاء')]},h(M.TextField,{label:'الاسم',defaultValue:'سارة العتيبي'}),h(M.TextField,{label:'الجهة',placeholder:'اسم الجهة'}),h('div',{className:'mco-span-all'},h(M.TextField,{label:'البريد الإلكتروني',placeholder:'name@gov.sa'}))))",
 'LAYOUT': "h('div',{className:'pv-shell'},h(M.PageShell,{sideMenu:h('div',{className:'pv-sideslot'}),navbar:h(M.Navbar,{title:'خطط التواصل',breadcrumbs:[{label:'الرئيسية',href:'#'},{label:'خطط التواصل'}],action:h(M.Button,{size:'mobile',iconStart:'add'},'إضافة خطة')}),footer:[h('span',{key:1},'منصة تواصل الوزراء © 2026'),h('span',{key:2},'سياسة الخصوصية')],emptyText:'لا توجد خطط بعد'}))",
 'NAVBAR': "h('div',{className:'pv-stack'},h(M.Navbar,{title:'الأهداف الاستراتيجية',onBack:function(){},breadcrumbs:[{label:'خطة التواصل السنوية',href:'#'},{label:'الأهداف الاستراتيجية'}],action:h(M.Button,{size:'mobile',iconStart:'add'},'إضافة هدف')}),h(M.Navbar,{type:'tabs',title:'أجندة التواصل',breadcrumbs:[{label:'أجندة التواصل'}],tabs:h('div',{className:'osui-tabs osui-tabs--is-horizontal'},h('div',{className:'osui-tabs__header pv-tabs'},h('button',{className:'osui-tabs__header-item osui-tabs--is-active'},'الكل'),h('button',{className:'osui-tabs__header-item'},'القادمة'),h('button',{className:'osui-tabs__header-item'},'السابقة')))}),h(M.Navbar,{type:'simple'}))",
 'FILTERBAR': "h(M.FilterBar,{search:h('input',{className:'form-control pv-w100',placeholder:'ابحث برقم الخطة أو الاسم','aria-label':'بحث'})},h('select',{className:'form-control pv-w100','aria-label':'الجهة'},h('option',null,'كل الجهات')),h('select',{className:'form-control pv-w100','aria-label':'الربع'},h('option',null,'كل الأرباع')))",
}
ALL_REACT = dict(REACT_ITEMS); ALL_REACT.update(EXTRA_REACT)

def render_react():
    js = helpers + ''.join(
        "(function(){var d=document.createElement('div');d.id='r-%s';document.body.appendChild(d);ReactDOM.createRoot(d).render(%s);})();" % (k, v)
        for k, v in ALL_REACT.items())
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.set_content('<html dir="rtl"><body><script>%s</script><script>%s</script><script>%s</script><script>%s</script></body></html>' % (react, rdom, bundle, js))
        pg.wait_for_timeout(800)
        out = {k: pg.eval_on_selector('#r-' + k, 'e=>e.innerHTML') for k in ALL_REACT}
        b.close()
    if errs: print('REACT ERRORS', errs)
    return out

BTN_MAP = [('mco-btn--primary', 'btn-primary'), ('mco-btn--secondary', ''), ('mco-btn--tertiary', 'btn-tertiary'), ('mco-btn--link', 'btn-link'),
           ('mco-btn--cancel', 'btn-cancel'), ('mco-btn--mobile', 'btn-mobile'), ('mco-btn--small', 'btn-small'), ('mco-btn--default', ''), ('is-loading', 'btn-loading')]

def to_os(htmlstr):
    s = BeautifulSoup(htmlstr, 'html.parser')
    for svg in s.find_all('svg'):
        inner = svg.decode_contents()
        name = INV.get(inner)
        if name is None and 'M1.2 5.2' in inner: name = 'check'
        if name is None:
            svg.decompose(); continue
        cls = [c for c in svg.get('class', []) if c in ('mco-flip', 'mco-rot')]
        size = svg.get('width', '24')
        span = s.new_tag('span')
        span['class'] = ['mco-icon', 'mco-i-' + name] + cls
        span['style'] = 'width:%spx;height:%spx' % (size, size)
        span['aria-hidden'] = 'true'
        svg.replace_with(span)
    for b in s.select('.mco-btn'):
        cls = b.get('class', [])
        destructive = 'mco-btn--destructive' in cls
        new = ['btn']
        for c in cls:
            for a, z in BTN_MAP:
                if c == a and z: new.append(z)
        if destructive:
            if 'btn-primary' in new: new.remove('btn-primary'); new.append('btn-error')
            elif 'btn-tertiary' in new: new.append('btn-destructive')
            else: new.append('btn-destructive')
        b['class'] = new
    for el in s.select('strong'):
        if el.parent and 'mco-addmore__text' in el.parent.get('class', []):
            el.name = 'span'; el['class'] = ['mco-addmore__title']
    return str(s)

# ---------- OS widget previews (hand-written, same markup the platform renders) ----------
def I(name, size=20, extra=''):
    return '<span class="mco-icon mco-i-%s%s" style="width:%dpx;height:%dpx" aria-hidden="true"></span>' % (name, (' ' + extra) if extra else '', size, size)

def os_previews():
    P = {}
    P['BUTTONS'] = '<div class="pv-stack">' + ''.join('<div class="pv-row"><span class="pv-k">%s</span>%s</div>' % (t, b) for t, b in [
        ('الأنواع', '<button class="btn btn-primary">%s<span>أساسي</span></button><button class="btn">ثانوي</button><button class="btn btn-tertiary">نصي</button><button class="btn btn-link">رابط</button><button class="btn btn-cancel">إلغاء</button>' % I('add')),
        ('خطِر', '<button class="btn btn-error">حذف</button><button class="btn btn-destructive">حذف</button><button class="btn btn-tertiary btn-destructive">حذف</button>'),
        ('الأحجام', '<button class="btn btn-primary">44px</button><button class="btn btn-primary btn-mobile">36px جوال</button><button class="btn btn-primary btn-small">32px صغير</button>'),
        ('الحالات', '<button class="btn btn-primary" disabled>معطّل</button><button class="btn" disabled>معطّل</button><button class="btn btn-primary mco-btn-loading" disabled aria-label="جارٍ التحميل"><span class="mco-btn__dots"><span></span><span></span><span></span></span></button><button class="btn btn-primary"><span>التالي</span>%s</button>' % I('arrow-left'))]) + '</div>'
    P['CHECKBOX'] = '<div class="pv-row">' + ''.join('<span class="mco-choice-row"><input type="checkbox" class="checkbox" data-checkbox id="cb%d"%s><label for="cb%d">%s</label></span>' % (i, a, i, t) for i, (a, t) in enumerate([(' checked', 'محدد'), ('', 'غير محدد'), (' class="checkbox not-valid"', 'خطأ'), (' disabled checked', 'معطّل')])) + '</div>'
    P['CHECKBOX'] = P['CHECKBOX'].replace('class="checkbox" data-checkbox id="cb2" class="checkbox not-valid"', 'class="checkbox not-valid" data-checkbox id="cb2"')
    P['RADIO'] = '<div class="radio-group is-horizontal pv-row" role="radiogroup" aria-label="نوع الخطة">' + ''.join('<span class="mco-choice-row"><input type="radio" class="radio-button" name="rg" id="rb%d"%s><label for="rb%d">%s</label></span>' % (i, a, i, t) for i, (a, t) in enumerate([(' checked', 'داخلية'), ('', 'خارجية'), (' disabled', 'معطّل')])) + '</div>'
    P['SWITCH'] = '<div class="pv-row">' + ''.join('<span class="mco-choice-row"><input type="checkbox" data-switch id="sw%d"%s><label for="sw%d">%s</label></span>' % (i, a, i, t) for i, (a, t) in enumerate([(' checked', 'مفعّل'), ('', 'متوقف'), (' disabled', 'معطّل')])) + '</div>'
    P['CHOICECARD'] = '<div class="pv-row">' + ''.join('<label class="mco-card-choice%s" for="cc%d"><input type="radio" class="radio-button" name="cc" id="cc%d"%s><span>%s</span></label>' % (c, i, i, a, t) for i, (c, a, t) in enumerate([('', ' checked', 'خطة سنوية'), ('', '', 'خطة ربعية'), (' mco-card-choice--small', '', 'صغير'), (' is-disabled', ' disabled', 'معطّل')])) + '</div>'
    def tabs(items, extra='', vertical=False):
        cls = 'osui-tabs ' + ('osui-tabs--is-vertical ' if vertical else 'osui-tabs--is-horizontal ') + extra
        hd = ''.join('<button type="button" role="tab" class="osui-tabs__header-item%s" aria-selected="%s">%s</button>' % (' osui-tabs--is-active' if i == 0 else '', 'true' if i == 0 else 'false', t) for i, t in enumerate(items))
        return '<div class="%s"><div class="osui-tabs__header pv-tabs%s" role="tablist">%s</div></div>' % (cls, ' pv-vert' if vertical else '', hd)
    P['TABS'] = '<div class="pv-stack"><span class="pv-k">خط سفلي (الافتراضي)</span>%s<span class="pv-k">mco-tabs-filled</span>%s<span class="pv-k">mco-tabs-list</span>%s</div>' % (
        tabs(['الكل', 'القادمة', 'السابقة']), tabs(['الكل', 'المسودات', 'المعتمدة'], 'mco-tabs-filled'), tabs(['البيانات العامة', 'الأهداف', 'المرفقات'], 'mco-tabs-list', True))
    pag = '<div class="pagination-container" role="navigation" aria-label="ترقيم الصفحات"><button class="pagination-button" disabled aria-label="السابق">%s</button><button class="pagination-button is--active" aria-current="page">1</button><button class="pagination-button">2</button><button class="pagination-button">3</button><button class="pagination-button is--ellipsis" tabindex="-1">…</button><button class="pagination-button">9</button><button class="pagination-button" aria-label="التالي">%s</button></div>' % (I('arrow-left', 20, 'mco-flip'), I('arrow-left'))
    P['PAGINATION'] = pag
    P['PFOOTER'] = '<div class="mco-pfooter">%s<label class="mco-pfooter__size"><select aria-label="عدد النتائج"><option>عدد النتائج 12</option><option>عدد النتائج 24</option><option>عدد النتائج 48</option></select>%s</label></div>' % (pag, I('chevron-down', 18))
    P['TOAST'] = '<div class="pv-stack">' + ''.join('<div class="feedback-message feedback-message-%s pv-static" role="status">%s<span class="feedback-message-text">%s</span></div>' % (t, I(ic, 24), m) for t, ic, m in [
        ('success', 'verify', 'تم حفظ التغييرات بنجاح'), ('info', 'info-circle', 'يتم تحديث البيانات كل ساعة'), ('warning', 'danger', 'بعض الحقول تحتاج مراجعة'), ('error', 'information', 'تعذّر إرسال الخطة، حاول مرة أخرى')]) + '</div>'
    rows = [('PL-2026-01', 'خطة التواصل للقمة الخليجية', 'success', 'معتمدة'), ('PL-2026-02', 'حملة التوعية بالميزانية العامة', 'warning', 'بانتظار الاعتماد'), ('PL-2026-03', 'إعلان استراتيجية القطاع الصحي', 'info', 'قيد المراجعة')]
    trs = ''.join('<tr class="table-row"><td><span class="mco-cell--number">%s</span></td><td>%s</td><td><span class="mco-status mco-status--%s"><span class="mco-status__dot" aria-hidden="true"></span>%s</span></td><td><button class="btn btn-cancel btn-small">%s<span>عرض</span></button></td></tr>' % (c, n, s, l, I('eye', 18)) for c, n, s, l in rows)
    P['TABLE'] = '<div class="pv-scroll"><table class="table pv-table"><thead class="table-header"><tr><th>رقم الخطة</th><th>اسم الخطة</th><th>الحالة</th><th><span class="pv-sr">إجراءات</span></th></tr></thead><tbody>%s</tbody></table></div>' % trs
    P['SUBHEADER'] = '<div class="mco-subheader">%s<div class="mco-subheader__actions"><button class="btn btn-primary">%s<span>إضافة خطة</span></button><button class="btn">تصدير</button></div></div>' % (tabs(['الكل', 'المسودات', 'المعتمدة'], 'mco-tabs-filled'), I('add'))
    def dd(id_, label, helper):
        return '<div class="mco-field pv-dd"><label class="mco-field__label" for="%s">%s</label><div id="%s"></div><div class="mco-field__foot">%s</div></div>' % (id_, label, id_, helper)
    P['DROPDOWN'] = '<div class="pv-row pv-top">%s%s</div>' % (dd('vs-one', 'الجهة', 'اختيار واحد مع بحث'), dd('vs-multi', 'الجهات', 'اختيار متعدد'))
    P['CHIPS'] = '<div class="pv-row pv-top">%s</div>' % dd('vs-tags', 'الجهات المشاركة', 'اختر جهة أو أكثر')
    from build_theme import icon_slug
    VX = {icon_slug(k): v for k, v in json.load(open(os.path.join(DEPS, 'vuesax-outline.json'), encoding='utf-8'))['icons'].items()}
    used = sorted(set(list(ICONS) + EXTRA_ICONS + ['check']))
    btn = lambda n: '<button type="button" class="pv-icon" data-copy="%s" title="نسخ رابط SVG">%s<span>%s</span></button>' % (n, I(n, 24), n)
    cats = {}
    for n, v in sorted(VX.items()):
        if n not in used: cats.setdefault(v['category'], []).append(n)
    groups = [('مستخدمة في المكوّنات (في الثيم)', used)] + [(c + ' (MCO_Icons_All.css)', cats[c]) for c in sorted(cats)]
    grid = ''.join('<section class="pv-icat" data-icat><h4 class="pv-icat__t"><span>%s</span> <em>%d</em></h4><div class="pv-icons">%s</div></section>' % (t, len(ns), ''.join(btn(n) for n in ns)) for t, ns in groups)
    grid = '<label class="pv-isearch"><span class="pv-sr">ابحث عن أيقونة</span><input type="search" class="form-control" data-isearch placeholder="ابحث بالاسم (%d أيقونة)" dir="ltr"></label>' % (len(used) + sum(len(v) for v in cats.values())) + grid
    P['ICONGRID'] = '%s<p class="pv-hint" id="copy-msg" role="status">اضغط على أيقونة لنسخ رابط SVG حقها وتنزيلها.</p>' % grid
    return P

# ---------- tree rendering ----------
KIND_OF = lambda w: ('if' if w.startswith(('If', 'Else')) else 'ph' if w.startswith('Placeholder') else 'list' if w.startswith('List')
    else 'block' if w.startswith('MCO_') else 'act' if w.startswith(('Button', 'Link')) else 'expr' if w.startswith(('Expression', 'Text')) else 'html' if w.startswith('HTML') else 'os' if w.startswith(('Popup', 'Table', 'Tabs', 'Dropdown', 'Pagination', 'Checkbox', 'Radio', 'Switch', 'Label', 'Image', 'Message', 'Client', 'Header', 'Row', 'TabsHeader', 'TabsContent')) else 'box')

def render_tree(src):
    lines = [l for l in src.split('\n') if l.strip()]
    items = []
    for l in lines:
        ind = (len(l) - len(l.lstrip(' '))) // 2
        parts = [p.strip() for p in l.strip().split('::')]
        while len(parts) < 3: parts.append('')
        items.append((ind, parts[0], parts[1], parts[2]))
    out = []
    for i, (ind, w, st, note) in enumerate(items):
        # is last sibling at this depth?
        last = True
        for j in range(i + 1, len(items)):
            if items[j][0] < ind: break
            if items[j][0] == ind: last = False; break
        guides = ''
        for d in range(1, ind):
            cont = False
            for j in range(i + 1, len(items)):
                if items[j][0] < d: break
                if items[j][0] == d: cont = True; break
            # ancestor at depth d continues?
            anc_cont = False
            for j in range(i + 1, len(items)):
                if items[j][0] < d + 0: break
                if items[j][0] == d: anc_cont = True; break
            guides += '<i class="g%s"></i>' % (' v' if anc_cont else '')
        if ind > 0:
            guides += '<i class="g %s"></i>' % ('l' if last else 't')
        k = KIND_OF(w)
        st_html = '' if st in ('', '—') else '<code>%s</code>' % html.escape(st)
        note_html = '' if not note else '<span class="n" dir="ltr">%s</span>' % html.escape(note)
        out.append('<div class="tr">%s<span class="w k-%s">%s</span>%s%s</div>' % (guides, k, html.escape(w), st_html, note_html))
    return '<div class="tree" dir="ltr">%s</div>' % ''.join(out)

KIND_LABEL = {OS: ('os', 'نمط OutSystems UI'), BLOCK: ('block', 'Block مخصّص'), MIX: ('mix', 'ودجت المنصة + Block')}

AR = re.compile(r'[؀-ۿ]')
RUN = re.compile(r'[A-Za-z0-9_"\'=+<>(){}\[\]/.:,*#%\-][A-Za-z0-9_"\'=+<>(){}\[\]/.:,*#%\- ·→…]*[A-Za-z0-9_"\')}\]%*…]|[A-Za-z0-9]')
def bidi(t):
    """نص عربي فيه مقاطع إنجليزية: كل مقطع إنجليزي في bdi باتجاه ltr"""
    if not AR.search(t):
        return '<bdi dir="ltr">%s</bdi>' % html.escape(t) if t else ''
    out, last = [], 0
    for m in RUN.finditer(t):
        if not re.search('[A-Za-z]', m.group(0)): continue
        out.append(html.escape(t[last:m.start()])); out.append('<bdi dir="ltr">%s</bdi>' % html.escape(m.group(0))); last = m.end()
    out.append(html.escape(t[last:]))
    return ''.join(out)

def table(head, rows, codecols=()):
    th = ''.join('<th>%s</th>' % h for h in head)
    trs = ''
    for r in rows:
        tds = ''
        for i, c in enumerate(r):
            if i in codecols and c and not AR.search(c): v = '<code dir="ltr">%s</code>' % html.escape(c)
            else: v = bidi(c)
            tds += '<td>%s</td>' % v
        trs += '<tr>%s</tr>' % tds
    return '<div class="tw"><table class="spec"><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (th, trs)

def comp_html(key, num, prev):
    c = C[key]
    kc, kl = KIND_LABEL[c['kind']]; kl = T(kl)
    extra = ''
    if key in NEW: extra += '<span class="new">%s</span>' % T('جديد')
    if c.get('figma'): extra += '<a class="fig" href="%s%s" target="_blank" rel="noopener">%s</a>' % (FIGMA, c['figma'].replace(':', '-'), T('فتح في Figma'))
    parts = ['<article class="comp" id="%s"><header class="ch"><div class="ct"><span class="num">%s</span><h3>%s</h3><code class="mco" dir="ltr">%s</code>%s</div><div class="ch-tools"><button type="button" class="pv-lang" data-pv-lang aria-pressed="false" aria-label="%s"><span data-l="ar" class="on">عربي</span><span data-l="en">EN</span></button><span class="kind kind-%s">%s</span></div></header>' % (key, num, tr(c['name']), c['mco'], extra, T('تبديل المعاينة بين العربي والإنجليزي'), kc, kl)]
    parts.append('<p class="sum">%s</p>' % bidi(tr(c['summary'])))
    parts.append('<div class="pv" aria-label="%s">%s</div>' % (T('معاينة'), prev))
    trr = lambda rows: [tuple(tr(x) for x in r) for r in rows]
    body = []
    if 'variants' in c:
        body.append('<h4>%s</h4>' % T('الاستخدام') + table([T('الحالة'), T('في OutSystems'), T('ملاحظة')], trr(c['variants']), codecols=(1,)))
    if 'inputs' in c:
        rows = trr(c['inputs']) + [('ExtraClass', 'Text', T('كلاسات إضافية على الجذر'))]
        body.append('<h4>Input Parameters</h4>' + table([T('الاسم'), T('النوع'), T('الوصف')], rows, codecols=(0,)))
    if 'events' in c:
        body.append('<h4>Events</h4>' + table([T('الاسم'), T('يمرّر'), ''], [(a, tr(b), '') for a, b in c['events']], codecols=(0,)).replace('<th></th>', '<th class="e"></th>'))
    if 'placeholders' in c:
        body.append('<h4>Placeholders</h4>' + table([T('الاسم'), T('يوضع فيه')], trr(c['placeholders']), codecols=(0,)))
    spec = '<div class="spec-col">%s</div>' % ''.join(body)
    tree = '<div class="tree-col"><h4>%s</h4>%s</div>' % (T('شجرة الودجات') if c['kind'] != OS else T('مثال في Service Studio'), render_tree(tr_tree(c['tree'])))
    parts.append('<div class="build%s">%s%s</div>' % (' os' if (c['kind'] == OS or 'variants' in c) else '', tree, spec))
    if c.get('notes'):
        parts.append('<ul class="notes">%s</ul>' % ''.join('<li>%s</li>' % bidi(tr(n)) for n in c['notes']))
    parts.append('</article>')
    return ''.join(parts)


_PNG_CACHE = {}
def svg_imgs_to_png(page):
    """صور <img> بصيغة SVG (أعلام وصور توضيحية في المعاينات) تتحوّل PNG، لأن المشاركة العامة في Claude ما تقبل صور SVG."""
    import base64
    uris = sorted(set(re.findall(r'<img[^>]*?src="(data:image/svg\+xml[^"]*)"', page)))
    todo = [u for u in uris if u not in _PNG_CACHE]
    if todo:
        with sync_playwright() as p:
            b = p.chromium.launch(); pg = b.new_page(device_scale_factor=3)
            for u in todo:
                pg.set_content('<html><body style="margin:0;background:transparent"><img id="i" src="%s" style="display:block;width:120px"></body></html>' % html.escape(u, quote=True))
                pg.wait_for_timeout(50)
                png = pg.locator('#i').screenshot(omit_background=True)
                _PNG_CACHE[u] = 'data:image/png;base64,' + base64.b64encode(png).decode()
            b.close()
    for u in uris:
        page = page.replace('src="%s"' % u, 'src="%s"' % _PNG_CACHE[u])
    return page

def build():
    global LANG
    rp = {k: to_os(v) for k, v in render_react().items()}
    op = os_previews()
    op.update(previews_extra.build(I))
    # قالب الصفحة يأخذ القائمة الجانبية المحدّثة (2.3) والتذييل (MCO_Footer) نفسهما
    if 'LAYOUT' in rp:
        rp['LAYOUT'] = rp['LAYOUT'].replace('<div class="pv-sideslot"></div>', op['SIDEONE'])
        rp['LAYOUT'] = re.sub(r'<footer class="mco-shell__footer">.*?</footer>', '<div class="mco-shell__footer">%s</div>' % op['FOOTER'], rp['LAYOUT'], flags=re.S)
    # نوع stepper الجديد في شريط التنقل (Figma navbar 2:20663) بعد الأنواع الثلاثة من bundle.js
    if 'NAVBAR' in rp and rp['NAVBAR'].endswith('</div>'):
        rp['NAVBAR'] = rp['NAVBAR'][:-len('</div>')] + op['NAVSTEPPER'] + '</div>'
    # الحوار المضمّن الصغير بزر جانبي (Figma 1021:8123) تحت أمثلة MCO_InlineDialog
    if 'dialog' in rp and rp['dialog'].endswith('</div>'):
        rp['dialog'] = rp['dialog'][:-len('</div>')] + op['DLGSMALL'] + '</div>'
    for LANG in ('ar', 'en'):
        page_for(rp, op)

def page_for(rp, op):
    def prev(key):
        c = C[key]
        if 'preview_js' in c: return rp[key]
        p = c['preview']
        return rp.get(p) or op[p]
    toc = []; secs = []
    used = [k for s_ in SECTIONS for g in s_['groups'] for k in g['items']]  # المحذوف من الأقسام ما يُحسب
    n_os = sum(1 for k in used if C[k]['kind'] == OS); n_blk = len(used) - n_os
    for si, s in enumerate(SECTIONS, 1):
        g_html = []; toc_groups = []
        ci = 0
        for g in s['groups']:
            items = []
            for key in g['items']:
                ci += 1
                items.append(comp_html(key, '%d.%d' % (si, ci), prev(key)))
            toc_groups.append('<div class="tg"><span>%s</span>%s</div>' % (tr(g['title']), ''.join('<a href="#%s">%s%s</a>' % (k, tr(C[k]['name']), ' <i class="tnew">%s</i>' % T('جديد') if k in NEW else '') for k in g['items'])))
            g_html.append('<section class="grp"><h3 class="gt">%s</h3>%s</section>' % (tr(g['title']), ''.join(items)))
        count = sum(len(g['items']) for g in s['groups'])
        sn = '%s %s' % (T('القسم'), T(['الأول', 'الثاني'][si - 1]))
        toc.append('<div class="ts"><a class="tsh" href="#%s"><b>%s</b> %s <em>%d %s</em></a>%s</div>' % (s['id'], sn, tr(s['title']), count, T('مكوّناً'), ''.join(toc_groups)))
        secs.append('<section class="sec" id="%s"><header class="sh"><span class="eyebrow">%s</span><h2>%s</h2><p>%s</p></header>%s</section>' % (s['id'], sn, tr(s['title']), bidi(tr(s['lead'])), ''.join(g_html)))

    conv = rd(GUIDE, 'conventions_en.html' if LANG == 'en' else 'conventions.html')
    page = rd(GUIDE, 'shell.html')
    if LANG == 'en':
        for a, b in SHELL_EN:
            if a not in page: print('SHELL_EN miss:', a[:60])
            page = page.replace(a, b)
    page = page.replace('/*OSUI*/', osui).replace('/*THEME*/', theme + '\n' + rd(HERE, '..', 'MCO_Icons_All.css'))
    page = page.replace('/*I18N*/', json.dumps(json.load(open(GUIDE + '/i18n_en.json')), ensure_ascii=False).replace('</', '<\\/'))
    page = page.replace('<!--TOC-->', ''.join(toc)).replace('<!--CONV-->', conv).replace('<!--SECTIONS-->', ''.join(secs))
    import datetime
    page = page.replace('{UPDATED}', datetime.date.today().strftime('%Y-%m-%d'))
    page = page.replace('{N_OS}', str(n_os)).replace('{N_BLK}', str(n_blk)).replace('{N_ALL}', str(len(used)))
    import os
    out = OUT_EN if LANG == 'en' else OUT
    # كل نسخة صفحة كاملة (doctype وhead)، لأن ar.html تُنشر كملف بجانب index.html
    hl = 'lang="en" dir="ltr"' if LANG == 'en' else 'lang="ar" dir="rtl"'
    page = '<!doctype html>\n<html %s>\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n' % hl + page.replace('</style>', '</style>\n</head>\n<body>', 1) + '\n</body>\n</html>\n'
    if LANG == 'en' and MISSING:
        print('EN MISSING', len(MISSING))
        json.dump(sorted(MISSING), open(os.path.join(HERE, '..', 'en_missing.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(page)
    print('written', LANG, len(page), 'os', n_os, 'blocks', n_blk)

if __name__ == '__main__':
    build()
