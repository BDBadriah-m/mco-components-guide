# -*- coding: utf-8 -*-
# محتوى دليل مكوّنات MCO لـ OutSystems
# tree: سطر لكل ودجت «Widget :: Style Classes :: ملاحظة»، والمسافتان = مستوى

OS, BLOCK, MIX = 'os', 'block', 'mix'

SECTIONS = [
 {'id': 's1', 'title': 'المكونات الفردية', 'lead': 'العناصر الصغيرة اللي تُستخدم داخل أي شاشة أو Block: الأيقونات والأزرار والحقول وعناصر التنقل.', 'groups': [
  {'title': 'الأساسيات', 'items': ['icon', 'status', 'ctag', 'stat', 'avatar', 'ifield', 'datetile', 'fact']},
  {'title': 'الأزرار', 'items': ['button']},
  {'title': 'حقول الإدخال والاختيار', 'items': ['textfield', 'dropdown', 'chips', 'checkbox', 'radio', 'switch', 'choicecard']},
  {'title': 'عناصر التنقل', 'items': ['tabs', 'maintabs', 'pagination', 'csteps', 'wizard']},
 ]},
 {'id': 's2', 'title': 'المكونات الوظيفية', 'lead': 'مكوّنات مركّبة تؤدي وظيفة كاملة في الصفحة، وتتكوّن غالباً من المكوّنات الفردية.', 'groups': [
  {'title': 'هيكل الصفحة', 'items': ['layout', 'navbar', 'sidemenu', 'usercard', 'subheader', 'actionsbar', 'footer']},
  {'title': 'النماذج', 'items': ['fsection', 'empty']},
  {'title': 'الرسائل والنوافذ', 'items': ['toast', 'popup', 'formpopup', 'dialog', 'loader']},
  {'title': 'عرض البيانات', 'items': ['table', 'filterbar', 'pfooter', 'mcard', 'info', 'points', 'quarters', 'timeline', 'addmore']},
  {'title': 'عرض التفاصيل للقراءة فقط', 'items': ['dhead', 'summary', 'cardhead', 'record', 'activity', 'file', 'slide', 'dcard', 'xtext', 'gallery', 'person', 'addbanner']},
 ]},
]

C = {}

# ───────────────────────── القسم الأول ─────────────────────────

C['icon'] = dict(name='الأيقونة', mco='MCO_Icon', kind=BLOCK,
 summary='أيقونات Vuesax outline كـ CSS: عنصر فارغ بكلاس الأيقونة، ولونها يتبع لون النص.',
 inputs=[('Name', 'Text', 'اسم الأيقونة من القائمة تحت'), ('Size', 'Integer = 24', '12 · 16 · 18 · 20 · 22 · 24 · 32 · 36'),
         ('IsFlipped', 'Boolean = False', 'يعكس الأيقونة أفقياً (سهم «السابق»)'), ('AriaLabel', 'Text', 'فقط إذا كانت الأيقونة تحمل معنى بدون نص')],
 tree='''MCO_Icon :: — :: Block
  Expression :: "mco-icon mco-i-" + Name + " mco-size-" + Size + If(IsFlipped, " mco-flip", "") + " " + ExtraClass :: Value = "" · aria-hidden = If(AriaLabel = "", "true", "false") · role = "img" و aria-label = AriaLabel عند وجوده''',
 notes=['الأحجام: 20 داخل الأزرار، 22 داخل الحقول، 24 في القوائم والتبويبات.',
        '«التالي» = arrow-left، و«السابق» = arrow-left مع IsFlipped = True. لا تستخدم arrow-right للرجوع، فهي في Vuesax سهم داخل مربع.',
        'الأيقونات المستخدمة في المكوّنات موجودة في الثيم نفسه. المجموعة الكاملة (900 أيقونة) في ملف MCO_Icons_All.css: أضفه في الـ Theme كـ Style Sheet ثاني بعد ملف الثيم إذا احتجت أيقونة غير موجودة فيه.'],
 preview='ICONGRID')

C['status'] = dict(name='شارة الحالة', mco='MCO_StatusBadge', kind=BLOCK,
 summary='نص الحالة على خلفية لونها مع نقطة 9px. النص هو حامل المعنى، واللون مساند.',
 inputs=[('Status', 'MCO_Status Identifier', 'default · success · info · warning · danger'), ('Label', 'Text', 'نص الحالة'),
         ('Size', 'Text = "large"', 'large (36px) · small (26px)'), ('ShowDot', 'Boolean = True', '')],
 tree='''MCO_StatusBadge :: — :: Block
  Container :: "mco-status mco-status--" + Status + If(Size = "small", " mco-status--small", "") + " " + ExtraClass
    If :: — :: ShowDot
      Container :: mco-status__dot :: aria-hidden = "true"
    Expression :: — :: Value = Label''',
 preview_js="row([h(M.StatusBadge,null,'مسودة'),h(M.StatusBadge,{status:'success'},'مكتمل'),h(M.StatusBadge,{status:'info'},'قيد المعالجة'),h(M.StatusBadge,{status:'warning'},'بانتظار الاعتماد'),h(M.StatusBadge,{status:'danger'},'مرفوض'),h(M.StatusBadge,{status:'success',size:'small'},'صغير'),h(M.StatusBadge,{status:'info',dot:false},'بدون نقطة')])")

C['ctag'] = dict(name='اسم الدولة أو الجهة', mco='MCO_CountryTag', kind=BLOCK,
 summary='اسم دولة بعلمها (30×20) أو اسم وزارة بشعارها.',
 inputs=[('Name', 'Text', ''), ('FlagURL', 'Text', 'رابط العلم من مجموعة Flags (120×80)')],
 placeholders=[('Mark', 'شعار الوزارة بدل العلم')],
 tree='''MCO_CountryTag :: — :: Block
  Container :: "mco-ctag " + ExtraClass
    If :: — :: FlagURL <> ""
      Image :: mco-ctag__flag :: Type = External URL · URL = FlagURL · Alt = ""
    Else :: — ::
      Placeholder :: — :: Mark
    Expression :: — :: Value = Name''',
 preview_js="row([h(M.CountryTag,{key:1,name:'السعودية',flag:FLAG_SA}),h(M.CountryTag,{key:2,name:'الإمارات',flag:FLAG_AE}),h(M.CountryTag,{key:3,name:'مصر',flag:FLAG_EG})])")

C['button'] = dict(name='الزر', mco='Button', kind=OS,
 summary='ودجت Button حق OutSystems. النوع والحجم يُحددان بالكلاسات في Style Classes فقط.',
 variants=[('أساسي', 'btn btn-primary', 'إجراء واحد أساسي في كل مجموعة'), ('ثانوي', 'btn', ''), ('نصي', 'btn btn-tertiary', ''),
           ('رابط', 'btn btn-link', 'بخط سفلي ووزن عادي'), ('إلغاء', 'btn btn-cancel', 'بجانب الزر الأساسي'),
           ('أساسي خطِر', 'btn btn-error', 'حذف نهائي'), ('ثانوي خطِر', 'btn btn-destructive', ''), ('نصي خطِر', 'btn btn-tertiary btn-destructive', ''),
           ('حجم الجوال 36px', '+ btn-mobile', 'يُضاف لأي نوع'), ('حجم صغير 32px', '+ btn-small', 'داخل الجداول والبطاقات'),
           ('تحميل', '+ mco-btn-loading', 'مع Enabled = False، والمحتوى Container بكلاس mco-btn__dots فيه 3 عناصر فارغة')],
 tree='''Button :: btn btn-primary :: OnClick = …
  MCO_Icon :: — :: Name = "add" · Size = 20 (الأيقونة قبل النص = يمين النص)
  Text :: — :: "إضافة خطة"''',
 notes=['المعطّل: Enabled = False فقط، والثيم يرسم حالته.', 'سهم «التالي» يوضع بعد النص: Text ثم MCO_Icon بـ Name = "arrow-left".',
        'تنبيه تباين: نص الزر الثانوي brand-light على الأبيض 3.8:1، فالإجراءات المهمة تكون بالزر الأساسي.'],
 preview='BUTTONS')

C['textfield'] = dict(name='حقل الإدخال', mco='MCO_TextField', kind=MIX,
 summary='Block يلفّ ودجت الإدخال حق المنصة (Input أو TextArea أو Date Picker أو Upload) ويضيف العنوان والنص المساعد ورسالة الخطأ.',
 inputs=[('InputId', 'Text', 'Id ودجت الإدخال اللي في الـ Placeholder، لربط العنوان والنص المساعد'), ('Label', 'Text', ''),
         ('Type', 'Text = "text"', 'text · textarea · date · file · select (يحدد الأيقونة)'), ('IsRequired', 'Boolean = False', 'يضيف *'),
         ('ShowInfo', 'Boolean = False', 'أيقونة info-circle بجانب العنوان'), ('HelperText', 'Text', ''),
         ('ErrorText', 'Text', 'إذا فيه نص يتحول الحقل لحالة الخطأ'), ('IsDisabled', 'Boolean = False', ''),
         ('HasBox', 'Boolean = True', 'False مع Dropdown لأن له إطاره'), ('MaxLength', 'Integer = 0', 'يظهر العدّاد إذا أكبر من 0'),
         ('CurrentLength', 'Integer = 0', 'طول القيمة الحالية في الحقل'), ('Size', 'Text = "default"', 'default · mobile (خط 16px)')],
 placeholders=[('Input', 'ودجت الإدخال بكلاس mco-field__control بدل form-control')],
 tree='''MCO_TextField :: — :: Block
  Container :: "mco-field mco-field--" + Type + If(ErrorText <> "", " is-error", "") + If(IsDisabled, " is-disabled", "") + If(Size = "mobile", " mco-field--mobile", "") + " " + ExtraClass
    HTML Element (label) :: mco-field__label :: for = InputId
      Expression :: — :: Value = Label
      If :: — :: IsRequired
        Expression :: mco-field__req :: Value = "*"
      If :: — :: ShowInfo
        MCO_Icon :: — :: Name = "info-circle" · Size = 20
    If :: — :: HasBox
      Container :: mco-field__box
        Placeholder :: — :: Input
        If :: — :: Type = "date" أو "file" أو "select"
          Container :: mco-field__trail
            MCO_Icon :: — :: Name = "calendar" / "direct-send" / "chevron-down" · Size = 22
    Else :: — ::
      Placeholder :: — :: Input
    If :: — :: HelperText <> "" or ErrorText <> "" or MaxLength > 0
      Container :: mco-field__foot :: id = InputId + "-help"
        Expression :: — :: Value = If(ErrorText <> "", ErrorText, HelperText)
        If :: — :: MaxLength > 0
          Expression :: mco-field__count :: Value = "بحد أقصى " + MaxLength + " حرف ( " + CurrentLength + "/" + MaxLength + " )"''',
 notes=['التحقق: مرّر ErrorText = If(Input.Valid, "", Input.ValidationMessage). الثيم يخفي رسالة المنصة الافتراضية داخل الحقل حتى لا تتكرر.',
        'التاريخ: نمط Date Picker من OutSystems UI على Input بكلاس mco-field__control.',
        'خارج النماذج (مثل شريط البحث في FilterBar) يكفي Input عادي بكلاس form-control.'],
 preview_js=r"""h('div',{className:'pv-grid3'},
 h(M.TextField,{label:'عنوان الحقل',info:'معلومة',placeholder:'النص الإرشادي',helper:'نص مساعد لتوضيح متطلبات الحقل'}),
 h(M.TextField,{label:'عنوان الحقل',defaultValue:'قيمة مدخلة',error:'هذا الحقل مطلوب'}),
 h(M.TextField,{label:'عنوان الحقل',defaultValue:'قيمة معطلة',disabled:true,helper:'نص مساعد'}),
 h(M.TextField,{type:'date',label:'التاريخ',placeholder:'يوم / شهر / سنة'}),
 h(M.TextField,{type:'file',label:'إرفاق ملف',placeholder:'اسحب الملف أو اضغط للرفع'}),
 h(M.TextField,{type:'textarea',label:'الوصف',maxLength:500,placeholder:'اكتب الوصف'}))""")

