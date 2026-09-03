import json, re, os
base='/tmp/60fps'
records=[]
for slug in open(f'{base}/batch1.txt').read().split():
    meta=json.load(open(f'{base}/shots/{slug}/meta.json'))
    prompt=open(f'{base}/prompts/{slug}.md').read().strip()
    first=prompt.split('\n\n')[0].strip()
    m=re.search(r'Pattern:\s*(.+)', prompt)
    pattern=m.group(1).strip() if m else ''
    cat='Interaction' if slug.endswith('-interaction') else 'Animation'
    app=slug.split('-')[0]
    appname={'x':'X','h':'H&M','goat':'GOAT','cred':'CRED','lake':'Lake','cobot':'Cobot','play':'Play'}.get(app, app.capitalize())
    records.append({
        'id': f'60fps:{slug}',
        'source': '60fps',
        'slug': slug,
        'title': meta['title'],
        'category': cat,
        'desc': meta['desc'],
        'author': appname,
        'authorUrl': meta['url'],
        'published': '2026-09-04T00:00:00.000Z',
        'originalUrl': meta['url'],
        'pageUrl': meta['url'],
        'media': [{'poster': meta['poster'], 'src': meta['video'], 'type': 'video', 'montage': f'frames/60fps-{slug}.jpg'}],
        'summary': first,
        'frames': [],
        'mechanics': {'Pattern': [pattern] if pattern else [], 'Content type': ['interactive' if cat=='Interaction' else 'passive animation'], 'Source': ['60fps.design']},
        'prompt': prompt,
    })
data=json.load(open('/tmp/insp-site/interactions.json'))
existing={r['id'] for r in data}
new=[r for r in records if r['id'] not in existing]
data.extend(new)
json.dump(data, open('/tmp/insp-site/interactions.json','w'), indent=1)
print('added', len(new), 'total', len(data))
