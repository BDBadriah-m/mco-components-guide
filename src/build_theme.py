# -*- coding: utf-8 -*-
"""يبني MCO_OutSystems_Theme.css من مصادر نظام التصميم.

المدخلات (في مجلد deps/ — طريقة جلبها في README.md):
  deps/tokens.json   ← project/tokens.json من artifact «MCO Design System»
  deps/bundle.css    ← project/components/bundle.css
  deps/bundle.js     ← project/components/bundle.js (منه تُؤخذ مسارات الأيقونات)
القوالب (هنا، تُعدَّل يدوياً):
  theme/theme_head.css   الأقسام 1 و3 إلى 6؛ القسم 2 يُولَّد مكان /*@TOKENS@*/
  theme/theme_extra.css  القسم 8؛ كلاسات الأيقونات تُولَّد مكان /*@ICONS@*/
المخرج: ../MCO_OutSystems_Theme.css
"""
import json, os, re, sys, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
DEPS = os.path.join(HERE, 'deps')
OUT = os.path.join(HERE, '..', 'MCO_OutSystems_Theme.css')
OUT_ICONS = os.path.join(os.path.dirname(OUT), 'MCO_Icons_All.css')

def tokens_block(t):
    out = ['/* ---------------------------------------------------------------------------',
           '   2.0 الخط والمسافات والزوايا والظلال من tokens.json (الألوان في 2 و2.2)',
           '   --------------------------------------------------------------------------- */',
           ':root {']
    # الألوان ما تُكتب هنا: أسماؤها القديمة صارت بدائل للتوكنز الدلالية (القسم 2.2)
    fam = t['type']['families'].get('sans')
    if fam:
        out.append('\n  /* الخط */\n  --font-sans: %s;' % fam)
    for key, label in (('spacing', 'المسافات'), ('radius', 'الزوايا'), ('shadow', 'الظلال')):
        if key in t:
            out.append('\n  /* %s */' % label)
            for tok in t[key]['tokens']:
                out.append('  --%s: %s;' % (tok['name'], tok['value']))
    out.append('}')
    return '\n'.join(out)

TOKENS_CSS = os.path.join(DEPS, 'mco-design-tokens-light-dark.css')
ROLES = os.path.join(HERE, 'theme', 'token_roles.json')

# توكنز إضافية بدون مقابل دلالي في ملف Figma (نفس القيمة الفاتحة، وقيمة داكنة من نفس السلّم)
EXTRA_TOKENS = {
    'mco-bg-light-grey':  ('#f6f6f7', 'var(--color-gray-900)'),
    'mco-font-secondary': ('#8e98a1', 'var(--color-gray-200)'),
    'mco-status-default': ('#999999', 'var(--color-gray-500)'),
}
DARK_SEL = '[data-theme="dark"]'

def semantic_block(roles):
    """القسم 2: ملف التوكنز الفاتح/الداكن كما هو + توكنز إضافية + الأسماء القديمة كبدائل."""
    out = ['/* ---------------------------------------------------------------------------',
           '   2. توكنز MCO — ملف «mco-design-tokens-light-dark.css» من Figma كما هو',
           '   الفاتح هو الافتراضي دائماً، والداكن فقط بـ <html data-theme="dark"> (إعداد الجهاز لا يغيّره).',
           '   لا يُعدَّل هنا: يُستبدل الملف في deps/ ويُعاد البناء.',
           '   --------------------------------------------------------------------------- */',
           open(TOKENS_CSS).read().strip(), '',
           '/* 2.1 توكنز إضافية خاصة بالثيم (ما لها مقابل في ملف Figma) */',
           ':root, [data-theme="light"] {']
    out += ['  --%s: %s;' % (k, v[0]) for k, v in EXTRA_TOKENS.items()]
    out += ['}', DARK_SEL + ' {'] + ['  --%s: %s;' % (k, v[1]) for k, v in EXTRA_TOKENS.items()] + ['}', '',
           '/* 2.2 الأسماء القديمة (tokens.json) كبدائل للتوافق — المكوّنات تستخدم الدلالية مباشرة */',
           ':root {'] + ['  --%s: var(--%s);' % (k, v['default']) for k, v in roles.items() if not k.startswith('_')] + ['}']
    return '\n'.join(out)

def apply_roles(css, roles):
    """يستبدل var(--قديم) بالتوكن الدلالي حسب الخاصية: color → text، background → bg، border/outline → border."""
    def role_of(prop):
        if prop.startswith('--'): return 'default'
        if prop in ('color', 'caret-color', 'fill', 'stroke') or prop.startswith('-webkit-text'): return 'text'
        if prop.startswith('background'): return 'bg'
        if 'border' in prop or prop.startswith('outline'): return 'border'
        return 'default'
    def decl(m):
        prop, val = m.group(1), m.group(2)
        r = role_of(prop)
        def rep(v):
            name = v.group(1)
            if name not in roles or name.startswith('_'): return v.group(0)
            return 'var(--%s' % roles[name].get(r, roles[name]['default'])
        return '%s:%s' % (prop, re.sub(r'var\(--([a-z0-9-]+)', rep, val))
    return re.sub(r'(--[\w-]+|[a-z-]+)\s*:([^;{}]*)', decl, css)