C['dropdown'] = dict(name='القائمة المنسدلة', mco='Dropdown Search', kind=OS,
 summary='نمط Dropdown Search من OutSystems UI. الثيم يرسم الصندوق وحقل البحث والخيارات بألوان MCO.',
 variants=[('اختيار واحد', 'Dropdown Search · AllowMultipleSelection = False', ''), ('اختيار متعدد', 'Dropdown Search · AllowMultipleSelection = True', 'الخيارات بمربعات اختيار'),
           ('قائمة بسيطة بدون بحث', 'ودجت Dropdown', 'للقوائم القصيرة (أقل من 7 خيارات)'), ('مع عنوان ونص مساعد', 'داخل MCO_TextField بـ HasBox = False', '')],
 tree='''MCO_TextField :: — :: Label = "الجهة" · HasBox = False · HelperText = "…"
  Dropdown Search :: — :: Prompt = "اختر" · SearchPrompt = "بحث"''',
 preview='DROPDOWN')

C['chips'] = dict(name='الاختيار المتعدد برقائق', mco='Dropdown Tags', kind=OS,
 summary='نمط Dropdown Tags من OutSystems UI. القيم المختارة تظهر رقائق على bg-light-grey.',
 variants=[('اختيار متعدد برقائق', 'Dropdown Tags', ''), ('مع عنوان ونص مساعد', 'داخل MCO_TextField بـ HasBox = False', '')],
 tree='''MCO_TextField :: — :: Label = "الجهات المشاركة" · HasBox = False
  Dropdown Tags :: — :: Prompt = "اختر جهة أو أكثر"''',
 notes=['رقاقة العدّاد «+N» الموجودة في Figma غير مدعومة في النمط، فكل القيم تظهر رقائق.'],
 preview='CHIPS')

C['checkbox'] = dict(name='مربع الاختيار', mco='Checkbox', kind=OS,
 summary='ودجت Checkbox حق المنصة. الثيم يعطيه 26px بزاوية 6px، والمحدد بلون brand-primary.',
 variants=[('عادي ومحدد', 'بدون كلاس', ''), ('خطأ', 'تلقائي عند Valid = False', 'المنصة تضيف not-valid'), ('معطّل', 'Enabled = False', '')],
 tree='''Container :: mco-choice-row
  Checkbox :: — :: Variable = …
  Label :: — :: Input Widget = اسم الـ Checkbox · Text = "أوافق على الشروط"''',
 preview='CHECKBOX')

C['radio'] = dict(name='زر الاختيار الواحد', mco='Radio Group', kind=OS,
 summary='Radio Group مع Radio Button لكل خيار. لخيار واحد من 2 إلى 5 خيارات؛ لأكثر استخدم القائمة المنسدلة.',
 variants=[('عمودي', 'Radio Group بدون كلاس', ''), ('أفقي', 'Radio Group · Style Classes = "radio-group is-horizontal"', ''), ('معطّل', 'Enabled = False', '')],
 tree='''Radio Group :: radio-group is-horizontal :: Variable = …
  Container :: mco-choice-row
    Radio Button :: — :: Value = 1
    Label :: — :: Input Widget = اسم الـ Radio Button · Text = "داخلي"''',
 preview='RADIO')

C['switch'] = dict(name='المفتاح', mco='Switch', kind=OS,
 summary='ودجت Switch: مسار 48×26 ومقبض 22px. لإعداد يُطبَّق فوراً، لا لخيار داخل نموذج يُرسل لاحقاً.',
 variants=[('عادي', 'بدون كلاس', 'في RTL المقبض يساراً عند التشغيل'), ('معطّل', 'Enabled = False', '')],
 tree='''Container :: mco-choice-row
  Switch :: — :: Variable = …
  Label :: — :: Input Widget = اسم الـ Switch · Text = "إشعارات البريد"''',
 preview='SWITCH')

C['choicecard'] = dict(name='الخيار داخل بطاقة', mco='MCO_ChoiceCard', kind=BLOCK,
 summary='صندوق 46px يحمل Checkbox أو Radio Button ونصه. المحدد يأخذ خلفية brand-shade-30.',
 inputs=[('InputId', 'Text', 'Id ودجت الاختيار'), ('Size', 'Text = "default"', 'default (46px) · small (38px)'),
         ('IsError', 'Boolean = False', ''), ('IsDisabled', 'Boolean = False', '')],
 placeholders=[('Input', 'Checkbox أو Radio Button'), ('Label', 'نص الخيار')],
 tree='''MCO_ChoiceCard :: — :: Block
  HTML Element (label) :: "mco-card-choice" + If(Size = "small", " mco-card-choice--small", "") + If(IsError, " is-error", "") + If(IsDisabled, " is-disabled", "") + " " + ExtraClass :: for = InputId
    Placeholder :: — :: Input
    Placeholder :: — :: Label''',
 notes=['الصفّ: Container بكلاس mco-gap-8 وDisplay = flex، وفيه بطاقة لكل خيار.'],
 preview='CHOICECARD')

C['tabs'] = dict(name='التبويبات', mco='Tabs', kind=OS,
 summary='نمط Tabs من OutSystems UI بثلاثة أشكال من Figma، يُختار الشكل بالـ ExtendedClass.',
 variants=[('خط سفلي «Tabs style 2»', 'بدون ExtendedClass', 'الافتراضي'), ('معبّأ «Tabs style 1»', 'ExtendedClass = "mco-tabs-filled"', 'في الرأس الفرعي للصفحة'),
           ('قائمة عمودية «Tabs style 3»', 'ExtendedClass = "mco-tabs-list" · Orientation = Vertical', 'عرض 303px')],
 tree='''Tabs :: — :: ExtendedClass = "mco-tabs-filled"
  TabsHeaderItem :: — :: Text = "الكل"
  TabsContentItem :: — :: محتوى التبويب''',
 preview='TABS')

C['segtabs'] = dict(name='التبويبات المتساوية', mco='MCO_SegmentedTabs', kind=BLOCK,
 summary='تبويبات بعرض متساوٍ داخل بطاقة بيضاء، للتبديل بين عروض متقاربة داخل قسم واحد.',
 inputs=[('Items', 'List of MCO_TabItem', '{Value, Label}'), ('ActiveValue', 'Text', '')],
 events=[('OnChange', 'Value (Text)')],
 tree='''MCO_SegmentedTabs :: — :: Block
  List :: "mco-segtabs " + ExtraClass :: Source = Items · role = "tablist"
    Button :: "mco-segtab" + If(Items.Current.Value = ActiveValue, " is-active", "") :: role = "tab" · aria-selected · OnClick → OnChange(Items.Current.Value)
      Expression :: — :: Value = Items.Current.Label''',
 notes=['تنبيه تباين من الملف: نص brand-light مع الأبيض 3.8:1.'],
 preview_js="h(M.SegmentedTabs,{defaultValue:'b',items:[{value:'a',label:'الأهداف'},{value:'b',label:'المؤشرات'},{value:'c',label:'المبادرات'}]})")

C['pagination'] = dict(name='ترقيم الصفحات', mco='Pagination', kind=OS,
 summary='نمط Pagination من OutSystems UI. أزرار 36px بظل shadow-s، والصفحة الحالية brand-primary.',
 variants=[('عادي', 'بدون كلاس', ''), ('مع عدد النتائج', 'داخل MCO_PaginationFooter', 'في القسم الثاني')],
 tree='''Pagination :: — :: StartIndex · MaxRecords · TotalCount · OnNavigate = …''',
 preview='PAGINATION')

C['stepper'] = dict(name='مؤشر الخطوات', mco='MCO_Stepper', kind=BLOCK,
 summary='3 إلى 7 خطوات على شكل أسهم متتالية: المكتملة brand-default، والنشطة brand-shade-30. الطرفان مستويان بزوايا 8px.', figma='2:20204',
 inputs=[('Steps', 'List of Text', 'عناوين الخطوات'), ('Current', 'Integer', 'فهرس الخطوة الحالية، يبدأ من 0')],
 tree='''MCO_Stepper :: — :: Block
  List :: "mco-stepper " + ExtraClass :: Source = Steps · role = "list"
    Container :: "mco-step mco-step--" + If(Steps.CurrentRowNumber < Current, "complete", If(Steps.CurrentRowNumber = Current, "active", "inactive")) + If(Steps.CurrentRowNumber = 0, " mco-step--initial", "") :: role = "listitem" · aria-current = "step" للنشطة
      Container :: mco-step__num
        If :: — :: Steps.CurrentRowNumber < Current
          MCO_Icon :: — :: Name = "tick-circle" · Size = 20
        Else :: — ::
          Expression :: — :: Value = Steps.CurrentRowNumber + 1
      Expression :: mco-step__title :: Value = Steps.Current''',
 notes=['شكل الطرفين تلقائي من الثيم: الخطوة الأولى مستوية من اليمين والأخيرة مستوية من اليسار، بزوايا 8px كما في Figma «Progress step»، فلا يحتاج المطور كلاساً إضافياً.', 'على الجوال حيث ما يتسع، استخدم MCO_WizardProgress.', 'بديل جاهز: نمط Wizard من OutSystems UI يأخذ ألوان MCO من الثيم، لكن بدون شكل الأسهم.'],
 preview_js="h('div',{className:'pv-stack'},h(M.Stepper,{current:1,steps:['البيانات الأساسية','المرفقات','المراجعة','الإرسال']}),h(M.Stepper,{current:3,steps:['الأولى','الثانية','الثالثة']}))")

C['wizard'] = dict(name='مؤشر التقدّم المختصر', mco='MCO_WizardProgress', kind=BLOCK,
 summary='شريط 50×5 لكل خطوة، فوق النماذج متعددة الخطوات على الجوال.',
 inputs=[('Total', 'Integer', 'عدد الخطوات'), ('Current', 'Integer', 'من 0'), ('AriaLabel', 'Text = "تقدّم الخطوات"', '')],
 tree='''MCO_WizardProgress :: — :: Block · OnParametersChanged: تُبنى قائمة Bars بأرقام 0 … Total-1
  List :: "mco-wizard " + ExtraClass :: Source = Bars · role = "progressbar" · aria-valuemin = 1 · aria-valuemax = Total · aria-valuenow = Current + 1 · aria-label = AriaLabel
    Container :: "mco-wizard__bar " + If(Bars.Current < Current, "is-done", If(Bars.Current = Current, "is-current", "is-next"))''',
 preview_js="row([h(M.WizardProgress,{key:1,total:3,current:1}),h(M.WizardProgress,{key:2,total:5,current:3})])")

# ───────────────────────── القسم الثاني ─────────────────────────

C['layout'] = dict(name='قالب الصفحة', mco='MCO_LayoutBase', kind=BLOCK,
 summary='Layout للصفحات الداخلية: القائمة الجانبية يميناً، وفي العمود الرئيسي شريط التنقل ثم المحتوى ثم التذييل.',
 placeholders=[('SideMenu', 'MCO_SideMenu'), ('Navbar', 'MCO_Navbar'), ('Content', 'محتوى الشاشة'), ('Footer', 'MCO_Footer')],
 tree='''MCO_LayoutBase :: — :: Block (Layout)
  Container :: "layout mco-shell " + ExtraClass
    Placeholder :: — :: SideMenu
    Container :: mco-shell__main
      Placeholder :: — :: Navbar
      HTML Element (main) :: mco-shell__content
        Placeholder :: — :: Content
      HTML Element (footer) :: mco-shell__footer
        Placeholder :: — :: Footer''',
 notes=['يُنشأ كـ Layout جديد في وحدة MCO_Components، وكل شاشة داخلية تبدأ منه.', 'كلاس layout يبقى على الجذر لأن بعض أنماط OutSystems UI تبحث عنه.'],
 preview='LAYOUT')

