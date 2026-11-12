# -*- coding: utf-8 -*-
"""معاينات المكوّنات اللي ما لها مقابل في bundle.js (مكوّنات Figma الجديدة وتحديثاتها).
كل معاينة HTML بنفس الكلاسات اللي تبنيها شجرة الودجات، وأزرارها btn من OutSystems UI."""
import base64, os, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', 'assets')

def _data(name, mime='image/png'):
    with open(os.path.join(ASSETS, name), 'rb') as f:
        return 'data:%s;base64,%s' % (mime, base64.b64encode(f.read()).decode())

def build(I):
    emblem = _data('emblem.png')
    art = _data('plan-illustration.png')
    P = {}

    def stat(icon, label, value, sm=False):
        return ('<div class="mco-stat%s"><div class="mco-stat__icon">%s</div><div class="mco-stat__text">'
                '<span class="mco-stat__label">%s</span><span class="mco-stat__value" dir="ltr">%s</span></div></div>') % (' mco-stat--sm' if sm else '', I(icon, 24), label, value)

    stats3 = stat('medal', 'عدد الأهداف', '4') + stat('sms', 'عدد أنشطة التواصل', '10') + stat('calendar', 'تاريخ تقديم الخطة', '22-05-2026', True)
    ld = lambda c: '<span class="mco-loader%s" role="status" aria-label="جارٍ التحميل"><span class="mco-loader__level"><span class="mco-loader__fill"></span></span></span>' % c
    P['LOADER'] = ('<div class="pv-row" style="align-items:flex-end;gap:40px">'
                   '<div class="pv-stack" style="align-items:center"><span class="pv-k">sm</span>%s</div>'
                   '<div class="pv-stack" style="align-items:center"><span class="pv-k">default</span>%s</div>'
                   '<div class="pv-stack" style="align-items:center"><span class="pv-k">lg · صفحة كاملة</span><div style="display:flex;flex-direction:column;align-items:center;gap:var(--space-24)">%s<p class="mco-loader-page__label">جارٍ التحميل</p></div></div></div>') % (ld(' mco-loader--sm'), ld(''), ld(' mco-loader--lg'))
    P['STAT'] = '<div class="mco-summary__stats">%s</div>' % stats3

    tabs = lambda items, act: '<div class="osui-tabs osui-tabs--is-horizontal mco-tabs-main"><div class="osui-tabs__header pv-tabs" role="tablist">%s</div></div>' % ''.join(
        '<button type="button" role="tab" class="osui-tabs__header-item%s" aria-selected="%s">%s<span>%s</span></button>' % (
            ' osui-tabs--is-active' if i == act else '', 'true' if i == act else 'false', I(ic, 24), t) for i, (ic, t) in enumerate(items))
    P['MAINTABS'] = '<div class="pv-stack"><span class="pv-k">تبويبان</span>%s<span class="pv-k">4 تبويبات</span>%s</div>' % (
        tabs([('record-circle', 'أطر التواصل'), ('element-3', 'خطط التواصل')], 0),
        tabs([('element-3', 'الأهداف'), ('element-3', 'المؤشرات'), ('element-3', 'المبادرات'), ('element-3', 'الأنشطة')], 0))

    usercard = ('<div class="mco-usercard"><div class="mco-usercard__who"><span class="mco-usercard__avatar" aria-hidden="true">م ع</span>'
                '<div class="mco-usercard__text"><span class="mco-usercard__name">محمد أحمد عبدالله</span><span class="mco-usercard__role">مدير وزارة الاستثمار</span></div></div>'
                '<div class="mco-usercard__links"><button type="button" class="mco-usercard__link">%s<span>إعدادات</span></button>'
                '<button type="button" class="mco-usercard__link mco-usercard__link--danger">%s<span>خروج</span></button></div></div>') % (I('setting-2', 14), I('logout', 14))
    P['USERCARD'] = '<div style="width:255px;max-width:100%%">%s</div>' % usercard

    items = [('home', 'الرئيسية', False), ('task-square', 'أعمال التواصل الخارجي', True), ('calendar-2', 'التقويم الشامل', False),
             ('backward-item', 'المركز المعرفي', False), ('notification', 'إدارة الإشعارات', False), ('note', 'التقارير', False)]
    def side(collapsed):
        lis = ''.join('<li class="mco-side__li"><button type="button" class="mco-side__item%s"%s>%s%s</button></li>' % (
            ' is-active' if a else '', ' aria-current="page"' if a else '', I(ic, 24), '<span class="mco-side__label">%s</span>' % t) for ic, t, a in items)
        return ('<nav class="mco-side%s" aria-label="القائمة الرئيسية"><div class="mco-side__top"><div class="mco-side__logo"><div class="mco-side__brand">'
                '<img src="%s" alt="شعار المملكة"><span>منصة تواصل الوزراء</span></div></div><ul class="mco-side__list">%s</ul></div>'
                '<div class="mco-side__bottom">%s<button type="button" class="mco-iconbtn mco-side__collapse" data-pv-collapse aria-expanded="%s" aria-label="%s">%s</button></div></nav>') % (
            ' is-collapsed' if collapsed else '', emblem, lis, usercard, 'false' if collapsed else 'true', 'فتح القائمة' if collapsed else 'طي القائمة', I('collapse-menu' if collapsed else 'expand-menu', 24))
    P['SIDEMENU2'] = '<div class="pv-row pv-top">%s%s</div>' % (side(False), side(True))
    P['SIDEONE'] = side(False)

    P['SUMMARY'] = ('<div class="mco-summary"><div class="mco-summary__main"><div class="mco-summary__head"><h2 class="mco-summary__title">الخطة السنوية لعام 2026</h2>'
                    '<span class="mco-status mco-status--success"><span class="mco-status__dot" aria-hidden="true"></span>معتمدة</span></div>'
                    '<div class="mco-summary__stats">%s</div><div class="mco-summary__actions">'
                    '<button class="btn btn-primary btn-small">%s<span>الأهداف الاستراتيجية</span></button>'
                    '<button class="btn btn-small">%s<span>أولويات الدول</span></button>'
                    '<button class="btn btn-small">%s<span>عرض التقويم</span></button></div></div>'
                    '<img class="mco-summary__art" src="%s" alt=""></div>') % (stats3, I('task-square', 20), I('global', 20), I('calendar', 20), art)

    def field(icon, label, value):
        return ('<div class="mco-slide__field"><div class="mco-slide__tile">%s</div><div class="mco-slide__text"><span class="mco-slide__label">%s</span>'
                '<span class="mco-slide__value">%s</span></div></div>') % (I(icon, 24), label, value)
    def procs(edit=True, delete=True, toggle=True, open_=False):
        inner = ''
        if edit: inner += '<button type="button" class="mco-iconbtn" aria-label="تعديل">%s</button>' % I('edit-2', 20)
        if delete: inner += '<button type="button" class="mco-iconbtn mco-iconbtn--danger" aria-label="حذف">%s</button>' % I('trash', 20)
        if (edit or delete) and toggle: inner += '<span class="mco-slide__sep"></span>'
        if toggle: inner += '<button type="button" class="mco-slide__toggle" aria-expanded="%s" aria-label="%s">%s</button>' % (
            'true' if open_ else 'false', 'طي' if open_ else 'توسيع', I('arrow-down', 24, 'mco-rot' if open_ else ''))
        return '<div class="mco-slide__procs%s">%s</div>' % ('' if (edit or delete) else ' is-bare', inner)
    two = field('archive', 'اسم التصنيف', 'تعزيز العلاقات الدبلوماسية') + field('archive', 'اسم التصنيف', 'رفع مستوى التواصل')
    one = field('archive', 'اسم التصنيف', 'تعزيز العلاقات الدبلوماسية')
    def slide(fields, tools, open_=False, body=''):
        return '<div class="mco-slide%s"><div class="mco-slide__head"><div class="mco-slide__fields">%s</div><div class="mco-slide__tools">%s</div></div>%s</div>' % (
            ' is-open' if open_ else '', fields, tools, '<div class="mco-slide__body">%s</div>' % body if open_ else '')

    long_txt = ('من أبرز التحديات والمخاطر المحتملة: تفاوت مستوى الوعي بين الشرائح المستهدفة، ووجود معلومات غير دقيقة في بعض القنوات الإعلامية، '
                'ومحدودية التنسيق بين بعض الجهات ذات العلاقة، بالإضافة إلى التغييرات في البيئة الخارجية التي قد تؤثر على توقيت الرسائل وأولوياتها. ') * 4
    short_txt = 'تحقيق التكامل بين الجهات المشاركة، ووضوح الرسائل الرئيسية، والالتزام بالجدول الزمني المعتمد للأنشطة.'
    def dcard(title, body):
        return '<section class="mco-dcard"><h3 class="mco-dcard__title">%s</h3><div class="mco-dcard__body">%s</div></section>' % (title, body)
    xtext = ('<div class="mco-xtext is-clamped" data-xtext><p class="mco-xtext__text">%s</p><button type="button" class="btn btn-tertiary btn-small" aria-expanded="false" data-xtoggle>'
             '%s<span>عرض المزيد</span></button></div>') % (long_txt, I('arrow-down', 18))
    info = ('<dl class="mco-info mco-info--lg">' + ''.join('<div class="mco-kv mco-info__item"><dt class="mco-kv__k">%s</dt><dd class="mco-kv__v">%s</dd></div>' % kv for kv in [
        ('الحد الأدنى لعدد الأنشطة خلال السنة', '4'), ('الحد الأدنى لأنشطة الظهور الإعلامي', '3'), ('الحد الأدنى لأنشطة الفعاليات والأحداث', '5'), ('متوسط المستهدف من الأنشطة لكل زيارة', '2')]) + '</dl>')
    table = ('<div class="pv-scroll"><table class="table pv-table"><thead class="table-header"><tr><th>رقم الموعد</th><th>الجهة</th><th>نوع الزيارة</th><th>الحالة</th></tr></thead><tbody>'
             '<tr class="table-row"><td><span class="mco-cell--number">123456</span></td><td>وزارة الاستثمار</td><td>زيارة رسمية</td><td><span class="mco-status mco-status--warning"><span class="mco-status__dot" aria-hidden="true"></span>بانتظار الاعتماد</span></td></tr>'
             '</tbody></table></div>')
    gallery = ('<div class="mco-gallery" role="region" aria-label="صور النشاط"><button type="button" class="mco-gallery__nav" aria-label="السابق" data-gal="1">%s</button>'
               '<div class="mco-gallery__track">%s</div><button type="button" class="mco-gallery__nav" aria-label="التالي" data-gal="-1">%s</button></div>') % (
        I('arrow-left', 24, 'mco-flip'), ''.join('<div class="mco-gallery__item pv-ph" aria-label="صورة %d">%s</div>' % (n, I('gallery', 32)) for n in range(1, 6)), I('arrow-left', 24))
    def person(name, role, place, ini):
        return ('<div class="mco-person"><div class="mco-person__avatar"><span class="mco-person__initials" aria-hidden="true">%s</span></div><div class="mco-person__info">'
                '<span class="mco-person__name">%s</span><span class="mco-person__role">%s</span><span class="mco-person__place">%s<span>%s</span></span></div></div>') % (ini, name, role, I('location', 14), place)
    persons = ('<div class="mco-person-group"><div class="mco-person-group__col"><h4 class="mco-person-group__title">الطرف السعودي</h4>%s</div>'
               '<div class="mco-person-group__col"><h4 class="mco-person-group__title">الطرف النظير</h4>%s</div></div>') % (
        person('خالد العتيبي', 'وكيل وزارة الاستثمار', 'المملكة العربية السعودية', 'خ ع'), person('سارة الأحمد', 'وزيرة الاقتصاد', 'دولة الكويت', 'س أ'))

    P['DCARD'] = '<div class="pv-stack">%s</div>' % ''.join([
        dcard('أبرز عوامل النجاح', '<p class="mco-xtext__text">%s</p>' % short_txt), dcard('الملخص التنفيذي للزيارة', xtext),
        dcard('مؤشرات الطرف النظير', info), dcard('مواعيد الطرف النظير', table), dcard('صور النشاط', gallery), dcard('بيانات الأطراف', persons)])
    P['XTEXT'] = xtext
    P['GALLERY'] = gallery
    P['PERSON'] = persons

    P['SLIDE'] = '<div class="pv-stack">%s</div>' % ''.join([
        '<span class="pv-k">حقلان مع أدوات</span>', slide(two, procs()),
        '<span class="pv-k">حقل واحد</span>', slide(one, procs(False, False)),
        '<span class="pv-k">مع زر</span>', slide(two, '<button class="btn btn-mobile">%s<span>اضغط هنا</span>%s</button>' % (I('user', 20), I('arrow-left', 20)) + procs(False, False)),
        '<span class="pv-k">مفتوحة (اضغط زر الانسدال في أي بطاقة)</span>', slide(two, procs(open_=True), True, dcard('أبرز عوامل النجاح', '<p class="mco-xtext__text">%s</p>' % short_txt) + dcard('بيانات الأطراف', persons))])

    P['ADDBANNER'] = ('<div class="pv-stack">' + ''.join(
        ('<div class="mco-addbanner"><div class="mco-addbanner__tile">%s</div><div class="mco-addbanner__content"><h3 class="mco-addbanner__title">%s</h3>'
         '<div class="mco-addbanner__progress"><div class="mco-addbanner__steps" aria-hidden="true">%s</div><div class="mco-addbanner__meta"><b>%d من 4</b> %s</div></div></div>%s</div>') % (
            I('record-circle', 28), t, ''.join('<span class="mco-addbanner__step%s"></span>' % (' is-done' if i < cur else '') for i in range(4)), cur, h,
            '<button class="btn">%s<span>إضافة هدف</span></button>' % I('record-circle', 20) if cur < 4 else '')
        for t, cur, h in [('هل تريد إضافة هدف استراتيجي آخر؟', 1, 'أهداف · يمكنك إضافة 3 أهداف أخرى'), ('اكتملت الأهداف الاستراتيجية', 4, 'أهداف · وصلت للحد الأقصى')]) + '</div>')

    # الجدول كما في Figma: تصفية فوقه، وزران في كل صف، وتذييل تحته
    rows = [('123456', 'وزارة الخارجية', 'زيارة رسمية', 'warning', 'بانتظار الاعتماد'), ('123457', 'وزارة المالية', 'اجتماع ثنائي', 'success', 'معتمد'), ('123458', 'وزارة الصحة', 'مؤتمر', 'info', 'قيد المراجعة')]
    trs = ''.join(('<tr class="table-row"><td><span class="mco-cell--number">%s</span></td><td>%s</td><td>%s</td><td><span class="mco-status mco-status--%s"><span class="mco-status__dot" aria-hidden="true"></span>%s</span></td>'
                   '<td><div class="pv-acts"><button class="btn">%s<span>اضغط هنا</span></button><button class="btn btn-primary">%s<span>اضغط هنا</span></button></div></td></tr>') % (c, e, t, s, l, I('user', 20), I('user', 20)) for c, e, t, s, l in rows)
    pag = ('<div class="pagination-container" role="navigation" aria-label="ترقيم الصفحات"><button class="pagination-button" disabled aria-label="السابق">%s</button><button class="pagination-button is--active" aria-current="page">1</button>'
           '<button class="pagination-button">2</button><button class="pagination-button">3</button><button class="pagination-button is--ellipsis" tabindex="-1">…</button><button class="pagination-button">10</button>'
           '<button class="pagination-button" aria-label="التالي">%s</button></div>') % (I('arrow-left', 20, 'mco-flip'), I('arrow-left', 20))
    P['TABLE2'] = ('<div class="pv-stack" style="gap:32px"><div class="mco-filterbar" role="search"><div class="mco-filterbar__search"><input class="form-control pv-w100" placeholder="ابحث برقم الموعد أو الجهة" aria-label="بحث"></div>'
                   '<div class="mco-filterbar__fields"><select class="form-control pv-w100" aria-label="الجهة"><option>كل الجهات</option></select><select class="form-control pv-w100" aria-label="النوع"><option>كل الأنواع</option></select>'
                   '<select class="form-control pv-w100" aria-label="الحالة"><option>كل الحالات</option></select><input class="form-control pv-w100" placeholder="التاريخ" aria-label="التاريخ"></div></div>'
                   '<div class="pv-scroll"><table class="table pv-table pv-wide"><thead class="table-header"><tr><th>رقم الموعد</th><th>الجهة</th><th>نوع الزيارة</th><th>الحالة</th><th><span class="pv-sr">إجراءات</span></th></tr></thead><tbody>%s</tbody></table></div>'
                   '<div class="mco-pfooter">%s<label class="mco-pfooter__size"><select aria-label="عدد النتائج"><option>عدد النتائج 12</option><option>عدد النتائج 24</option></select>%s</label></div></div>') % (trs, pag, I('chevron-down', 18))
    # 9.11 / 9.12 بطاقة قسم النموذج والحالة الفارغة
    def fsec(body):
        return ('<section class="mco-fsection"><header class="mco-fsection__head">%s<h3 class="mco-fsection__title">العناصر التنفيذية</h3></header>'
                '<div class="mco-fsection__body">%s</div></section>') % (I('category-2', 29), body)
    def tf(i, label, ph):
        return ('<div class="mco-field mco-field--text"><label class="mco-field__label" for="fs%d">%s</label><div class="mco-field__box">'
                '<input id="fs%d" class="mco-field__control" type="text" placeholder="%s"></div></div>') % (i, label, i, ph)
    def sel(i, label):
        return ('<div class="mco-field mco-field--select"><label class="mco-field__label" for="fs%d">%s</label><div class="mco-field__box">'
                '<select id="fs%d" class="mco-field__control"><option value="">النص الإرشادي</option><option>خيار 1</option></select>'
                '<span class="mco-field__trail">%s</span></div></div>') % (i, label, i, I('chevron-down', 22))
    alert = ('<div class="mco-alert mco-alert--info" role="status"><span class="mco-status-icon mco-status-icon--40 mco-status-icon--info">%s</span>'
             '<div class="mco-alert__body"><div class="mco-alert__title">إخطار لتزويد المستخدم بتذكيرات</div><div class="mco-alert__text"><span>توجيه الإخطارات للمستخدمين وإعلامهم بالتحديثات</span></div></div>'
             '<button type="button" class="mco-iconbtn" aria-label="إغلاق">%s</button></div>') % (I('info-circle', 24), I('close', 24))
    grid = '<div class="mco-fsection__grid">%s%s%s%s</div>' % (sel(1, 'تصنيف الاستقبال'), tf(2, 'الهدف الرئيسي', 'مثال'), sel(3, 'الهدف الفرعي'), tf(4, 'الدولة', 'مثال'))
    empty = ('<div class="mco-empty"><div class="mco-empty__top"><span class="mco-empty__icon">%s</span><p class="mco-empty__text">لا يوجد عناصر تنفيذية مضافة، يمكنك إضافة عنصر تنفيذي</p></div>'
             '<button type="button" class="btn btn-primary"><span>إضافة</span>%s</button></div>') % (I('element-plus', 39), I('arrow-left', 20))
    P['FSECTION'] = fsec(alert + grid)
    P['EMPTY'] = fsec(empty)

    # 9.13 التذييل
    crest = _data('mini-crest.png')
    P['FOOTER'] = ('<footer class="mco-footer"><div class="mco-footer__brand"><img class="mco-footer__crest" src="%s" alt="">'
                   '<span>جميع الحقوق محفوظة © 2026 لمنصة تواصل الوزراء</span></div>'
                   '<nav class="mco-footer__links" aria-label="روابط التذييل"><a class="mco-footer__link" href="#">الشروط والأحكام</a>'
                   '<a class="mco-footer__link" href="#">سياسة الخصوصية</a></nav></footer>') % crest

    # 9.14 بطاقة السجل
    rf = lambda l, v: '<div class="mco-record__field"><span class="mco-record__label">%s</span><span class="mco-record__value">%s</span></div>' % (l, v)
    P['RECORD'] = ('<article class="mco-record"><div class="mco-record__fields">%s%s%s%s</div><div class="mco-record__actions">'
                   '<button type="button" class="btn"><span>عرض التفاصيل</span>%s</button>'
                   '<button type="button" class="btn btn-tertiary">%s<span>تعديل</span></button>'
                   '<button type="button" class="btn btn-tertiary btn-destructive">%s<span>حذف</span></button></div></article>') % (
        rf('هدف التواصل الاستراتيجي المرتبط', 'هدف التواصل'), rf('التصنيف الفرعي', 'نشاط فرعي'), rf('التصنيف الرئيسي', 'فئة نشاط'),
        '<div class="mco-record__field"><span class="mco-record__label">تاريخ النشاط</span><span class="mco-record__value">22-05-2026</span></div>',
        I('arrow-left', 20), I('card-edit', 20), I('trash', 20))


    # ───── 11. تحديث مكتبة Figma (نوفمبر 2026) ─────
    svg = lambda b: 'data:image/svg+xml,' + urllib.parse.quote(b)
    FLAG_PL = svg('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 20"><rect width="30" height="10" fill="#fff"/><rect y="10" width="30" height="10" fill="#dc143c"/></svg>')
    FLAG_DK = svg('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 37 28"><rect width="37" height="28" fill="#c8102e"/><rect x="12" width="4" height="28" fill="#fff"/><rect y="12" width="37" height="4" fill="#fff"/></svg>')
    FLAG_SA = svg('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 20"><rect width="30" height="20" fill="#006c35"/><rect x="8" y="12.5" width="14" height="1.2" rx=".6" fill="#fff"/><path d="M9 6.5h12M9 8.5h10" stroke="#fff" stroke-width="1.1" stroke-linecap="round"/></svg>')
    PHOTO = svg('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 42 42"><rect width="42" height="42" fill="#d6e7f4"/><circle cx="21" cy="17" r="7" fill="#7db6e0"/><path d="M7 40c2-9 8-13 14-13s12 4 14 13" fill="#7db6e0"/></svg>')
    # 11.2 مؤشر الخطوات الدائري
    def csteps(states, extra=''):
        n = len(states); out = []
        for i, st in enumerate(states):
            if i: out.append('<li class="mco-csteps__line" aria-hidden="true"></li>')
            dot = I('check', 16) if st == 'done' else str(i + 1)
            out.append('<li class="mco-cstep%s"%s><span class="mco-cstep__dot">%s</span><span class="mco-cstep__text"><span class="mco-cstep__caption">الخطوة %d من %d</span><span class="mco-cstep__title">عنوان الخطوة</span></span></li>' % (
                {'done': ' is-done', 'active': ' is-active'}.get(st, ''), ' aria-current="step"' if st == 'active' else '', dot, i + 1, n))
        return '<ol class="mco-csteps%s" aria-label="خطوات النموذج">%s</ol>' % (extra, ''.join(out))
    P['CSTEPS'] = '<div class="pv-stack"><span class="pv-k">الخطوة الأولى</span>%s<span class="pv-k">الخطوة الثانية</span>%s</div>' % (csteps(['active', 'todo', 'todo']), csteps(['done', 'active', 'todo']))
    P['NAVSTEPPER'] = ('<header class="mco-nav"><div class="mco-nav__bar"><div class="mco-nav__tools"><button aria-label="الإشعارات" class="mco-nav__tool" type="button">%s</button>'
                       '<button aria-label="بحث" class="mco-nav__tool" type="button">%s</button><button aria-label="الوضع الداكن" class="mco-nav__tool" type="button">%s</button></div></div>'
                       '<div class="mco-nav__body"><nav aria-label="مسار التنقل" class="mco-crumbs">%s%s<a href="#">أجندة التواصل</a>%s<span aria-current="page">خطة التواصل السنوية</span></nav>'
                       '<div class="mco-nav__titlerow"><button aria-label="رجوع" class="mco-nav__back" type="button">%s</button><h1 class="mco-nav__title">الأهداف الاستراتيجية</h1>'
                       '<button class="btn btn-primary btn-mobile" type="button">%s<span>اضغط هنا</span>%s</button></div></div>%s</header>') % (
        I('notification-bing', 24), I('search-normal', 24), I('moon', 24), I('home', 16), I('arrow-left', 12), I('arrow-left', 12), I('arrow-left', 24, 'mco-flip'),
        I('user', 20), I('arrow-left', 20), csteps(['active', 'todo', 'todo'], ' mco-nav__steps'))
    # 11.4 حقل المعلومة
    ifield = lambda l, v: '<div class="mco-ifield"><span class="mco-ifield__label">%s</span><span class="mco-ifield__value">%s</span></div>' % (l, v)
    ifield_c = lambda l, v, f: '<div class="mco-ifield"><span class="mco-ifield__label">%s</span><span class="mco-ifield__value"><img class="mco-ifield__flag" src="%s" alt="">%s</span></div>' % (l, f, v)
    ifield_chip = lambda l, v: '<div class="mco-ifield"><span class="mco-ifield__label">%s</span><span class="mco-ifield__chip">%s</span></div>' % (l, v)
    P['IFIELD'] = '<div class="pv-row" style="gap:48px">%s%s%s</div>' % (ifield('عنوان الحقل', 'قيمة الحقل'), ifield_c('الدولة', 'المملكة العربية السعودية', FLAG_SA), ifield_chip('تصنيف الزيارة', 'زيارة رسمية'))
    # 11.3 بطاقة السجل (تحديث)
    acts = lambda view: ('<div class="mco-record__actions">%s<div class="mco-record__tools"><button type="button" class="btn btn-tertiary">%s<span>تعديل</span></button>'
                         '<button type="button" class="btn btn-tertiary btn-destructive">%s<span>حذف</span></button></div></div>') % (
        '<button type="button" class="btn"><span>عرض التفاصيل</span>%s</button>' % I('arrow-left', 20) if view else '', I('card-edit', 20), I('trash', 20))
    purpose = ('<div class="mco-record__purpose is-clamped" data-rpurpose><span class="mco-ifield__label">الغرض من الزيارة</span><p class="mco-record__purpose-text">تعزيز العلاقات الثنائية بين المملكة العربية السعودية وجمهورية بولندا، وبحث فرص التعاون في مجالات الاستثمار والطاقة والتعليم، إلى جانب عقد لقاءات مع عدد من المسؤولين الحكوميين وممثلي القطاع الخاص لاستعراض مستهدفات رؤية المملكة 2030 وفرص الشراكة المستقبلية بين البلدين في القطاعات ذات الأولوية، والاتفاق على آلية متابعة مشتركة لتنفيذ مخرجات الزيارة خلال العام القادم.</p>'
               '<button type="button" class="mco-record__more" aria-expanded="false"><span>عرض المزيد</span>%s</button></div>') % I('arrow-down', 16)
    visit = '<div class="mco-record__body"><div class="mco-record__fields">%s%s%s%s%s</div>%s</div>' % (
        ifield_c('الدولة', 'بولندا', FLAG_PL), ifield_chip('تصنيف الزيارة', 'زيارة رسمية'), ifield('تاريخ بداية الزيارة', '23-06-2026'), ifield('تاريخ نهاية الزيارة', '26-06-2026'), ifield('مدة الزيارة', '4 أيام'), purpose)
    P['RECORD'] = '<div class="pv-stack"><span class="pv-k">افتراضي</span><article class="mco-record"><div class="mco-record__fields">%s%s%s%s</div>%s</article><span class="pv-k">زيارة (اضغط «عرض المزيد»)</span><article class="mco-record">%s%s</article></div>' % (
        ifield('تاريخ النشاط', '22-05-2026'), ifield('التصنيف الرئيسي', 'فئة نشاط'), ifield('التصنيف الفرعي', 'نشاط فرعي'), ifield('هدف التواصل الاستراتيجي المرتبط', 'هدف التواصل'), acts(True), visit, acts(False))
    # 11.5 شريط الإضافة بزرّين
    two = ('<div class="mco-addbanner"><div class="mco-addbanner__tile">%s</div><div class="mco-addbanner__content"><h3 class="mco-addbanner__title">هل تريد إضافة هدف استراتيجي آخر؟</h3></div>'
           '<div class="mco-addbanner__actions"><button class="btn">%s<span>إعادة بملاحظات</span></button><button class="btn btn-primary">%s<span>قبول الطلب</span></button></div></div>') % (I('record-circle', 28), I('back-square', 20), I('verify', 20))
    P['ADDBANNER'] = P['ADDBANNER'][:-len('</div>')] + '<span class="pv-k">بزرّين (قبول أو إعادة)</span>' + two + '</div>'
    # 11.6 الصورة الرمزية
    P['AVATAR'] = ('<div class="pv-row" style="gap:24px"><span class="mco-avatar mco-avatar--image"><img src="%s" alt="محمد أحمد"></span>'
                   '<span class="mco-avatar" role="img" aria-label="مستخدم">%s</span><button type="button" class="mco-avatar" aria-label="إضافة شخص">%s</button></div>') % (PHOTO, I('user', 16), I('profile-add', 16))
    # 11.7 / 11.8 مربع التاريخ وعنصر الحقيقة
    dtile = '<div class="mco-datetile" role="img" aria-label="22 مايو 2026"><span class="mco-datetile__month">مايو</span><span class="mco-datetile__day">22</span><span class="mco-datetile__year">2026</span></div>'
    P['DATETILE'] = '<div class="pv-row">%s</div>' % dtile
    fact = lambda ic, l, v, tone='': '<div class="mco-fact%s"><span class="mco-fact__icon">%s</span><div class="mco-fact__text"><span class="mco-fact__label">%s</span><span class="mco-fact__value">%s</span></div></div>' % (tone, I(ic, 20), l, v)
    status_fact = ('<div class="mco-fact"><div class="mco-fact__text"><span class="mco-fact__label">حالة الطلب</span><span class="mco-status mco-status--warning"><span class="mco-status__dot" aria-hidden="true"></span>بانتظار الاعتماد</span></div></div>')
    P['FACT'] = '<div class="pv-row" style="gap:8px">%s%s%s</div>' % (fact('calendar', 'فترة الزيارة', '22 – 25 مايو 2026'), fact('tick-circle', 'تأكيد التاريخ', 'مؤكد', ' mco-fact--success'), status_fact)
    # 11.9 رأس البطاقة
    P['CARDHEAD'] = '<div class="mco-cardhead"><h3 class="mco-cardhead__title">الأنشطة المرتبطة</h3><span class="mco-cardhead__count">3</span></div>'
    # 11.10 بطاقة النشاط
    kv = lambda l, v: '<div class="mco-activity__kv"><span class="mco-activity__label">%s</span><span class="mco-activity__value">%s</span></div>' % (l, v)
    activity = '<article class="mco-activity"><div class="mco-activity__top">%s%s</div><div class="mco-activity__divider"></div><div class="mco-activity__fields">%s%s</div></article>' % (
        dtile, kv('التصنيف الرئيسي', 'فئة نشاط'), kv('التصنيف الفرعي', 'نشاط فرعي'), kv('هدف التواصل الاستراتيجي المرتبط', 'هدف التواصل'))
    P['ACTIVITY'] = '<div class="pv-stack" style="gap:16px">%s<div class="pv-grid3">%s%s%s</div></div>' % (P['CARDHEAD'].replace('الأنشطة المرتبطة', 'الأنشطة'), activity, activity, activity)
    # 11.11 الحالة الفارغة كبطاقة
    P['EMPTY'] = ('<div class="pv-stack"><span class="pv-k">داخل قسم نموذج (Style = section)</span>%s<span class="pv-k">بطاقة (Style = card)</span>'
                  '<div class="mco-empty mco-empty--card"><div class="mco-empty__top"><span class="mco-empty__icon">%s</span><p class="mco-empty__text">لا يوجد محتوى بعد</p>'
                  '<p class="mco-empty__desc">وصف مختصر لما يحدث هنا وما الخطوة التالية</p></div><button type="button" class="btn btn-primary btn-mobile">%s<span>إجراء</span></button></div></div>') % (
        P['EMPTY'], I('document-upload', 32), I('document-upload', 20))
    # 11.12 عنصر الملف
    file_ = lambda ext, name, notes=True: ('<article class="mco-file"><div class="mco-file__row"><span class="mco-filetype mco-filetype--%s" aria-hidden="true"><span class="mco-filetype__ext">%s</span></span>'
                                          '<div class="mco-file__meta"><span class="mco-file__name" dir="auto">%s</span><span class="mco-file__sub">رُفع في 22-05-2026 · 1.2 ميجابايت</span></div>'
                                          '<div class="mco-file__actions"><button type="button" class="btn">عرض</button><button type="button" class="btn btn-tertiary">تحميل</button></div></div>%s</article>') % (
        ext, ext, name, '<div class="mco-file__notes"><b>الملاحظات:</b><span>نص الملاحظات</span></div>' if notes else '')
    P['FILE'] = '<div class="pv-stack" style="gap:12px">%s%s%s</div>' % (file_('pdf', 'خطة الزيارة.pdf'), file_('doc', 'محضر الاجتماع.docx', False), file_('png', 'صورة الوفد.png', False))
    # 11.13 رأس صفحة التفاصيل
    P['DHEAD'] = ('<section class="mco-dhead"><div class="mco-dhead__top"><div class="mco-dhead__id"><img class="mco-dhead__flag" src="%s" alt="علم الدنمارك"><div class="mco-dhead__text">'
                  '<div class="mco-dhead__titlerow"><h2 class="mco-dhead__title">زيارة الدنمارك</h2><span class="mco-status mco-status--info"><span class="mco-status__dot" aria-hidden="true"></span>قيد المراجعة</span></div>'
                  '<p class="mco-dhead__desc">زيارة رسمية · وزارة الخارجية</p></div></div><button type="button" class="btn btn-cancel btn-mobile">تعديل</button></div>'
                  '<div class="mco-dhead__facts">%s%s%s%s</div></section>') % (FLAG_DK, fact('calendar', 'فترة الزيارة', '22 – 25 مايو 2026'), fact('calendar-2', 'مدة الزيارة', '4 أيام'),
                                                                              fact('tick-circle', 'تأكيد التاريخ', 'مؤكد', ' mco-fact--success'), fact('task-square', 'عدد الأنشطة', '3 أنشطة'))
    # 11.14–11.17 صفحة الخدمة (Sprint-1)
    P['SVCHERO'] = ('<section class="mco-svchero"><div class="mco-svchero__content"><span class="mco-svchero__tag">%s<span>خدمات التواصل الخارجي</span></span>'
                    '<div class="mco-svchero__text"><h3 class="mco-svchero__title">رفع خطة التواصل الخارجي السنوية</h3><p class="mco-svchero__desc">تمكّنك هذه الخدمة من رفع خطة التواصل الخارجي للوزارة، وتتضمن أهداف التواصل الاستراتيجية وأنشطة التواصل المختلفة، مثل الزيارات والاستقبالات والأنشطة الأخرى.</p></div></div>'
                    '<div class="mco-svchero__cta"><h4 class="mco-svchero__cta-title">جاهز للبدء ؟</h4><button type="button" class="btn btn-primary"><span>بدء الخدمة</span>%s</button></div></section>') % (I('global', 24), I('arrow-left', 20))
    phase = lambda ic, label, title, steps, start, actor: ('<article class="mco-phase"><div class="mco-phase__head"><span class="mco-phase__icon">%s</span><div class="mco-phase__heading"><span class="mco-phase__label">%s</span><h4 class="mco-phase__title">%s</h4></div></div>'
                    '<ol class="mco-phase__steps">%s</ol><div class="mco-phase__actor">%s<span>%s</span></div></article>') % (
        I(ic, 24), label, title, ''.join('<li class="mco-phase__step"><span class="mco-phase__num">%d</span><span>%s</span></li>' % (start + i, t) for i, t in enumerate(steps)), I('user', 16), actor)
    p1 = phase('edit', 'المرحلة 1 · الخطوات 1–3', 'إعداد الخطة', ['تحديد عام الخطة', 'إدخال أهداف التواصل الاستراتيجية', 'إدخال بيانات الزيارات والاستقبالات والأنشطة الأخرى'], 1, 'القائم بالأعمال في الوزارة')
    p2 = phase('verify', 'المرحلة 2 · الخطوات 4–5', 'المراجعة والاعتماد', ['موافقة صاحب الصلاحية في الوزارة', 'مراجعة الطلب واعتماده من مكتب تواصل الوزراء'], 4, 'صاحب الصلاحية في الوزارة ومكتب تواصل الوزراء')
    P['PHASE'] = '<div class="pv-row" style="align-items:stretch">%s</div>' % p1
    P['SVCSTEPS'] = '<section class="mco-svcsteps"><div class="mco-svcsteps__head"><h3 class="mco-svcsteps__title">خطوات الخدمة</h3><span class="mco-svcsteps__count">مرحلتان</span></div><div class="mco-svcsteps__grid">%s%s</div></section>' % (p1, p2)
    notice = ('<div class="mco-dialog mco-dialog--warning mco-dialog--left mco-dialog--small" role="alertdialog" aria-label="ملاحظة"><div class="mco-dialog__main"><span class="mco-dialog__icon">%s</span>'
              '<div class="mco-dialog__text"><span class="mco-dialog__title">ملاحظة</span><div class="mco-dialog__body">يرجى تحديث أولويات الدول قبل إنشاء الخطة السنوية، ويمكنك إدارتها بالضغط على «أولويات الدول».</div></div></div>'
              '<div class="mco-dialog__actions"><button type="button" class="btn mco-dialog__cta">أولويات الدول</button></div></div>') % I('danger', 20)
    P['SVCPAGE'] = '<div class="mco-svcpage">%s%s%s</div>' % (notice, P['SVCHERO'], P['SVCSTEPS'])
    return P
