"""Static semantic checks. Does not replace Minecraft's content log/runtime tests."""
from pathlib import Path
import json,uuid,zipfile,io,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]; checks=0

def check(cond,msg):
 global checks
 assert cond,msg
 checks+=1

def read(p):return json.loads((ROOT/p).read_text())
for pack in ('BP','RP'):
 for f in (ROOT/pack).rglob('*.json'):
  json.loads(f.read_text());checks+=1
bp=read('BP/manifest.json');rp=read('RP/manifest.json');version=read('package.json')['version'];v=[int(x) for x in version.split('.')]
uuids=[]
for m in (bp,rp):
 check(m['format_version']==2,'manifest format')
 check(m['header']['version']==v,'version coherent')
 check(m['header']['min_engine_version']==[1,26,50],'engine pin')
 uuids.append(m['header']['uuid']);uuids += [a['uuid'] for a in m['modules']]
 for mod in m['modules']:check(mod['version']==v,'module version')
for u in uuids:uuid.UUID(u);checks+=1
check(len(uuids)==len(set(uuids)),'unique UUIDs')
check(any(d.get('uuid')==rp['header']['uuid'] and d['version']==v for d in bp['dependencies']),'RP dependency')
check(any(d.get('module_name')=='@minecraft/server' and d['version']=='2.10.0' for d in bp['dependencies']),'stable script pin')
for m in bp['modules']:
 if m['type']=='script':check((ROOT/'BP'/m['entry']).exists(),'script entry exists')
e=read('BP/entities/broom.json')['minecraft:entity'];c=e['components'];events=e['events'];groups=e['component_groups']
check(e['description']['identifier']=='witchbroom:broom','entity identifier')
check(c['minecraft:rideable']['seat_count']==1,'one seat')
check(c['minecraft:physics']['has_collision'],'native collision')
check('minecraft:free_camera_controlled' in c and 'minecraft:vertical_movement_action' in c,'current native controls')
check('minecraft:input_air_controlled' not in c and 'minecraft:pushable' not in c,'deprecated components excluded')
check('minecraft:persistent' in c and 'minecraft:despawn' not in c,'persistence')
check(groups['witchbroom:flying']['minecraft:physics']['has_gravity']==False,'flying gravity off')
check(groups['witchbroom:landed']['minecraft:physics']['has_gravity']==True,'landing gravity on')
check('witchbroom:landed' in events['witchbroom:land']['add']['component_groups'],'explicit restoration')
check('witchbroom:flying' in events['witchbroom:land']['remove']['component_groups'],'remove flight group')
for key in ('on_rider_enter_event','on_rider_exit_event'):check(c['minecraft:rideable'][key] in events,'rider event exists')
check((ROOT/'BP'/c['minecraft:loot']['table']).exists(),'loot reference')
for action in c['minecraft:interact']['interactions']:
 check(action['on_interact']['event'] in events,'pickup event')
 check((ROOT/'BP'/action['spawn_items']['table']).exists(),'pickup loot')
 check('is_sneaking' in json.dumps(action),'toggle-friendly crouch')
item=read('BP/items/broom.json')['minecraft:item'];check(item['components']['minecraft:entity_placer']['entity']==e['description']['identifier'],'placer reference')
recipe=read('BP/recipes/broom.json')['minecraft:recipe_shaped'];check(recipe['result']['item']==item['description']['identifier'],'recipe result')
pattern=''.join(recipe['pattern']);check(pattern.count('S')==2 and pattern.count('A')==1 and pattern.count('W')==3,'craft recipe quantities')
client=read('RP/entity/broom.entity.json')['minecraft:client_entity']['description'];check(client['identifier']==e['description']['identifier'],'client id')
for t in client['textures'].values():check((ROOT/'RP'/(t+'.png')).exists(),'entity texture')
geo=read('RP/models/entity/broom.geo.json')['minecraft:geometry'][0];check(geo['description']['identifier']==client['geometry']['default'],'geometry reference')
with Image.open(ROOT/'RP/textures/entity/broom.png') as im:
 check(im.size==(geo['description']['texture_width'],geo['description']['texture_height']),'atlas dimensions');w,h=im.size
bones={b['name'] for b in geo['bones']};check('broom' in bones,'animation root')
for bone in geo['bones']:
 if 'parent' in bone:check(bone['parent'] in bones,'parent bone')
 for cube in bone.get('cubes',[]):
  check(all(x>0 for x in cube['size']),'nonzero cubes')
  for face in cube['uv'].values():
   u,vv=face['uv'];du,dv=face['uv_size'];check(0<=u<=w and 0<=u+du<=w and 0<=vv<=h and 0<=vv+dv<=h,'UV in atlas')
rc=read('RP/render_controllers/broom.render_controllers.json')['render_controllers'];check(all(r in rc for r in client['render_controllers']),'render controllers')
anim=read('RP/animations/broom.animation.json')['animations'];check(all(a in anim for a in client['animations'].values()),'animation refs')
for a in anim.values():check(set(a['bones'])<=bones,'animated bones exist')
tex=read('RP/textures/item_texture.json')['texture_data'];key=item['components']['minecraft:icon']['textures']['default'];check(key in tex,'item atlas reference');check((ROOT/'RP'/(tex[key]['textures']+'.png')).exists(),'item PNG')
particle=read('RP/particles/spark.json')['particle_effect'];check((ROOT/'RP'/(particle['description']['basic_render_parameters']['texture']+'.png')).exists(),'particle texture')
for lang in ('en_US','ja_JP'):
 lines=(ROOT/f'RP/texts/{lang}.lang').read_text().splitlines();keys=[a.split('=',1)[0] for a in lines if '=' in a];check(len(keys)==len(set(keys)),'unique language keys')
 for key in ('item.witchbroom:broom.name','action.interact.witchbroom.ride','action.interact.witchbroom.pack','witchbroom.controls','witchbroom.landing'):check(key in keys,'localized string')
for p in ('BP/pack_icon.png','RP/pack_icon.png','RP/textures/items/broom.png','RP/textures/particle/spark.png'):
 with Image.open(ROOT/p) as im:im.verify();checks+=1
addon=ROOT/'dist'/f'Moonweave_Broom_v{version}.mcaddon'
with zipfile.ZipFile(addon) as z:
 check(z.testzip() is None,'addon ZIP CRC');check(len(z.namelist())==3,'outer ZIP includes two packs and guide')
 for pack in ('BP','RP'):
  with zipfile.ZipFile(io.BytesIO(z.read(f'Moonweave_{pack}_v{version}.mcpack'))) as inner:
   check(inner.testzip() is None,'pack ZIP CRC');check('manifest.json' in inner.namelist(),'manifest at pack root')
   check(not any(x.startswith('/') or '..' in Path(x).parts for x in inner.namelist()),'safe ZIP paths')
   for name in inner.namelist():check(inner.read(name)==(ROOT/pack/name).read_bytes(),'pack source byte match')
print(f'PASS: {checks} structural/reference/package assertions (not game-runtime validation)')
print('SHA256 '+hashlib.sha256(addon.read_bytes()).hexdigest())