C['navbar'] = dict(name='شريط التنقل العلوي', mco='MCO_Navbar', kind=BLOCK, figma='2:20663',
 summary='شريط أدوات متدرّج، ثم مسار التنقل وعنوان الصفحة وزر الرجوع والإجراء الرئيسي على خلفية متدرّجة بتموّجات خفيفة. أربعة أنواع: default وtabs وsimple وstepper.',
 inputs=[('Type', 'Text = "default"', 'default · tabs (مع تبويبات) · simple (شريط الأدوات فقط) · stepper (مع مؤشر الخطوات الدائري)'), ('Title', 'Text', ''),
         ('Breadcrumbs', 'List of MCO_Breadcrumb', '{Label, URL}، آخر عنصر بدون URL'), ('ShowBack', 'Boolean = True', '')],
 events=[('OnBack', '—')],
 placeholders=[('Tools', 'أزرار شريط الأدوات: Button بكلاس mco-nav__tool وفيه MCO_Icon'), ('Action', 'زر بكلاس "btn btn-primary btn-mobile"'), ('Tabs', 'Tabs عند Type = "tabs"'), ('Steps', 'MCO_StepsBar بـ ExtraClass = "mco-nav__steps" عند Type = "stepper"')],
 tree='''MCO_Navbar :: — :: Block
  HTML Element (header) :: "mco-nav " + ExtraClass
    Container :: mco-nav__bar
      Container :: mco-nav__tools
        Placeholder :: — :: Tools
    If :: — :: Type <> "simple"
      Container :: mco-nav__body
        Container :: mco-crumbs :: role = "navigation" · aria-label = "مسار التنقل"
          MCO_Icon :: — :: Name = "home" · Size = 16
          List :: mco-crumbs__list :: Source = Breadcrumbs
            Container :: mco-crumbs__item
              MCO_Icon :: — :: Name = "arrow-left" · Size = 16
              If :: — :: Breadcrumbs.Current.URL <> ""
                Link :: mco-crumbs__link :: URL = Breadcrumbs.Current.URL · Text = Label
              Else :: — ::
                Expression :: — :: Value = Breadcrumbs.Current.Label · aria-current = "page"
        Container :: mco-nav__titlerow
          If :: — :: ShowBack
            Button :: mco-nav__back :: OnClick → OnBack · aria-label = "رجوع"
              MCO_Icon :: — :: Name = "arrow-left" · IsFlipped = True
          HTML Element (h1) :: mco-nav__title
            Expression :: — :: Value = Title
          Placeholder :: — :: Action
        If :: — :: Type = "tabs"
          Container :: mco-nav__tabs
            Placeholder :: — :: Tabs
    If :: — :: Type = "stepper"
      Placeholder :: — :: Steps''',
 notes=['محدّث من Figma (navbar 2:20663): الشريط العلوي متدرّج من action-primary-default إلى bg-navbar، والخلفية تحته متدرّجة من bg-brand-soft إلى bg-surface مع تموّجات دائرية خفيفة، وكلها من الثيم بدون صور.',
        'مسار التنقل 14px بلون text-tertiary، وزر الرجوع على bg-subtle بدون حد.',
        'زر الإجراء داخل الشريط يأخذ brand-secondary تلقائياً من الثيم، كما في Figma.', 'التبويبات داخل mco-nav__tabs تأخذ شكل «#Nav Tab» تلقائياً: ارتفاع 53px، ونص 16px عريض، وخط سفلي 4px brand-default للنشط، وتلتصق بالحافة السفلية للشريط بدون مسافة.'],
 preview='NAVBAR')

C['sidemenu'] = dict(name='القائمة الجانبية', mco='MCO_SideMenu', kind=BLOCK,
 summary='عرض 287px (106px مطوية). العنصر النشط بخلفية brand-shade-20 وشريط 5px على الحافة اليمنى.',
 inputs=[('Items', 'List of MCO_MenuItem', '{Value, Label, Icon, ParentValue}؛ ParentValue فارغ للعناصر الرئيسية'),
         ('ActiveValue', 'Text', 'العنصر الحالي'), ('IsCollapsed', 'Boolean = False', '')],
 events=[('OnSelect', 'Value (Text)'), ('OnCollapse', '—')],
 placeholders=[('Logo', 'شعار المنصة'), ('Footer', 'الإعدادات وتسجيل الخروج بنفس هيكل العنصر')],
 tree='''MCO_SideMenu :: — :: Block · متغير محلي OpenValue لفتح القائمة الفرعية
  HTML Element (nav) :: "mco-side" + If(IsCollapsed, " is-collapsed", "") + " " + ExtraClass :: aria-label = "القائمة الرئيسية"
    Container :: mco-side__top
      Container :: mco-side__logo
        Placeholder :: — :: Logo
      List :: mco-side__list :: Source = TopItems (ParentValue = "") · role = "list"
        Container :: "mco-side__li" + If(Value = OpenValue, " is-open", "") :: role = "listitem"
          Button :: "mco-side__item" + If(Value = ActiveValue, " is-active", "") :: OnClick → إذا له أبناء: OpenValue = Value، وإلا OnSelect(Value)
            MCO_Icon :: — :: Name = Icon
            If :: — :: not IsCollapsed
              Expression :: mco-side__label :: Value = Label
            If :: — :: HasChildren and not IsCollapsed
              MCO_Icon :: — :: Name = "arrow-down" · ExtraClass = If(Value = OpenValue, "mco-rot", "")
          If :: — :: Value = OpenValue and not IsCollapsed
            List :: mco-side__sub :: Source = Children (ParentValue = Value)
              Container :: mco-side__li
                Button :: "mco-side__item mco-side__item--sub" + If(Value = ActiveValue, " is-active", "") :: OnClick → OnSelect(Value)
                  Expression :: mco-side__label :: Value = Label
    Container :: mco-side__bottom
      Container :: mco-side__list
        Placeholder :: — :: Footer
      Button :: mco-iconbtn mco-side__collapse :: OnClick → OnCollapse · aria-label = "طي القائمة"
        MCO_Icon :: — :: Name = "menu"''',
 preview_js=r"""h('div',{className:'pv-row pv-top'},
 h(M.SideMenu,{value:'a1',onCollapse:function(){},items:[{value:'home',label:'الصفحة الرئيسية',icon:'home'},{value:'plans',label:'خطط التواصل',icon:'task-square'},{value:'agenda',label:'أجندة التواصل',icon:'calendar',children:[{value:'a1',label:'الأجندة الشهرية'},{value:'a2',label:'الفعاليات'}]},{value:'docs',label:'المستندات',icon:'folder'}],footerItems:[{value:'set',label:'الإعدادات',icon:'setting-2'},{value:'out',label:'تسجيل الخروج',icon:'logout'}]}),
 h(M.SideMenu,{collapsed:true,value:'plans',onCollapse:function(){},items:[{value:'home',label:'الصفحة الرئيسية',icon:'home'},{value:'plans',label:'خطط التواصل',icon:'task-square'},{value:'agenda',label:'أجندة التواصل',icon:'calendar'},{value:'docs',label:'المستندات',icon:'folder'}],footerItems:[{value:'set',label:'الإعدادات',icon:'setting-2'}]}))""")

C['subheader'] = dict(name='الرأس الفرعي للصفحة', mco='MCO_PageSubHeader', kind=BLOCK,
 summary='شريط brand-shade-30 تحت شريط التنقل: تبويبات يميناً وأزرار يساراً.',
 placeholders=[('Tabs', 'Tabs بـ ExtendedClass = "mco-tabs-filled"'), ('Actions', 'أزرار btn')],
 tree='''MCO_PageSubHeader :: — :: Block
  Container :: "mco-subheader " + ExtraClass
    Container :: mco-subheader__tabs
      Placeholder :: — :: Tabs
    Container :: mco-subheader__actions
      Placeholder :: — :: Actions''',
 preview='SUBHEADER')

C['actionsbar'] = dict(name='شريط الإجراءات', mco='MCO_ActionsBar', kind=BLOCK, figma='2:20589',
 summary='خلفية bg-light-grey تجمع إجراءات النموذج: الإلغاء يميناً، والتنقل (السابق ثم التالي) يساراً.',
 placeholders=[('Start', 'زر الإلغاء "btn btn-destructive" (يمين)'), ('End', 'زر "btn" للسابق ثم "btn btn-primary" للتالي أو الحفظ (يسار)')],
 tree='''MCO_ActionsBar :: — :: Block
  Container :: "mco-actionsbar " + ExtraClass
    Container :: mco-actionsbar__start
      Placeholder :: — :: Start
    Container :: mco-actionsbar__end
      Placeholder :: — :: End''',
 notes=['الترتيب كما في Figma «Actions bar»: الإلغاء في بداية السطر (يمين)، والزر الأساسي في آخره (أقصى اليسار) وقبله السابق.',
        'زر «التالي» فيه MCO_Icon ‏arrow-left بعد النص.'],
 preview_js="h(M.ActionsBar,{start:[h(M.Button,{key:1,variant:'secondary',destructive:true},'إلغاء')],end:[h(M.Button,{key:2,variant:'secondary'},'السابق'),h(M.Button,{key:3,variant:'primary',iconEnd:'arrow-left'},'التالي')]})")

C['alert'] = dict(name='التنبيه', mco='MCO_Alert', kind=BLOCK,
 summary='تنبيه داخل الصفحة: أيقونة الحالة 40px وعنوان ونص ورابط إجراء اختياري وزر إغلاق.',
 inputs=[('Status', 'MCO_Status Identifier', 'success · info · warning · danger'), ('Title', 'Text', ''), ('ShowClose', 'Boolean = True', '')],
 events=[('OnClose', '—')],
 placeholders=[('Message', 'نص التنبيه'), ('Action', 'زر بكلاس "btn btn-link" (اختياري)')],
 tree='''MCO_Alert :: — :: Block
  Container :: "mco-alert mco-alert--" + Status + " " + ExtraClass :: role = "status"
    Container :: "mco-status-icon mco-status-icon--40 mco-status-icon--" + Status
      MCO_Icon :: — :: Name = Status.Icon · Size = 24
    Container :: mco-alert__body
      Expression :: mco-alert__title :: Value = Title
      Container :: mco-alert__text
        Placeholder :: — :: Message
        Placeholder :: — :: Action
    If :: — :: ShowClose
      Button :: mco-iconbtn :: OnClick → OnClose · aria-label = "إغلاق"
        MCO_Icon :: — :: Name = "close"''',
 notes=['عنوان التحذير بلون font-primary لأن لون warning لا يصلح نصاً (1.7:1)، والثيم يضبطه.'],
 preview_js="h('div',{className:'pv-stack'},['success','info','warning','danger'].map(function(s){return h(M.Alert,{key:s,status:s,title:'تنبيه',onClose:function(){},action:h(M.Button,{variant:'link'},'رابط الإجراء')},'توضيح تفاصيل العملية والإجراءات وإعادة المحاولة');}))")

C['toast'] = dict(name='الإشعار القصير', mco='Feedback Message', kind=OS,
 summary='إجراء Message حق المنصة. الثيم يرسم الأنواع الأربعة بألوان حالات MCO وعرض حتى 542px.',
 variants=[('نجاح', 'Message · Type = Success', ''), ('معلومة', 'Message · Type = Info', ''), ('تحذير', 'Message · Type = Warning', ''), ('خطأ', 'Message · Type = Error', '')],
 tree='''Client Action :: — :: بعد الحفظ
  Message :: — :: Type = Success · Message = "تم حفظ التغييرات"''',
 preview='TOAST')

C['popup'] = dict(name='نافذة الرسالة', mco='Popup + MCO_PopupContent', kind=MIX,
 summary='ودجت Popup حق المنصة للنافذة والطبقة الخلفية، وداخله Block للمحتوى: أيقونة حالة 60px وعنوان ونص وأزرار.',
 inputs=[('Status', 'MCO_Status Identifier (اختياري)', 'بدون قيمة = بدون أيقونة'), ('Title', 'Text', '')],
 placeholders=[('Message', 'نص الرسالة'), ('Actions', 'زر "btn btn-primary" وزر "btn btn-cancel"')],
 tree='''Popup :: popup-dialog mco-popup-default :: ShowPopup = متغير · mco-popup-large لعرض 720px
  MCO_PopupContent :: — :: Block
    Container :: "mco-popup " + ExtraClass :: role = "dialog" · aria-label = Title
      If :: — :: Status <> NullTextIdentifier()
        Container :: "mco-status-icon mco-status-icon--60 mco-status-icon--" + Status
          MCO_Icon :: — :: Name = Status.Icon · Size = 36
      Container :: mco-popup__content
        Expression :: mco-popup__title :: Value = Title
        Container :: mco-popup__text
          Placeholder :: — :: Message
      Container :: mco-popup__actions
        Placeholder :: — :: Actions''',
 preview='POPUP')