def icon_url(svg_inner, viewbox='0 0 24 24'):
    svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s">%s</svg>' % (viewbox, svg_inner.replace('currentColor', '#000'))
    enc = urllib.parse.quote(svg, safe=' =:/,;()-.').replace('"', '%22')
    return 'url("data:image/svg+xml,%s")' % enc

def icon_slug(name):
    """اسم كلاس صالح: أي حرف غير a-z0-9 يصير شرطة (ruler&pen → ruler-pen، aave-(aave) → aave-aave)"""
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9-]', '-', name.lower())).strip('-')

def icon_rule(name, svg_inner, viewbox='0 0 24 24'):
    return '.mco-i-%s { --mco-icon: %s; }' % (name, icon_url(svg_inner, viewbox))

def icons_block(bundle_js):
    m = re.search(r'var ICONS = (\{.*?\});\n', bundle_js, re.S)
    if not m:
        sys.exit('لم أجد ICONS في bundle.js')
    icons = json.loads(m.group(1))
    # أيقونات إضافية من مجموعة Vuesax الكاملة (theme/extra_icons.json) تحتاجها مكوّنات Figma الجديدة
    extra = os.path.join(HERE, 'theme', 'extra_icons.json')
    if os.path.exists(extra):
        for k, v in json.load(open(extra)).items():
            icons.setdefault(k, v)
    rules = [icon_rule(n, icons[n]) for n in sorted(icons)]
    # علامة الصح في الخط الزمني (مرسومة في bundle.js خارج ICONS)
    rules.append(icon_rule('check', '<path d="M1.2 5.2 5 8.8 12.8 1.2" fill="none" stroke="#000" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/>', '0 0 14 10'))
    return '\n'.join(rules), len(icons) + 1, icons

def main():
    t = json.load(open(os.path.join(DEPS, 'tokens.json')))
    bundle_css = open(os.path.join(DEPS, 'bundle.css')).read()
    bundle_js = open(os.path.join(DEPS, 'bundle.js')).read()
    head = open(os.path.join(HERE, 'theme', 'theme_head.css')).read()
    extra = open(os.path.join(HERE, 'theme', 'theme_extra.css')).read()
    icons, n, ICONS = icons_block(bundle_js)
    # القسم 7: bundle.css كما هو بدون سطري التعليق الأولين
    sec7 = '\n'.join(bundle_css.split('\n')[2:])
    roles = json.load(open(ROLES))
    body = apply_roles(head.replace('/*@TOKENS@*/', '/*@SEM@*/') + sec7 + extra, roles)
    css = body.replace('/*@SEM@*/', tokens_block(t) + '\n\n' + semantic_block(roles)).replace('/*@ICONS@*/', icons)
    # url(@icon:NAME) في القوالب ← data URI للأيقونة نفسها (للـ mask في عناصر لا نتحكم في HTML حقها)
    css = re.sub(r'url\(@icon:([a-z0-9-]+)\)', lambda m: icon_url(ICONS[m.group(1)]), css)
    used = set(re.findall(r'var\((--[a-z0-9-]+)', css))
    defined = set(re.findall(r'(--[a-z0-9-]+)\s*:', css))
    missing = sorted(used - defined)
    open(OUT, 'w').write(css)
    print('MCO_OutSystems_Theme.css:', len(css), 'bytes ·', n, 'icons')
    # كل أيقونات Vuesax outline (900) في ملف مستقل، عشان الثيم يبقى خفيف: يُضاف كـ Style Sheet ثاني عند الحاجة
    vx = {icon_slug(k): v for k, v in json.load(open(os.path.join(DEPS, 'vuesax-outline.json')))['icons'].items()}
    rest = [n_ for n_ in sorted(vx) if n_ not in ICONS and n_ != 'check']
    head_all = ('/* MCO_Icons_All.css — كل أيقونات Vuesax outline (%d أيقونة) ككلاسات mco-i-*.\n'
                '   يحتاج ملف الثيم MCO_OutSystems_Theme.css قبله (قاعدة .mco-icon فيه). الأيقونات المستخدمة في المكوّنات (%d) موجودة في الثيم نفسه،\n'
                '   وهذا الملف فيه الباقي فقط (%d). المصدر: deps/vuesax-outline.json من نظام التصميم. */\n') % (len(vx), n, len(rest))
    open(OUT_ICONS, 'w').write(head_all + '\n'.join(icon_rule(k, vx[k]['svg']) for k in rest) + '\n')
    print('MCO_Icons_All.css:', len(rest), 'icons')
    if missing:
        print('تنبيه — متغيرات مستخدمة وغير معرّفة:', missing)

if __name__ == '__main__':
    main()
