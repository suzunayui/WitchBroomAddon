#!/usr/bin/env python3
"""Rebuild original cuboid geometry, exact UV atlas, inventory art, and faithful preview."""
import json, math, random
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
ROOT=Path(__file__).resolve().parents[1]
for d in ('RP/models/entity','RP/textures/entity','RP/textures/items','RP/textures/particle','BP'):
 (ROOT/d).mkdir(parents=True,exist_ok=True)
# A 128-square atlas, with individually addressed 16-square material swatches.
PAL={
 'walnut':(95,52,37),'woodlight':(133,78,44),'wooddark':(57,30,30),
 'straw':(211,161,60),'strawlight':(241,201,99),'strawdark':(170,113,40),
 'plum':(96,43,97),'plumlight':(144,70,137),'gold':(239,181,65),
 'aqua':(50,208,199),'aquashade':(20,117,142),'rope':(178,136,81)}
SLOTS={m:((i%8)*16,(i//8)*16) for i,m in enumerate(PAL)}
atlas=Image.new('RGBA',(128,128),(0,0,0,0)); ap=atlas.load(); rng=random.Random(19)
for name,(r,g,b) in PAL.items():
 ox,oy=SLOTS[name]
 for y in range(16):
  for x in range(16):
   delta=rng.choice([-8,-4,0,0,3,6])
   if name.startswith(('wood','walnut','straw')): delta+=(-10 if x in (2,8,13) else 0)+(7 if x in (3,9) else 0)
   if name in ('gold','aqua'): delta+=(9 if x<4 or y<3 else -6 if y>12 else 0)
   ap[ox+x,oy+y]=tuple(max(0,min(255,c+delta)) for c in (r,g,b))+(255,)
atlas.save(ROOT/'RP/textures/entity/broom.png')
cubes=[]; charm=[]; materials=[]
def cube(o,s,m='walnut',rot=None,pivot=None,target=None):
 u,v=SLOTS[m]; faces={f:{'uv':[u,v],'uv_size':[16,16]} for f in ['north','south','east','west','up','down']}
 c={'origin':o,'size':s,'uv':faces}
 if rot: c.update(rotation=rot,pivot=pivot or [o[i]+s[i]/2 for i in range(3)])
 (cubes if target is None else target).append(c); materials.append((c,m))
# Long, slightly crooked walnut handle. Forward is -Z.
cube([-.9,9,-14],[1.8,1.8,28])
cube([-.65,10.8,-12],[1.3,.22,22],'woodlight')
cube([-.85,9.3,-19],[1.7,1.6,6],'walnut',[12,0,0],[-.0,10,-14])
cube([-.3,10.7,-21],[1.5,1.4,3],'woodlight',[0,-9,0],[.45,11.4,-19.5])
cube([.2,11.1,-22],[.9,.85,1.2],'walnut')
# Small joint knot and carved golden bands on the handle.
cube([-.99,9.0,-8],[2,.45,1.3],'wooddark')
cube([-.99,10.4,-8],[2,.45,1.3],'woodlight')
for z in (-5.0,-3.8): cube([-1.01,8.89,z],[2.02,2.02,.45],'gold')
# Dense tapered straw core, with a strongly fanned rear silhouette.
cube([-1.8,8.2,10],[3.6,2.8,6],'strawdark')
cube([-2.5,8.1,14],[5,2.5,5],'straw')
cube([-3.3,8.05,18],[6.6,2.3,4],'straw')
# Separate reeds make the fringe golden and distinctly broom-like.
for i in range(15):
 x=-1.6+i*(3.2/14)
 zstart=11.8
 end=24-(i%4)*.28
 y=7.75+(i%3)*.15
 angle=x*11
 cube([x,y,zstart],[.52,.95,end-zstart],['straw','strawlight','strawdark'][i%3],[1.5,angle,0],[x+.26,y+.5,zstart])
for i in range(11):
 x=-1.5+i*.3; start=12.0
 cube([x,10.5+(i%2)*.13,start],[.5,.7,23.0+(i%3)*.3-start],['strawlight','straw','strawlight'][i%3],[0,x*11,0],[x+.25,10.6,start])
# Plum leather binding around the neck of the bristles.
for z,width in ((10.4,3.9),(13.15,4.4)):
 cube([-width/2,7.72,z],[width,.55,1.15],'plum')
 cube([-width/2,11.2,z],[width,.55,1.15],'plumlight')
 cube([-width/2,8.1,z],[.55,3.2,1.15],'plum')
 cube([width/2-.55,8.1,z],[.55,3.2,1.15],'plumlight')
# The front-facing gold clasp catches light.
cube([2.02,9.0,13.28],[.4,1.55,.85],'gold')
cube([2.43,9.3,13.48],[.1,.92,.45],'plum')
# A small turquoise crystal suspended beneath the shaft.
cube([.92,7.3,-.5],[.4,2.5,.4],'rope',target=charm)
cube([.89,6.7,-.52],[.46,.75,.46],'gold',target=charm)
cube([.35,4.4,-1.13],[1.5,1.75,1.5],'aqua',[0,45,0],[1.1,5.3,-.38],charm)
cube([.62,3.8,-.86],[.95,.65,.95],'aquashade',[0,45,0],[1.1,4.1,-.38],charm)
cube([.64,6.05,-.84],[.92,.6,.92],'gold',[0,45,0],[1.1,6.35,-.38],charm)
geo={'format_version':'1.12.0','minecraft:geometry':[{'description':{'identifier':'geometry.witchbroom.broom','texture_width':128,'texture_height':128,'visible_bounds_width':4,'visible_bounds_height':2,'visible_bounds_offset':[0,.55,0]},'bones':[{'name':'broom','pivot':[0,9.8,0],'cubes':cubes},{'name':'charm','parent':'broom','pivot':[1.1,9.8,-.3],'cubes':charm}]}]}
(ROOT/'RP/models/entity/broom.geo.json').write_text(json.dumps(geo,indent=2)+'\n')
# Hand-authored 32 px diagonal inventory sprite with transparent surroundings.
im=Image.new('RGBA',(32,32)); d=ImageDraw.Draw(im)
d.line([(13,20),(26,5),(28,4)],fill='#382333',width=4)
d.line([(13,19),(26,5),(28,4)],fill='#a1683d',width=2)
d.line([(15,17),(25,6)],fill='#d09a58',width=1)
d.polygon([(11,17),(16,21),(11,30),(2,25)],fill='#68422b')
d.polygon([(11,18),(15,21),(10,29),(3,25)],fill='#d1a448')
for a,b in [((11,20),(4,25)),((12,20),(6,27)),((13,21),(9,28))]: d.line([a,b],fill='#f4d47c',width=1)
d.line([(10,17),(16,22)],fill='#492841',width=4)
d.line([(10,17),(16,22)],fill='#954f96',width=2)
d.line([(11,18),(16,21)],fill='#e4b459',width=1)
d.line([(19,15),(21,19)],fill='#9e7845')
d.polygon([(21,17),(23,19),(21,22),(19,19)],fill='#36c7c5')
d.point((21,18),fill='#d4ffff')
for x,y in [(7,10),(27,24)]:
 d.line([(x-1,y),(x+1,y)],fill='#97e5df'); d.line([(x,y-1),(x,y+1)],fill='#97e5df')
im.save(ROOT/'RP/textures/items/broom.png')
star=Image.new('RGBA',(8,8)); sd=ImageDraw.Draw(star)
sd.polygon([(3,0),(4,0),(4,2),(5,3),(7,3),(7,4),(5,4),(4,5),(4,7),(3,7),(3,5),(2,4),(0,4),(0,3),(2,3),(3,2)],fill=(255,255,255,255))
star.save(ROOT/'RP/textures/particle/spark.png')
# Exact cuboid rasterizer: same geometry, rotations, UV atlas, no invented details.
def transform(c):
 o=np.array(c['origin']); s=np.array(c['size']); pts=np.array([o+[x*s[0],y*s[1],z*s[2]] for x,y,z in [(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]])
 if 'rotation' in c:
  rx,ry,rz=np.radians(c['rotation']);
  X=np.array([[1,0,0],[0,np.cos(rx),-np.sin(rx)],[0,np.sin(rx),np.cos(rx)]]);Y=np.array([[np.cos(ry),0,np.sin(ry)],[0,1,0],[-np.sin(ry),0,np.cos(ry)]]);Z=np.array([[np.cos(rz),-np.sin(rz),0],[np.sin(rz),np.cos(rz),0],[0,0,1]])
  p=np.array(c['pivot']); pts=(pts-p)@(Z@Y@X).T+p
 return pts
FACES=[('north',[0,3,2,1]),('south',[4,5,6,7]),('west',[0,4,7,3]),('east',[1,2,6,5]),('up',[3,7,6,2]),('down',[0,1,5,4])]
allpts=np.concatenate([transform(c) for c,m in materials]); print('Cubes:',len(materials),'bounds',allpts.min(0).round(3).tolist(),allpts.max(0).round(3).tolist())
def render(W,H,scale):
 eye=np.array([.50,.52,.69]);eye/=np.linalg.norm(eye)
 right=np.cross([0,1,0],eye);right/=np.linalg.norm(right)
 up=np.cross(eye,right); basis=np.array([right,up,eye])
 buf=np.zeros((H,W,4),dtype=np.uint8); depth=np.full((H,W),-np.inf)
 center=np.array([0,8.6,1]); light=np.array([-.3,.9,-.4]);light/=np.linalg.norm(light)
 for c,m in materials:
  pts=transform(c); q=(pts-center)@basis.T; q[:,0]=W/2+q[:,0]*scale; q[:,1]=H/2-q[:,1]*scale
  for fn,inds in FACES:
   face=pts[inds];normal=np.cross(face[1]-face[0],face[2]-face[0]); normal/=np.linalg.norm(normal)
   if np.dot(normal,eye)<=0:continue
   shade=.67+.33*max(0,np.dot(normal,light)); uv0=c['uv'][fn]['uv'];uvs=np.array([[0,16],[0,0],[16,0],[16,16]])+uv0
   for a,b,cc in [(0,1,2),(0,2,3)]:
    v=q[np.array(inds)[[a,b,cc]]];uv=uvs[[a,b,cc]]
    xmin=max(0,int(np.floor(v[:,0].min()))); xmax=min(W-1,int(np.ceil(v[:,0].max())));ymin=max(0,int(np.floor(v[:,1].min())));ymax=min(H-1,int(np.ceil(v[:,1].max())))
    if xmin>xmax or ymin>ymax:continue
    xx,yy=np.meshgrid(np.arange(xmin,xmax+1)+.5,np.arange(ymin,ymax+1)+.5)
    den=(v[1,1]-v[2,1])*(v[0,0]-v[2,0])+(v[2,0]-v[1,0])*(v[0,1]-v[2,1])
    if abs(den)<1e-7:continue
    w0=((v[1,1]-v[2,1])*(xx-v[2,0])+(v[2,0]-v[1,0])*(yy-v[2,1]))/den
    w1=((v[2,1]-v[0,1])*(xx-v[2,0])+(v[0,0]-v[2,0])*(yy-v[2,1]))/den;w2=1-w0-w1
    z=w0*v[0,2]+w1*v[1,2]+w2*v[2,2]; crop=depth[ymin:ymax+1,xmin:xmax+1];mask=(w0>=-1e-5)&(w1>=-1e-5)&(w2>=-1e-5)&(z>crop)
    U=np.clip((w0*uv[0,0]+w1*uv[1,0]+w2*uv[2,0]).astype(int),uv0[0],uv0[0]+15);V=np.clip((w0*uv[0,1]+w1*uv[1,1]+w2*uv[2,1]).astype(int),uv0[1],uv0[1]+15)
    tex=np.asarray(atlas)[V,U].copy();tex[:,:,:3]=(tex[:,:,:3]*shade).astype(np.uint8)
    buf[ymin:ymax+1,xmin:xmax+1][mask]=tex[mask];crop[mask]=z[mask]
 return Image.fromarray(buf)
W,H=1440,960
bg=Image.new('RGBA',(W,H),'#111422'); dr=ImageDraw.Draw(bg)
for k in range(105):
 x=rng.randint(30,W-30);y=rng.randint(30,H-30);dr.ellipse((x,y,x+2,y+2),fill='#34324e')
dr.ellipse((330,180,1130,820),fill='#191b2d',outline='#343047',width=2)
model=render(W,H,27)
bg.alpha_composite(model)
try:
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',30);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
except:font=small=ImageFont.load_default()
dr=ImageDraw.Draw(bg);dr.text((55,45),'THE WITCH’S BROOM',font=font,fill='#efe3c4');dr.text((57,90),'Walnut • golden straw • plum leather • turquoise charm',font=small,fill='#b9adbc');dr.text((57,H-57),'Resource-model preview · exact cuboid geometry and texture atlas · not a gameplay screenshot',font=small,fill='#8e8ba5')
bg.convert('RGB').save(ROOT/'art-preview.png')
# Original pack cover, composed from the same asset and celestial illustration.
icon=Image.new('RGBA',(256,256),'#171727');di=ImageDraw.Draw(icon)
di.rounded_rectangle((7,7,248,248),radius=30,fill='#252039',outline='#c7a461',width=3)
di.ellipse((36,33,220,217),fill='#3b2c47');di.ellipse((158,31,208,81),fill='#efdba3');di.ellipse((174,21,219,67),fill='#3b2c47')
mini=render(256,256,5.7);icon.alpha_composite(mini)
di=ImageDraw.Draw(icon)
for x,y in [(34,72),(220,137),(85,221),(129,31)]:di.line([(x-3,y),(x+3,y)],fill='#a7e6dc');di.line([(x,y-3),(x,y+3)],fill='#a7e6dc')
for pack in ('BP','RP'):icon.save(ROOT/pack/'pack_icon.png')
print('Generated art-preview.png and both pack icons')