C['formpopup'] = dict(name='نافذة النموذج', mco='Popup + MCO_FormPopup', kind=MIX,
 summary='نافذة 1000px لنموذج قصير: عنوان brand-primary وشبكة حقول بعمودين ثم الأزرار.',
 inputs=[('Title', 'Text', ''), ('Columns', 'Integer = 2', '')],
 placeholders=[('Fields', 'حقول MCO_TextField؛ الحقل العريض داخل Container بكلاس mco-span-all'), ('Actions', 'أزرار btn')],
 tree='''Popup :: popup-dialog mco-popup-form :: ShowPopup = متغير
  MCO_FormPopup :: — :: Block
    Container :: "mco-formpopup " + ExtraClass :: role = "dialog" · aria-label = Title
      HTML Element (h2) :: mco-formpopup__title
        Expression :: — :: Value = Title
      Container :: mco-formpopup__grid :: Style = "grid-template-columns: repeat(" + Columns + ", minmax(0, 1fr))"
        Placeholder :: — :: Fields
      Container :: mco-popup__actions mco-formpopup__actions
        Placeholder :: — :: Actions''',
 preview='FORMPOPUP')

C['dialog'] = dict(name='الحوار المضمّن', mco='MCO_InlineDialog', kind=BLOCK,
 summary='رسالة داخل الصفحة تطلب قراراً: خمسة أنواع، وحجمان، والأزرار تحت أو بجانب النص.',
 inputs=[('Status', 'MCO_Status Identifier', 'danger · warning · info · success · default'), ('Size', 'Text = "large"', 'large · small'),
         ('Layout', 'Text = "under"', 'under (الأزرار تحت فاصل) · left (الأزرار في الطرف الأيسر)'), ('Title', 'Text', '')],
 placeholders=[('Message', 'النص'), ('Actions', 'أزرار btn (اختياري)')],
 tree='''MCO_InlineDialog :: — :: Block
  Container :: "mco-dialog mco-dialog--" + Status + " mco-dialog--" + Layout + If(Size = "small", " mco-dialog--small", "") + " " + ExtraClass :: role = If(Status = "danger" or Status = "warning", "alertdialog", "region")
    Container :: mco-dialog__main
      Container :: mco-dialog__icon
        MCO_Icon :: — :: Name = Status.DialogIcon · Size = 20
      Container :: mco-dialog__text
        If :: — :: Title <> ""
          Expression :: mco-dialog__title :: Value = Title
        Container :: mco-dialog__body
          Placeholder :: — :: Message
    Container :: mco-dialog__actions
      Placeholder :: — :: Actions''',
 notes=['الألوان مربوطة بتوكنز الحالات بدل لوحة «Dialouge colors» المستقلة في Figma.'],
 preview_js=r"""h('div',{className:'pv-stack'},
 h(M.InlineDialog,{type:'error',title:'إجراء لا يمكن عكسه',actions:[h(M.Button,{key:1,destructive:true},'حذف الحساب'),h(M.Button,{key:2,variant:'cancel'},'إلغاء')]},'أنت على وشك حذف حسابك بشكل دائم.'),
 h(M.InlineDialog,{type:'information',layout:'left',title:'للعلم فقط',actions:[h(M.Button,{key:1},'متابعة الجلسة'),h(M.Button,{key:2,variant:'secondary'},'تسجيل الخروج')]},'لقد كنت غير نشط لفترة. لأمانك، سيتم تسجيل خروجك قريباً.'),
 h(M.InlineDialog,{type:'alert',size:'small',title:'تنبيه'},'يرجى مراجعة البيانات قبل الإرسال.'),
 h(M.InlineDialog,{type:'success',size:'small',title:'تم الحفظ'},'حُفظت التغييرات بنجاح.'))""")

C['table'] = dict(name='جدول البيانات', mco='Table', kind=OS,
 summary='ودجت Table حق المنصة. الثيم يرسم رأساً 56px على bg-light-grey، والصفوف 78px متلاصقة بحد grey-soft كما في Figma، وبين شريط التصفية والجدول والترقيم 32px.',
 variants=[('رقم أو رمز', 'Expression · Style Classes = "mco-cell--number"', 'عريض بلون brand-secondary'), ('الحالة', 'MCO_StatusBadge داخل الخلية', ''),
           ('إجراءات الصف', 'Button · "btn btn-cancel btn-small"', ''), ('على الجوال', 'If IsPhone() → List من MCO_MobileTableCard', 'IsPhone من OutSystemsUI')],
 tree='''Table :: — :: Source = GetPlans.List
  Header Row :: — :: "رقم الخطة" · "اسم الخطة" · "الحالة" · ""
  Row :: — ::
    Expression :: mco-cell--number :: Value = Code
    Expression :: — :: Value = Name
    MCO_StatusBadge :: — :: Status = StatusId · Label = StatusLabel
    Button :: btn btn-cancel btn-small :: Text = "عرض"''',
 notes=['ضع فوقه MCO_FilterBar وتحته MCO_PaginationFooter.'],
 preview='TABLE')

C['filterbar'] = dict(name='شريط التصفية', mco='MCO_FilterBar', kind=BLOCK,
 summary='حقل بحث أعرض ثم حقول تصفية متساوية، فوق الجدول.',
 placeholders=[('Search', 'Input بكلاس form-control'), ('Filters', 'Dropdown أو Date Picker لكل تصفية')],
 tree='''MCO_FilterBar :: — :: Block
  Container :: "mco-filterbar " + ExtraClass :: role = "search"
    Container :: mco-filterbar__search
      Placeholder :: — :: Search
    Container :: mco-filterbar__fields
      Placeholder :: — :: Filters''',
 preview='FILTERBAR')

C['pfooter'] = dict(name='تذييل الجدول', mco='MCO_PaginationFooter', kind=BLOCK,
 summary='ترقيم الصفحات بجانب قائمة «عدد النتائج».',
 placeholders=[('Pagination', 'نمط Pagination'), ('PageSize', 'ودجت Dropdown بخيارات 12 · 24 · 48')],
 tree='''MCO_PaginationFooter :: — :: Block
  Container :: "mco-pfooter " + ExtraClass
    Placeholder :: — :: Pagination
    Container :: mco-pfooter__size
      Placeholder :: — :: PageSize''',
 preview='PFOOTER')

C['mcard'] = dict(name='بطاقة الجوال', mco='MCO_MobileTableCard', kind=BLOCK,
 summary='بديل صف الجدول على الجوال: عنوان وحالة، وتتوسع لعرض الحقول والإجراءات.',
 inputs=[('Title', 'Text', ''), ('Status', 'MCO_Status Identifier', ''), ('StatusLabel', 'Text', ''),
         ('Fields', 'List of MCO_KeyValue', '{Label, Value}'), ('IsExpanded', 'Boolean = False', 'القيمة الأولى لمتغير محلي')],
 events=[('OnToggle', 'IsOpen (Boolean)')],
 placeholders=[('Actions', 'أزرار "btn btn-small"')],
 tree='''MCO_MobileTableCard :: — :: Block · متغير محلي IsOpen = IsExpanded
  Container :: "mco-mcard" + If(IsOpen, " is-open", "") + " " + ExtraClass
    Container :: mco-mcard__row
      Expression :: mco-mcard__title :: Value = Title
      Container :: mco-mcard__meta
        MCO_StatusBadge :: — :: Status = Status · Label = StatusLabel
        Button :: mco-mcard__toggle :: OnClick → IsOpen = not IsOpen ثم OnToggle(IsOpen) · aria-expanded = IsOpen · aria-label = If(IsOpen, "طي", "توسيع")
          MCO_Icon :: — :: Name = "arrow-down" · ExtraClass = If(IsOpen, "mco-rot", "")
    If :: — :: IsOpen
      List :: mco-mcard__more :: Source = Fields
        Container :: mco-mcard__field
          Expression :: mco-mcard__k :: Value = Fields.Current.Label
          Expression :: mco-mcard__v :: Value = Fields.Current.Value
      Container :: mco-mcard__actions
        Placeholder :: — :: Actions''',
 preview_js=r"""h('div',{className:'pv-row pv-top'},
 h(M.MobileTableCard,{title:'حملة التوعية بالميزانية',status:{status:'warning',label:'قيد المراجعة'}}),
 h(M.MobileTableCard,{title:'خطة التواصل للقمة',defaultExpanded:true,status:{status:'success',label:'معتمدة'},fields:[{label:'رقم الخطة',value:'PL-2026-01'},{label:'الجهة',value:'وزارة الخارجية'},{label:'الربع',value:'الربع الأول'}],actions:[h(M.Button,{key:1,size:'small'},'عرض'),h(M.Button,{key:2,size:'small',variant:'secondary'},'تعديل')]}))""")

C['info'] = dict(name='قائمة المعلومات', mco='MCO_InfoList', kind=BLOCK,
 summary='أزواج عنوان وقيمة موزّعة أفقياً في صندوق بحد grey-soft، لملخص سجل.',
 inputs=[('Items', 'List of MCO_KeyValue', '{Label, Value}')],
 tree='''MCO_InfoList :: — :: Block
  List :: "mco-info " + ExtraClass :: Source = Items
    Container :: mco-kv mco-info__item
      Expression :: mco-kv__k :: Value = Items.Current.Label
      Expression :: mco-kv__v :: Value = Items.Current.Value''',
 notes=['قيمة غير نصية (مثل شارة حالة): ابنِ العنصر يدوياً بنفس الكلاسات وضع MCO_StatusBadge داخل Container بكلاس mco-kv__v.'],
 preview_js="h(M.InfoList,{items:[{label:'رقم الخطة',value:'PL-2026-14'},{label:'الجهة',value:'وزارة الخارجية'},{label:'المسؤول',value:'نورة القحطاني'},{label:'الحالة',value:h(M.StatusBadge,{status:'success',size:'small'},'معتمدة')}]})")

C['xcard'] = dict(name='البطاقة القابلة للتوسيع', mco='MCO_ExpandableCard', kind=BLOCK,
 summary='بطاقة brand-shade-30 بحقول مفتاح وقيمة، وأدوات 32px للتعديل والحذف والتوسيع.',
 inputs=[('Fields', 'List of MCO_KeyValue', ''), ('ShowEdit', 'Boolean = True', ''), ('ShowDelete', 'Boolean = True', ''), ('IsOpen', 'Boolean = False', 'القيمة الأولى لمتغير محلي')],
 events=[('OnEdit', '—'), ('OnDelete', '—'), ('OnToggle', 'IsOpen (Boolean)')],
 placeholders=[('Content', 'المحتوى الموسّع')],
 tree='''MCO_ExpandableCard :: — :: Block · متغير محلي Open = IsOpen
  HTML Element (section) :: "mco-xcard" + If(Open, " is-open", "") + " " + ExtraClass
    Container :: mco-xcard__head
      List :: mco-xcard__fields :: Source = Fields
        Container :: mco-kv
          Expression :: mco-kv__k :: Value = Fields.Current.Label
          Expression :: mco-kv__v :: Value = Fields.Current.Value
      Container :: mco-xcard__tools
        If :: — :: ShowEdit
          Button :: mco-xcard__tool :: OnClick → OnEdit · aria-label = "تعديل"
            MCO_Icon :: — :: Name = "edit-2" · Size = 16
        If :: — :: ShowDelete
          Button :: mco-xcard__tool :: OnClick → OnDelete · aria-label = "حذف"
            MCO_Icon :: — :: Name = "trash" · Size = 16
        Button :: mco-xcard__tool :: OnClick → Open = not Open ثم OnToggle(Open) · aria-expanded = Open
          MCO_Icon :: — :: Name = "arrow-down" · Size = 16 · ExtraClass = If(Open, "mco-rot", "")
    If :: — :: Open
      Container :: mco-xcard__body
        Placeholder :: — :: Content''',
 preview_js=r"""h('div',{className:'pv-stack'},
 h(M.ExpandableCard,{onEdit:function(){},onDelete:function(){},fields:[{label:'اسم الهدف الاستراتيجي',value:'تعزيز العلاقات الدبلوماسية'},{label:'الجهة المسؤولة',value:'وزارة الخارجية'}]}),
 h(M.ExpandableCard,{defaultOpen:true,onEdit:function(){},fields:[{label:'اسم الهدف الاستراتيجي',value:'رفع مستوى التواصل الإعلامي'}]},h(M.InfoList,{items:[{label:'تاريخ البدء',value:'2026/01/01'},{label:'تاريخ الانتهاء',value:'2026/12/31'}]})))""")

