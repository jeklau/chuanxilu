import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import json,re,os,hashlib
os.chdir(ROOT); os.makedirs('public',exist_ok=True); os.makedirs('dist',exist_ok=True)
data=open('data/all.json').read()
t=open('src/template.html').read()
assert '/*__DATA__*/null' in t
page=t.replace('/*__DATA__*/null',data)
ver=hashlib.sha1(page.encode()).hexdigest()[:8]
head,body=page.split('<div class="wrap">',1)
full=('<!doctype html>\n<html lang="zh-CN">\n<head>\n<meta charset="utf-8">\n'
 '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
 '<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}[hidden]{display:none!important}img{max-width:100%}</style>\n'
 +head+'</head>\n<body>\n<div class="wrap">'+body+'\n</body>\n</html>\n')
open('public/index.html','w').write(full)
# artifact 版：去掉只在自有域名有意义的 manifest / 图标链接
art=re.sub(r'<link rel="(manifest|icon|apple-touch-icon)"[^>]*>\n','',page)
open('dist/artifact.html','w').write(art)
sw=open('src/sw.js').read().replace('__VER__',ver)
open('public/sw.js','w').write(sw)
print('version',ver,'index',os.path.getsize('public/index.html'))