C['points'] = dict(name='بطاقة النقاط', mco='MCO_PointsList', kind=BLOCK,
 summary='عنوان قسم brand-secondary تسبقه شرطة عمودية brand-default، ثم نقاط بعرض كامل على bg-soft.', figma='119:7573',
 inputs=[('Title', 'Text', ''), ('Items', 'List of Text', '')],
 tree='''MCO_PointsList :: — :: Block
  HTML Element (section) :: "mco-points " + ExtraClass
    HTML Element (h3) :: mco-section-title
      Expression :: — :: Value = Title
    List :: mco-points__list :: Source = Items · role = "list"
      Container :: mco-points__item :: role = "listitem"
        Expression :: — :: Value = Items.Current''',
 notes=['عنوان القسم متاح ككلاس mco-section-title لأي بطاقة أخرى.'],
 preview_js="h(M.PointsList,{title:'أبرز التحديات',items:['تفاوت فهم الفئات المستهدفة لرسائل الحملة بين المناطق.','محدودية القنوات الرقمية لدى بعض الجهات الشريكة.','الحاجة إلى توحيد مؤشرات القياس بين الجهات.']})")

C['quarters'] = dict(name='مؤشر الأرباع', mco='MCO_QuarterProgress', kind=BLOCK,
 summary='مسار التقدّم خلال السنة مع علامة لكل ربع، والجزء المنجز brand-primary.',
 inputs=[('Value', 'Integer', '0 إلى 100'), ('AriaLabel', 'Text = "التقدّم خلال السنة"', '')],
 tree='''MCO_QuarterProgress :: — :: Block
  Container :: "mco-quarters " + ExtraClass :: role = "progressbar" · aria-valuemin = 0 · aria-valuemax = 100 · aria-valuenow = Value · aria-label = AriaLabel
    Container :: mco-quarters__track
      Container :: mco-quarters__fill :: Style = "width: " + Value + "%"
      Container :: mco-quarters__dot :: Style = "inset-inline-start: 0%" (ثم 33.33% · 66.67% · 100%)
    Container :: mco-quarters__labels
      Expression :: — :: "الربع الأول" · "الربع الثاني" · "الربع الثالث" · "الربع الرابع"''',
 preview_js="h(M.QuarterProgress,{value:60})")

C['timeline'] = dict(name='الخط الزمني', mco='MCO_Timeline', kind=BLOCK,
 summary='مراحل متتالية، لكل مرحلة دائرة حالة وشارة صغيرة وتاريخ.',
 inputs=[('Stages', 'List of MCO_Stage', '{Name, State, StatusLabel, Date}؛ State = notStarted · inProgress · onHold · failure · success')],
 tree='''MCO_Timeline :: — :: Block
  List :: "mco-timeline " + ExtraClass :: Source = Stages · role = "list"
    Container :: "mco-tl mco-tl--" + Stages.Current.State :: role = "listitem"
      Expression :: mco-tl__name :: Value = Name
      Container :: mco-tl__track
        Container :: mco-tl__dot :: aria-hidden = "true"
          If :: — :: State = "success"
            MCO_Icon :: — :: Name = "check" · Size = 12
      MCO_StatusBadge :: — :: Size = "small" · Status = StateToStatus(State) · Label = StatusLabel
      Container :: mco-tl__date
        MCO_Icon :: — :: Name = "calendar" · Size = 16
        Expression :: — :: Value = Date''',
 notes=['StateToStatus: success → success، inProgress → info، onHold → warning، failure → danger، notStarted → default.'],
 preview_js="h(M.Timeline,{stages:[{name:'التخطيط',state:'success',statusLabel:'مكتملة',date:'20-10-2026'},{name:'الاعتماد',state:'inProgress',statusLabel:'قيد التنفيذ',date:'05-11-2026'},{name:'التنفيذ',state:'onHold',statusLabel:'معلّقة',date:'20-11-2026'},{name:'المراجعة',state:'failure',statusLabel:'متعثرة',date:'01-12-2026'},{name:'الإغلاق',state:'notStarted',statusLabel:'لم تبدأ',date:'20-12-2026'}]})")

C['addmore'] = dict(name='إضافة المزيد', mco='MCO_AddMore', kind=BLOCK,
 summary='شريط بثلاث حالات: لا يوجد عناصر بعد، أو بعد الإضافة، أو رابط.',
 inputs=[('Variant', 'Text = "empty"', 'empty: زر أساسي · added: خلفية bg-soft وزر ثانوي · link: رابط'), ('Title', 'Text', ''), ('Description', 'Text', ''),
         ('ActionLabel', 'Text', '')],
 events=[('OnAdd', '—')],
 tree='''MCO_AddMore :: — :: Block
  Container :: "mco-addmore mco-addmore--" + Variant + " " + ExtraClass
    Container :: mco-addmore__text
      Expression :: mco-addmore__title :: Value = Title
      Expression :: — :: Value = Description
    Button :: If(Variant = "empty", "btn btn-primary", If(Variant = "added", "btn", "btn btn-link")) :: OnClick → OnAdd
      If :: — :: Variant <> "link"
        MCO_Icon :: — :: Name = "add" · Size = 20
      Text :: — :: ActionLabel
      If :: — :: Variant = "link"
        MCO_Icon :: — :: Name = "export" · Size = 20''',
 preview_js=r"""h('div',{className:'pv-stack'},
 h(M.AddMore,{variant:'empty',title:'لا يوجد حسابات بنكية مضافة!',description:'يمكنك إضافة 5 حسابات كحد أقصى',actionLabel:'إضافة حساب بنكي'}),
 h(M.AddMore,{variant:'added',title:'إضافة حساب بنكي آخر؟',description:'يمكنك إضافة حتى 5 حسابات',actionLabel:'إضافة حساب'}),
 h(M.AddMore,{variant:'link',title:'لا يوجد عنوان وطني مسجل للمنشأة!',description:'لتحديث بيانات العنوان الوطني',actionLabel:'اضغط هنا'}))""")

# ───────────────────────── مكوّنات Figma الجديدة (أكتوبر 2026) ─────────────────────────
C['footer'] = dict(name='التذييل', mco='MCO_Footer', kind=BLOCK, figma='370:5688',
 summary='سطر الحقوق مع الشعار يميناً، وروابط السياسات يساراً. ارتفاع 72px وحد علوي grey-soft.',
 inputs=[('Copyright', 'Text', 'مثال: "جميع الحقوق محفوظة © " + Year(CurrDate()) + " لمنصة تواصل الوزراء"'), ('CrestURL', 'Text', 'الشعار المصغّر 24px')],
 placeholders=[('Links', 'روابط Link بكلاس mco-footer__link (الشروط والأحكام، سياسة الخصوصية)')],
 tree='''MCO_Footer :: — :: Block
  HTML Element (footer) :: "mco-footer " + ExtraClass
    Container :: mco-footer__brand
      Image :: mco-footer__crest :: URL = CrestURL · Alt = ""
      Expression :: — :: Value = Copyright
    HTML Element (nav) :: mco-footer__links :: aria-label = "روابط التذييل"
      Placeholder :: — :: Links''',
 notes=['يوضع في Placeholder ‏Footer داخل MCO_LayoutBase.', 'على الجوال يصير السطران فوق بعض في المنتصف.', 'Figma سمّاه «simple-footer».'],
 preview='FOOTER')

C['fsection'] = dict(name='بطاقة قسم النموذج', mco='MCO_FormSection', kind=BLOCK, figma='74:5178',
 summary='قسم من نموذج طويل: رأس بخلفية brand-shade-20 فيه أيقونة وعنوان، وتحته جسم أبيض فيه تنبيه اختياري وحقول على عمودين.',
 inputs=[('Title', 'Text', ''), ('Icon', 'Text = "category-2"', 'أيقونة الرأس 29px')],
 placeholders=[('Content', 'تنبيه اختياري ثم Container بكلاس mco-fsection__grid فيه MCO_TextField، أو MCO_EmptyState إذا القسم فاضي')],
 tree='''MCO_FormSection :: — :: Block
  HTML Element (section) :: "mco-fsection " + ExtraClass
    HTML Element (header) :: mco-fsection__head
      MCO_Icon :: — :: Name = Icon · Size = 32
      HTML Element (h3) :: mco-fsection__title
        Expression :: — :: Value = Title
    Container :: mco-fsection__body
      Placeholder :: — :: Content''',
 notes=['داخل الجسم، عناوين الحقول تكبر تلقائياً لـ 20px عريض كما في Figma.',
        'الحقول توضع في Container بكلاس mco-fsection__grid: عمودان بمسافة 32px، وعمود واحد على الجوال.',
        'Figma سمّى الإطار «Frame 1820548551»، والاسم المقترح هنا MCO_FormSection.'],
 preview='FSECTION')

C['empty'] = dict(name='الحالة الفارغة', mco='MCO_EmptyState', kind=BLOCK, figma='719:7652',
 summary='أيقونة ونص عريض وزر إجراء أساسي عند غياب المحتوى. شكلان: داخل قسم نموذج (مربع أيقونة 67px)، أو بطاقة مستقلة بدائرة أيقونة 72px ووصف مختصر كما في Figma «Empty state».',
 inputs=[('Style', 'Text = "section"', 'section: داخل بطاقة قسم النموذج · card: بطاقة مستقلة («Empty state» 719:7652)'), ('Icon', 'Text = "element-plus"', 'card: document-upload أو ما يناسب'), ('Text', 'Text', ''), ('Description', 'Text', 'card فقط')],
 placeholders=[('Action', 'section: زر "btn btn-primary" فيه النص ثم MCO_Icon ‏arrow-left · card: "btn btn-primary btn-mobile" فيه MCO_Icon ثم النص')],
 tree='''MCO_EmptyState :: — :: Block
  Container :: "mco-empty" + If(Style = "card", " mco-empty--card", "") + " " + ExtraClass
    Container :: mco-empty__top
      Container :: mco-empty__icon
        MCO_Icon :: — :: Name = Icon · Size = If(Style = "card", 32, 36)
      HTML Element (p) :: mco-empty__text
        Expression :: — :: Value = Text
      If :: — :: Style = "card" and Description <> ""
        HTML Element (p) :: mco-empty__desc
          Expression :: — :: Value = Description
    Placeholder :: — :: Action''',
 notes=['الفرق عن MCO_AddMore: هذي تشغل مساحة المحتوى كاملة، وAddMore شريط مستقل.', 'شكل section من الإطار «Frame 1820548552» (74:5204)، وشكل card من مكوّن «Empty state» (719:7652).'],
 preview='EMPTY')

C['record'] = dict(name='بطاقة السجل', mco='MCO_RecordCard', kind=BLOCK, figma='673:7244',
 summary='سجل للقراءة بحقول MCO_InfoField متساوية العرض وحد متدرّج، وتحت فاصل زر عرض التفاصيل في بداية السطر وأزرار التعديل والحذف في نهايته. نوعا الزيارة والاستقبال يضيفان الدولة والتصنيف والغرض مع «عرض المزيد».',
 inputs=[('Fields', 'List of MCO_KeyValue', '{Key, Value}، من 2 إلى 5 حقول'), ('Purpose', 'Text', 'نص الغرض (زيارة أو استقبال)، بدون قيمة = بدون قسم الغرض'), ('PurposeLabel', 'Text = "الغرض من الزيارة"', ''),
         ('ShowView', 'Boolean = True', 'False في نوعي الزيارة والاستقبال'), ('ShowEdit', 'Boolean = True', ''), ('ShowDelete', 'Boolean = True', '')],
 events=[('OnView', '—'), ('OnEdit', '—'), ('OnDelete', '—')],
 placeholders=[('ExtraFields', 'حقول خاصة قبل Fields: MCO_InfoField بـ Type = "country" أو "chip"')],
 tree='''MCO_RecordCard :: — :: Block · متغير محلي PurposeOpen = False
  HTML Element (article) :: "mco-record " + ExtraClass
    Container :: mco-record__body
      Container :: mco-record__fields
        Placeholder :: — :: ExtraFields
        List :: — :: Source = Fields
          MCO_InfoField :: — :: Label = Fields.Current.Key · Value = Fields.Current.Value
      If :: — :: Purpose <> ""
        Container :: "mco-record__purpose" + If(PurposeOpen, "", " is-clamped")
          Expression :: mco-ifield__label :: Value = PurposeLabel
          HTML Element (p) :: mco-record__purpose-text
            Expression :: — :: Value = Purpose
          Button :: mco-record__more :: OnClick → PurposeOpen = not PurposeOpen · aria-expanded = PurposeOpen
            Expression :: — :: Value = If(PurposeOpen, "عرض أقل", "عرض المزيد")
            MCO_Icon :: — :: Name = "arrow-down" · Size = 16 · ExtraClass = If(PurposeOpen, "mco-rot", "")
    Container :: mco-record__actions
      If :: — :: ShowView
        Button :: btn :: OnClick → OnView
          Expression :: — :: Value = "عرض التفاصيل"
          MCO_Icon :: — :: Name = "arrow-left" · Size = 20
      Container :: mco-record__tools
        If :: — :: ShowEdit
          Button :: btn btn-tertiary :: OnClick → OnEdit
            MCO_Icon :: — :: Name = "card-edit" · Size = 20
            Expression :: — :: Value = "تعديل"
        If :: — :: ShowDelete
          Button :: btn btn-tertiary btn-destructive :: OnClick → OnDelete
            MCO_Icon :: — :: Name = "trash" · Size = 20
            Expression :: — :: Value = "حذف"''',
 notes=['محدّث من Figma («#TableField /)» 673:7244): حد 1.5px متدرّج من border-brand-subtle إلى border-focus، وفاصل الأزرار بلون border-brand-subtle.',
        'الأزرار داخل mco-record__actions تأخذ مقاس 36px وزوايا 7px تلقائياً: عرض التفاصيل في بداية السطر، والتعديل والحذف في نهايته.',
        'الغرض يظهر بسطرين ثم «عرض المزيد»؛ جرّب الضغط عليه في المعاينة.',
        'الحقول تتوزع بالتساوي، وتلتف لسطر ثاني على الشاشات الصغيرة.'],
 preview='RECORD')

NEW = {'csteps', 'avatar', 'ifield', 'datetile', 'fact', 'cardhead', 'activity', 'file', 'dhead', 'loader', 'footer', 'fsection', 'empty', 'record', 'stat', 'maintabs', 'usercard', 'summary', 'slide', 'dcard', 'xtext', 'gallery', 'person', 'addbanner'}

C['stat'] = dict(name='بطاقة الرقم', mco='MCO_StatTile', kind=BLOCK, figma='467:12414',
 summary='رقم أو تاريخ بارز مع عنوانه وأيقونة في مربع متدرّج، داخل بطاقة الملخص أو أي لوحة أرقام.',
 inputs=[('Label', 'Text', ''), ('Value', 'Text', 'الرقم أو التاريخ'), ('Icon', 'Text', 'اسم أيقونة'), ('Size', 'Text = "default"', 'default: رقم 32px · sm: 24px للتواريخ')],
 tree='''MCO_StatTile :: — :: Block
  Container :: "mco-stat" + If(Size = "sm", " mco-stat--sm", "") + " " + ExtraClass
    Container :: mco-stat__icon
      MCO_Icon :: — :: Name = Icon · Size = 24
    Container :: mco-stat__text
      Expression :: mco-stat__label :: Value = Label
      Expression :: mco-stat__value :: Value = Value · dir = "ltr"''',
 preview='STAT')

C['maintabs'] = dict(name='التبويبات الرئيسية', mco='Tabs + mco-tabs-main', kind=OS, figma='467:11975',
 summary='شريط تبويبات بعرض كامل لأقسام الصفحة الكبيرة: كل تبويب يأخذ مساحة متساوية، والنشط بتدرّج الهوية.',
 variants=[('2 إلى 4 تبويبات', 'Tabs · ExtendedClass = "mco-tabs-main"', 'العرض يتوزع بالتساوي'), ('أيقونة التبويب', 'MCO_Icon داخل TabsHeaderItem قبل النص', '24px')],
 tree='''Tabs :: — :: ExtendedClass = "mco-tabs-main"
  TabsHeaderItem :: — ::
    MCO_Icon :: — :: Name = "element-3"
    Text :: — :: "أطر التواصل"
  TabsContentItem :: — :: محتوى التبويب''',
 notes=['للتبديل داخل بطاقة استخدم التبويبات العادية (Tabs) بنمط mco-tabs-filled.'],
 preview='MAINTABS')

C['usercard'] = dict(name='بطاقة المستخدم', mco='MCO_UserCard', kind=BLOCK, figma='74:6099',
 summary='اسم المستخدم ومنصبه وصورته أسفل القائمة الجانبية، مع رابطَي الإعدادات والخروج.',
 inputs=[('Name', 'Text', ''), ('Role', 'Text', ''), ('PhotoURL', 'Text', 'بدون قيمة = الحرفان الأولان من الاسم')],
 events=[('OnSettings', '—'), ('OnLogout', '—')],
 tree='''MCO_UserCard :: — :: Block
  Container :: "mco-usercard " + ExtraClass
    Container :: mco-usercard__who
      If :: — :: PhotoURL <> ""
        Image :: mco-usercard__avatar :: URL = PhotoURL · Alt = Name
      Else :: — ::
        Expression :: mco-usercard__avatar :: Value = الحرفان الأولان من Name
      Container :: mco-usercard__text
        Expression :: mco-usercard__name :: Value = Name
        Expression :: mco-usercard__role :: Value = Role
    Container :: mco-usercard__links
      Button :: mco-usercard__link :: OnClick → OnSettings
        MCO_Icon :: — :: Name = "setting-2"
        Text :: — :: "إعدادات"
      Button :: mco-usercard__link mco-usercard__link--danger :: OnClick → OnLogout
        MCO_Icon :: — :: Name = "logout"
        Text :: — :: "خروج"''',
 notes=['يوضع في Placeholder ‏Footer داخل MCO_SideMenu، ويختفي تلقائياً لما تكون القائمة مطوية.'],
 preview='USERCARD')

C['summary'] = dict(name='بطاقة الملخص', mco='MCO_SummaryCard', kind=BLOCK, figma='467:12414',
 summary='رأس صفحة السجل: العنوان والحالة، وثلاثة أرقام رئيسية، وأزرار الانتقال لأقسامه، مع رسم توضيحي.',
 inputs=[('Title', 'Text', ''), ('Status', 'MCO_Status Identifier', ''), ('StatusLabel', 'Text', ''), ('ImageURL', 'Text', 'الرسم التوضيحي (اختياري)')],
 placeholders=[('Stats', '3 من MCO_StatTile'), ('Actions', 'زر رئيسي "btn btn-primary" وأزرار "btn" (Small 32px)، في كل زر MCO_Icon بحجم 20 قبل النص')],
 tree='''MCO_SummaryCard :: — :: Block
  Container :: "mco-summary " + ExtraClass
    Container :: mco-summary__main
      Container :: mco-summary__head
        HTML Element (h2) :: mco-summary__title
          Expression :: — :: Value = Title
        MCO_StatusBadge :: — :: Status = Status · Label = StatusLabel
      Container :: mco-summary__stats
        Placeholder :: — :: Stats
      Container :: mco-summary__actions
        Placeholder :: — :: Actions
    If :: — :: ImageURL <> ""
      Image :: mco-summary__art :: URL = ImageURL · Alt = ""''',
 notes=['الرسم التوضيحي في Figma (العقدة 467:12108)؛ يُصدَّر SVG ويُرفع في Resources.', 'Figma سمّى الإطار «Frame 1820548567»، والاسم المقترح هنا MCO_SummaryCard.',
        'الأزرار داخل mco-summary__actions تأخذ مقاس Small من Figma تلقائياً: ارتفاع 32px وزوايا 6px ونص 14px. الثانوية بحد brand-light ونص brand-default وبدون خلفية.',
        'أيقونات الأزرار في Figma كلها user (مكان مؤقت)؛ المقترح: task-square للأهداف، global لأولويات الدول، calendar للتقويم.'],
 preview='SUMMARY')

C['slide'] = dict(name='البطاقة المنسدلة', mco='MCO_SlideCard', kind=BLOCK, figma='424:7023',
 summary='بطاقة سجل بحقل أو حقلين بارزين وأدوات تعديل وحذف، وتنسدل لتعرض بطاقات التفاصيل تحتها.',
 inputs=[('Fields', 'List of MCO_SlideField', '{Label, Value, Icon}؛ الحقل الأول بمربع أيقونة داكن'), ('IsOpen', 'Boolean = False', 'القيمة الأولى لمتغير محلي'),
         ('IsCollapsible', 'Boolean = True', 'False = بدون زر الانسدال («no procedures»)'), ('ShowEdit', 'Boolean = True', ''), ('ShowDelete', 'Boolean = True', '')],
 events=[('OnToggle', 'IsOpen (Boolean)'), ('OnEdit', '—'), ('OnDelete', '—')],
 placeholders=[('Actions', 'زر إضافي "btn btn-mobile" بارتفاع زر الانسدال (36px) («with button»)'), ('Content', 'بطاقات MCO_DetailsCard تظهر عند الانسدال')],
 variants=[('حقلان مع أدوات', 'ShowEdit و ShowDelete = True', '«tow field»'), ('حقل واحد', 'Fields فيه عنصر واحد · ShowEdit و ShowDelete = False', '«one field»'),
           ('بدون أدوات', 'IsCollapsible = False', '«no procedures»'), ('مع زر', 'زر في Placeholder ‏Actions', '«with button»'), ('مفتوحة', 'IsOpen = True', '«slide details»')],
 tree='''MCO_SlideCard :: — :: Block · متغير محلي Open = IsOpen
  Container :: "mco-slide" + If(Open, " is-open", "") + " " + ExtraClass
    Container :: mco-slide__head
      List :: mco-slide__fields :: Source = Fields
        Container :: mco-slide__field
          Container :: mco-slide__tile
            MCO_Icon :: — :: Name = Fields.Current.Icon
          Container :: mco-slide__text
            Expression :: mco-slide__label :: Value = Fields.Current.Label
            Expression :: mco-slide__value :: Value = Fields.Current.Value
      Container :: mco-slide__tools
        Placeholder :: — :: Actions
        Container :: "mco-slide__procs" + If(not ShowEdit and not ShowDelete, " is-bare", "")
          If :: — :: ShowEdit
            Button :: mco-iconbtn :: OnClick → OnEdit · aria-label = "تعديل"
              MCO_Icon :: — :: Name = "edit-2"
          If :: — :: ShowDelete
            Button :: mco-iconbtn mco-iconbtn--danger :: OnClick → OnDelete · aria-label = "حذف"
              MCO_Icon :: — :: Name = "trash"
          If :: — :: (ShowEdit or ShowDelete) and IsCollapsible
            Container :: mco-slide__sep
          If :: — :: IsCollapsible
            Button :: mco-slide__toggle :: OnClick → Open = not Open ثم OnToggle(Open) · aria-expanded = Open
              MCO_Icon :: — :: Name = "arrow-down" · ExtraClass = If(Open, "mco-rot", "")
    If :: — :: Open
      Container :: mco-slide__body
        Placeholder :: — :: Content''',
 notes=['اسم Figma «card slider»: هي بطاقة تنسدل للأسفل، وما فيها تمرير أفقي، فالاسم المقترح MCO_SlideCard.', 'Structure جديدة: MCO_SlideField (Label · Value · Icon).'],
 preview='SLIDE')

C['dcard'] = dict(name='بطاقة التفاصيل', mco='MCO_DetailsCard', kind=BLOCK, figma='424:7542',
 summary='عرض بيانات للقراءة فقط: عنوان قسم بشريط عمودي، وتحته نص أو مؤشرات أو جدول أو صور أو أطراف.',
 inputs=[('Title', 'Text', 'عنوان القسم')],
 placeholders=[('Content', 'محتوى القسم (الجدول تحت)')],
 variants=[('نص قصير', 'Expression · Style Classes = "mco-xtext__text"', '«short text»'), ('نص طويل', 'MCO_ExpandableText', '«long text» مع «عرض المزيد»'),
           ('مؤشرات', 'MCO_InfoList · ExtraClass = "mco-info--lg"', '«indicators»'), ('جدول', 'ودجت Table', '«table»'),
           ('صور', 'MCO_Gallery', '«media»'), ('أطراف', 'Container بكلاس mco-person-group فيه MCO_PersonCard', '«persona»')],
 tree='''MCO_DetailsCard :: — :: Block
  HTML Element (section) :: "mco-dcard " + ExtraClass
    HTML Element (h3) :: mco-dcard__title
      Expression :: — :: Value = Title
    Container :: mco-dcard__body
      Placeholder :: — :: Content''',
 notes=['هذا المكوّن هو «عرض البيانات للقراءة فقط»: صفحات تفاصيل السجل تتكوّن من عدة بطاقات منه.'],
 preview='DCARD')

C['xtext'] = dict(name='النص القابل للتوسيع', mco='MCO_ExpandableText', kind=BLOCK, figma='424:8064',
 summary='نص طويل يظهر منه أول أسطره مع تلاشٍ تدريجي، وزر «عرض المزيد» يفتحه كاملاً.',
 inputs=[('Text', 'Text', ''), ('ShowToggle', 'Boolean = True', 'False للنصوص القصيرة'), ('MoreLabel', 'Text = "عرض المزيد"', ''), ('LessLabel', 'Text = "عرض أقل"', '')],
 tree='''MCO_ExpandableText :: — :: Block · متغير محلي Open = False
  Container :: "mco-xtext" + If(ShowToggle and not Open, " is-clamped", "") + " " + ExtraClass
    HTML Element (p) :: mco-xtext__text
      Expression :: — :: Value = Text
    If :: — :: ShowToggle
      Button :: btn btn-tertiary btn-small :: OnClick → Open = not Open · aria-expanded = Open
        MCO_Icon :: — :: Name = "arrow-down" · ExtraClass = If(Open, "mco-rot", "")
        Text :: — :: If(Open, LessLabel, MoreLabel)''',
 notes=['المنصة ما تقيس طول النص؛ مرّر ShowToggle = Length(Text) > 400 تقريباً.'],
 preview='XTEXT')

C['gallery'] = dict(name='معرض الصور', mco='MCO_Gallery', kind=BLOCK, figma='424:7930',
 summary='صور 280×169 في صف يتمرّر أفقياً، بزرين للتنقل على الطرفين.',
 inputs=[('Images', 'List of MCO_Image', '{URL, Alt}'), ('AriaLabel', 'Text = "صور النشاط"', '')],
 tree='''MCO_Gallery :: — :: Block
  Container :: "mco-gallery " + ExtraClass :: role = "region" · aria-label = AriaLabel
    Button :: mco-gallery__nav :: aria-label = "السابق" · OnClick → JavaScript: track.scrollBy({left: 300, behavior: 'smooth'})
      MCO_Icon :: — :: Name = "arrow-left" · IsFlipped = True
    List :: mco-gallery__track :: Source = Images · Name = Track
      Container :: mco-gallery__item
        Image :: — :: Type = External URL · URL = Images.Current.URL · Alt = Images.Current.Alt
    Button :: mco-gallery__nav :: aria-label = "التالي" · OnClick → JavaScript: track.scrollBy({left: -300, behavior: 'smooth'})
      MCO_Icon :: — :: Name = "arrow-left"''',
 notes=['الصفحة عربية، فالتمرير للأمام قيمته سالبة (scrollBy بقيمة -300).', 'Structure جديدة: MCO_Image (URL · Alt).'],
 preview='GALLERY')

C['person'] = dict(name='بطاقة الشخص', mco='MCO_PersonCard', kind=BLOCK, figma='424:7984',
 summary='صورة دائرية بإطار الهوية مع الاسم والمنصب والدولة، لعرض أطراف الزيارة أو الاجتماع.',
 inputs=[('Name', 'Text', ''), ('Role', 'Text', ''), ('Location', 'Text', 'اختياري'), ('PhotoURL', 'Text', 'بدون قيمة = الحرفان الأولان')],
 tree='''MCO_PersonCard :: — :: Block
  Container :: "mco-person " + ExtraClass
    Container :: mco-person__avatar
      If :: — :: PhotoURL <> ""
        Image :: — :: URL = PhotoURL · Alt = Name
      Else :: — ::
        Expression :: mco-person__initials :: Value = الحرفان الأولان من Name
    Container :: mco-person__info
      Expression :: mco-person__name :: Value = Name
      Expression :: mco-person__role :: Value = Role
      If :: — :: Location <> ""
        Container :: mco-person__place
          MCO_Icon :: — :: Name = "location" · Size = 16
          Expression :: — :: Value = Location''',
 notes=['طرفان جنباً إلى جنب: Container بكلاس mco-person-group، وفي كل عمود Container بكلاس mco-person-group__col فيه HTML Element (h4) بكلاس mco-person-group__title ثم MCO_PersonCard.'],
 preview='PERSON')

C['addbanner'] = dict(name='شريط الإضافة مع العدّاد', mco='MCO_AddBanner', kind=BLOCK, figma='755:7538',
 summary='دعوة لإضافة عنصر جديد مع مؤشر عدد المضاف من الحد الأقصى، مثل الأهداف الاستراتيجية.',
 inputs=[('Title', 'Text', ''), ('HelperText', 'Text', 'مثل «أهداف · يمكنك إضافة 3 أهداف أخرى»'), ('Current', 'Integer', 'عدد المضاف'), ('Total', 'Integer', 'الحد الأقصى'),
         ('Icon', 'Text = "record-circle"', ''), ('ButtonLabel', 'Text', ''), ('ShowButton', 'Boolean = True', 'False عند بلوغ الحد'),
         ('ShowProgress', 'Boolean = True', 'False في نوع الزرّين')],
 events=[('OnAdd', '—')],
 placeholders=[('Actions', 'نوع «tow actions»: Container بكلاس mco-addbanner__actions فيه "btn" (إعادة بملاحظات، back-square) ثم "btn btn-primary" (قبول الطلب، verify)، و ShowButton = False')],
 tree='''MCO_AddBanner :: — :: Block · OnParametersChanged: قائمة Steps بأرقام 0 … Total-1
  Container :: "mco-addbanner " + ExtraClass
    Container :: mco-addbanner__tile
      MCO_Icon :: — :: Name = Icon
    Container :: mco-addbanner__content
      HTML Element (h3) :: mco-addbanner__title
        Expression :: — :: Value = Title
      If :: — :: ShowProgress
        Container :: mco-addbanner__progress
          List :: mco-addbanner__steps :: Source = Steps · aria-hidden = "true"
            Container :: "mco-addbanner__step" + If(Steps.Current < Current, " is-done", "")
          Container :: mco-addbanner__meta
            HTML Element (b) :: — ::
              Expression :: — :: Value = Current + " من " + Total
            Expression :: — :: Value = " " + HelperText
    If :: — :: ShowButton
      Button :: btn :: OnClick → OnAdd
        MCO_Icon :: — :: Name = Icon · Size = 20
        Text :: — :: ButtonLabel
    Placeholder :: — :: Actions''',
 notes=['الفرق عن MCO_AddMore: هذا للإضافة المحدودة بعدد ظاهر.', 'الزخرفة (الدوائر) خلفية من الثيم، فما تحتاج ملفاً.'],
 preview='ADDBANNER')

# تحديثات من Figma على مكوّنات موجودة
C['sidemenu']['placeholders'] = [('Logo', 'Container بكلاس mco-side__brand: صورة الشعار + Expression «منصة تواصل الوزراء»'), ('Footer', 'MCO_UserCard')]
C['sidemenu']['tree'] = C['sidemenu']['tree'].replace('''      Button :: mco-iconbtn mco-side__collapse :: OnClick → OnCollapse · aria-label = "طي القائمة"
        MCO_Icon :: — :: Name = "menu"''', '''      Button :: mco-iconbtn mco-side__collapse :: OnClick → OnCollapse · aria-label = "طي القائمة"
        MCO_Icon :: — :: Name = If(IsCollapsed, "collapse-menu", "expand-menu")''').replace('aria-label = "طي القائمة"', 'aria-label = If(IsCollapsed, "فتح القائمة", "طي القائمة") · aria-expanded = not IsCollapsed')
C['sidemenu']['notes'] = ['محدّث من Figma (74:6099): الشعار مع اسم المنصة أعلى القائمة، وبطاقة المستخدم أسفلها، ومسافة 24px بين العناصر. ارتفاعها 847px على الأقل، وداخل MCO_LayoutBase تمتد بطول الشاشة.', 'زر الطي/الفتح أسفل القائمة على اليمين (أيقونة expand-menu)، وعند الطي يتوسّط (أيقونة collapse-menu). جرّب الضغط عليه في المعاينة.', 'الطي يدار بمتغير IsCollapsed في الشاشة أو الـ Layout: OnCollapse ← IsCollapsed = not IsCollapsed. عند الطي يبقى الشعار والأيقونات فقط، وتختفي بطاقة المستخدم.']
C['sidemenu']['figma'] = '74:6099'
C['sidemenu'].pop('preview_js', None); C['sidemenu']['preview'] = 'SIDEMENU2'
C['table']['figma'] = '2:20849'
C['table']['variants'] = [('رقم أو رمز', 'Expression · Style Classes = "mco-cell--number"', 'عريض بلون brand-secondary'), ('الحالة', 'MCO_StatusBadge داخل الخلية', ''),
           ('إجراءات الصف', 'Button · "btn btn-primary" و "btn"', 'كما في Figma'), ('فوق الجدول', 'MCO_FilterBar', 'بحث + قوائم تصفية'), ('تحت الجدول', 'MCO_PaginationFooter', ''),
           ('على الجوال', 'If IsPhone() → List من MCO_MobileTableCard', 'IsPhone من OutSystemsUI')]
C['table']['preview'] = 'TABLE2'

C['loader'] = dict(name='مؤشر التحميل', mco='MCO_Loader', kind=BLOCK, figma='630:6468',
 summary='شعار السيفين والنخلة يمتلئ بتدرّج الهوية من الأسفل للأعلى بحافة موجية، ويتكرر حتى ينتهي التحميل. يُستخدم داخل جزء من الصفحة أو كصفحة تحميل كاملة.',
 inputs=[('Size', 'Text = "default"', 'sm: 40px · default: 80px · lg: 160px'), ('IsFullPage', 'Boolean = False', 'True: يغطي الشاشة بخلفية الصفحة ويتوسطها'),
         ('Label', 'Text', 'الافتراضي «جارٍ التحميل». يُقرأ لقارئ الشاشة دائماً، ويظهر تحت الشعار في الصفحة الكاملة فقط')],
 variants=[('داخل جزء', 'Size = "sm" أو "default"', 'في مكان المحتوى حتى يوصل'), ('صفحة كاملة', 'IsFullPage = True · Size = "lg"', 'أول تحميل للتطبيق أو بين الشاشات')],
 tree='''MCO_Loader :: — :: Block
  If :: — :: IsFullPage
    Container :: "mco-loader-page " + ExtraClass :: role = "status"
      Container :: "mco-loader" + If(Size = "sm", " mco-loader--sm", If(Size = "lg", " mco-loader--lg", "")) :: aria-hidden = "true"
        Container :: mco-loader__level
          Container :: mco-loader__fill
      Expression :: mco-loader-page__label :: Value = Label
  Else :: — ::
    Container :: "mco-loader" + If(Size = "sm", " mco-loader--sm", If(Size = "lg", " mco-loader--lg", "")) + " " + ExtraClass :: role = "status" · aria-label = Label
      Container :: mco-loader__level
        Container :: mco-loader__fill''',
 notes=['الألوان من التوكنز: الشعار الفارغ color-bg-brand-soft، والتدرّج color-bg-loader-start (أسفل) ← color-bg-loader-end (أعلى)، وتتبدّل في الوضع الداكن تلقائياً.',
        'الشعار مرسوم كـ mask في الثيم، فلا تضف صورة أو أيقونة داخل الـ Block.',
        'مدة الدورة 2.6 ثانية، وتتغيّر بالمتغير ‎--mco-loader-dur‎ على الـ Container. مع إعداد «تقليل الحركة» في الجهاز يبطؤ الامتلاء وتتوقف الموجة.',
        'اعرضه بـ If على متغير IsLoading في الشاشة، واخفه بعد ما توصل البيانات (OnAfterFetch).'],
 preview='LOADER')

# ───────────────────────── تحديث مكتبة Figma (نوفمبر 2026) ─────────────────────────

C['csteps'] = dict(name='مؤشر الخطوات الدائري', mco='MCO_StepsBar', kind=BLOCK, figma='643:7093',
 summary='خطوات بدوائر مرقّمة وخطوط بينها، تحت كل دائرة «الخطوة X من N» وعنوانها. ثلاث حالات: لم يبدأ، قيد التعبئة، تم التعبئة. يُستخدم داخل شريط التنقل (Type = stepper) أو فوق نموذج طويل.',
 inputs=[('Steps', 'List of Text', 'عناوين الخطوات'), ('Current', 'Integer', 'فهرس الخطوة الحالية، يبدأ من 0')],
 tree="""MCO_StepsBar :: — :: Block
  HTML Element (ol) :: "mco-csteps " + ExtraClass :: aria-label = "خطوات النموذج"
    List :: — :: Source = Steps
      If :: — :: Steps.CurrentRowNumber > 0
        HTML Element (li) :: mco-csteps__line :: aria-hidden = "true"
      HTML Element (li) :: "mco-cstep" + If(Steps.CurrentRowNumber < Current, " is-done", If(Steps.CurrentRowNumber = Current, " is-active", "")) :: aria-current = "step" للحالية
        Container :: mco-cstep__dot
          If :: — :: Steps.CurrentRowNumber < Current
            MCO_Icon :: — :: Name = "check" · Size = 16
          Else :: — ::
            Expression :: — :: Value = Steps.CurrentRowNumber + 1
        Container :: mco-cstep__text
          Expression :: mco-cstep__caption :: Value = "الخطوة " + (Steps.CurrentRowNumber + 1) + " من " + Steps.Length
          Expression :: mco-cstep__title :: Value = Steps.Current""",
 notes=['داخل MCO_Navbar بـ Type = "stepper": ضع الـ Block في Placeholder ‏Steps مع ExtraClass = "mco-nav__steps" فيأخذ الشريط بارتفاع 68px تحت العنوان.',
        'هو مؤشر الخطوات المعتمد في الدليل (حلّ محل مؤشر الأسهم MCO_Stepper). على الجوال تختفي عناوين الخطوات غير الحالية، وللنماذج الطويلة على الجوال يمكن استخدام MCO_WizardProgress.'],
 preview='CSTEPS')

C['avatar'] = dict(name='الصورة الرمزية', mco='MCO_Avatar', kind=BLOCK, figma='664:7171',
 summary='دائرة 42px: صورة الشخص بحد خفيف، أو أيقونة شخص على bg-brand-soft بدون صورة، أو زر إضافة شخص.',
 inputs=[('Type', 'Text = "default"', 'image · default · add'), ('ImageURL', 'Text', 'مع image'), ('Name', 'Text', 'نص بديل للصورة أو لقارئ الشاشة')],
 events=[('OnAdd', 'مع add فقط')],
 tree="""MCO_Avatar :: — :: Block
  If :: — :: Type = "add"
    Button :: "mco-avatar " + ExtraClass :: OnClick → OnAdd · aria-label = "إضافة شخص"
      MCO_Icon :: — :: Name = "profile-add" · Size = 16
  Else :: — ::
    Container :: "mco-avatar" + If(Type = "image", " mco-avatar--image", "") + " " + ExtraClass :: role = "img" · aria-label = Name
      If :: — :: Type = "image"
        Image :: — :: URL = ImageURL · Alt = ""
      Else :: — ::
        MCO_Icon :: — :: Name = "user" · Size = 16""",
 preview='AVATAR')

C['ifield'] = dict(name='حقل المعلومة', mco='MCO_InfoField', kind=BLOCK, figma='656:7158',
 summary='عنوان رمادي 16px وقيمة عريضة 20px بلون text-brand. أنواع: نص، أو دولة مع علمها، أو تصنيف كرقاقة. هو الحقل داخل بطاقة السجل.',
 inputs=[('Label', 'Text', ''), ('Value', 'Text', ''), ('Type', 'Text = "text"', 'text · country · chip'), ('FlagURL', 'Text', 'مع country')],
 tree="""MCO_InfoField :: — :: Block
  Container :: "mco-ifield " + ExtraClass
    Expression :: mco-ifield__label :: Value = Label
    If :: — :: Type = "chip"
      Expression :: mco-ifield__chip :: Value = Value
    Else :: — ::
      Container :: mco-ifield__value
        If :: — :: Type = "country"
          Image :: mco-ifield__flag :: URL = FlagURL · Alt = ""
        Expression :: — :: Value = Value""",
 preview='IFIELD')

C['datetile'] = dict(name='مربع التاريخ', mco='MCO_DateTile', kind=BLOCK, figma='718:7416',
 summary='مربع 64px يعرض التاريخ كتقويم: شريط الشهر بلون icon-brand-strong، ثم اليوم 22px عريض، ثم السنة.',
 inputs=[('Date', 'Date', '')],
 tree="""MCO_DateTile :: — :: Block
  Container :: "mco-datetile " + ExtraClass :: role = "img" · aria-label = FormatDate(Date, "d MMMM yyyy")
    Expression :: mco-datetile__month :: Value = اسم الشهر من Date
    Expression :: mco-datetile__day :: Value = Day(Date)
    Expression :: mco-datetile__year :: Value = Year(Date)""",
 notes=['اسم الشهر بالعربي يُؤخذ من Multilingual أو من Static Entity بأسماء الشهور، حسب لغة التطبيق.'],
 preview='DATETILE')

C['fact'] = dict(name='عنصر الحقيقة', mco='MCO_FactItem', kind=BLOCK, figma='718:7473',
 summary='معلومة قصيرة بأيقونة في دائرة 40px، وعنوان 13px وقيمة عريضة 15px. ثلاث نغمات: الهوية، النجاح، أو شارة حالة بدل القيمة.',
 inputs=[('Label', 'Text', ''), ('Value', 'Text', ''), ('Icon', 'Text', ''), ('Tone', 'Text = "brand"', 'brand · success · status'), ('Status', 'MCO_Status Identifier', 'مع status')],
 tree="""MCO_FactItem :: — :: Block
  Container :: "mco-fact" + If(Tone = "success", " mco-fact--success", "") + " " + ExtraClass
    If :: — :: Tone <> "status"
      Container :: mco-fact__icon
        MCO_Icon :: — :: Name = Icon · Size = 20
    Container :: mco-fact__text
      Expression :: mco-fact__label :: Value = Label
      If :: — :: Tone = "status"
        MCO_StatusBadge :: — :: Status = Status · Label = Value
      Else :: — ::
        Expression :: mco-fact__value :: Value = Value""",
 notes=['داخل رأس صفحة التفاصيل (MCO_DetailHeader) تنفصل العناصر بخط تلقائياً.'],
 preview='FACT')

C['cardhead'] = dict(name='رأس البطاقة', mco='MCO_CardHeader', kind=BLOCK, figma='718:8456',
 summary='عنوان قسم 20px بلون text-brand يسبقه شريط عمودي 4×24، ومعه عدّاد اختياري في كبسولة.',
 inputs=[('Title', 'Text', ''), ('Count', 'Integer = -1', 'أقل من 0 = بدون عدّاد')],
 tree="""MCO_CardHeader :: — :: Block
  Container :: "mco-cardhead " + ExtraClass
    HTML Element (h3) :: mco-cardhead__title
      Expression :: — :: Value = Title
    If :: — :: Count >= 0
      Expression :: mco-cardhead__count :: Value = Count""",
 notes=['الشريط العمودي مرسوم من الثيم (::before)، فما يحتاج عنصر.'],
 preview='CARDHEAD')

C['activity'] = dict(name='بطاقة النشاط', mco='MCO_ActivityCard', kind=BLOCK, figma='719:7630',
 summary='بطاقة نشاط في شبكة: مربع التاريخ مع التصنيف الرئيسي، ثم فاصل، ثم التصنيف الفرعي والهدف المرتبط.',
 inputs=[('Date', 'Date', ''), ('MainCategory', 'Text', ''), ('SubCategory', 'Text', ''), ('Goal', 'Text', '')],
 tree="""MCO_ActivityCard :: — :: Block
  HTML Element (article) :: "mco-activity " + ExtraClass
    Container :: mco-activity__top
      MCO_DateTile :: — :: Date = Date
      Container :: mco-activity__kv
        Expression :: mco-activity__label :: Value = "التصنيف الرئيسي"
        Expression :: mco-activity__value :: Value = MainCategory
    Container :: mco-activity__divider
    Container :: mco-activity__fields
      Container :: mco-activity__kv
        Expression :: mco-activity__label :: Value = "التصنيف الفرعي"
        Expression :: mco-activity__value :: Value = SubCategory
      Container :: mco-activity__kv
        Expression :: mco-activity__label :: Value = "هدف التواصل الاستراتيجي المرتبط"
        Expression :: mco-activity__value :: Value = Goal""",
 notes=['تُعرض البطاقات في شبكة تحت MCO_CardHeader: Container بـ display grid وثلاثة أعمدة على سطح المكتب وعمود على الجوال.'],
 preview='ACTIVITY')

C['file'] = dict(name='عنصر الملف', mco='MCO_FileItem', kind=BLOCK, figma='719:7695',
 summary='ملف مرفق: أيقونة نوعه واسمه وتاريخ الرفع والحجم، وزرّا عرض وتحميل في نهاية السطر، وسطر ملاحظات اختياري تحته.',
 inputs=[('FileName', 'Text', ''), ('Extension', 'Text', 'pdf · doc · png · jpg · zip · txt'), ('Meta', 'Text', 'مثل «رُفع في 22-05-2026 · 1.2 ميجابايت»'), ('Notes', 'Text', 'بدون قيمة = بدون سطر الملاحظات')],
 events=[('OnView', '—'), ('OnDownload', '—')],
 tree="""MCO_FileItem :: — :: Block
  HTML Element (article) :: "mco-file " + ExtraClass
    Container :: mco-file__row
      Container :: "mco-filetype mco-filetype--" + ToLower(Extension) :: aria-hidden = "true"
        Expression :: mco-filetype__ext :: Value = Extension
      Container :: mco-file__meta
        Expression :: mco-file__name :: Value = FileName
        Expression :: mco-file__sub :: Value = Meta
      Container :: mco-file__actions
        Button :: btn btn-small :: OnClick → OnView · Text = "عرض"
        Button :: btn btn-tertiary btn-small :: OnClick → OnDownload · Text = "تحميل"
    If :: — :: Notes <> ""
      Container :: mco-file__notes
        HTML Element (b) :: — :: "الملاحظات:"
        Expression :: — :: Value = Notes""",
 notes=['أيقونة نوع الملف مرسومة بالـ CSS (ورقة بزاوية مطوية وشريط بلون النوع)، وهي تقريب لمكوّن «File Types» في Figma. لاستخدام رسومات Figma نفسها، صدّرها SVG وضعها Image بدل الـ Container.'],
 preview='FILE')

C['dhead'] = dict(name='رأس صفحة التفاصيل', mco='MCO_DetailHeader', kind=BLOCK, figma='719:7763',
 summary='أعلى صفحة تفاصيل سجل: علم أو شعار، وعنوان 24px مع شارة الحالة، ووصف مختصر، وزر تعديل في نهاية السطر، وتحتها صف من MCO_FactItem.',
 inputs=[('Title', 'Text', ''), ('Description', 'Text', ''), ('FlagURL', 'Text', 'علم الدولة أو شعار الجهة (60×40)'), ('Status', 'MCO_Status Identifier', ''), ('StatusLabel', 'Text', ''), ('ShowEdit', 'Boolean = True', '')],
 events=[('OnEdit', '—')],
 placeholders=[('Facts', 'من 2 إلى 4 MCO_FactItem')],
 tree="""MCO_DetailHeader :: — :: Block
  HTML Element (section) :: "mco-dhead " + ExtraClass
    Container :: mco-dhead__top
      Container :: mco-dhead__id
        Image :: mco-dhead__flag :: URL = FlagURL · Alt = ""
        Container :: mco-dhead__text
          Container :: mco-dhead__titlerow
            HTML Element (h2) :: mco-dhead__title
              Expression :: — :: Value = Title
            MCO_StatusBadge :: — :: Status = Status · Label = StatusLabel
          HTML Element (p) :: mco-dhead__desc
            Expression :: — :: Value = Description
      If :: — :: ShowEdit
        Button :: btn btn-cancel btn-mobile :: OnClick → OnEdit · Text = "تعديل"
    Container :: mco-dhead__facts
      Placeholder :: — :: Facts""",
 notes=['الحقائق تتوزع بالتساوي ويفصلها خط، وعلى الجوال تصير فوق بعض.'],
 preview='DHEAD')
