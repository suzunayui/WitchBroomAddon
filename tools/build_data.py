import json, uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def save(path,obj):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def uid(label):return str(uuid.uuid5(uuid.NAMESPACE_URL,'witchbroom:moonweave:v1:'+label))
VERSION=[0,1,0]
for pack,typ in [('BP','data'),('RP','resources')]:
 manifest={'format_version':2,'header':{'name':'pack.name','description':'pack.description','uuid':uid(pack),'version':VERSION,'min_engine_version':[1,26,50]},'modules':[{'type':typ,'uuid':uid(pack+':module'),'version':VERSION}],'metadata':{'authors':['dot']}}
 if pack=='BP':
  manifest['modules'].append({'type':'script','language':'javascript','uuid':uid('script'),'entry':'scripts/main.js','version':VERSION})
  manifest['dependencies']=[{'uuid':uid('RP'),'version':VERSION},{'module_name':'@minecraft/server','version':'2.10.0'}]
 save(pack+'/manifest.json',manifest)
 for lang in ['en_US','ja_JP']:
  p=ROOT/pack/'texts'/f'{lang}.lang';p.parent.mkdir(parents=True,exist_ok=True)
  ja=lang=='ja_JP';suffix='動作パック' if pack=='BP' else '見た目パック'
  p.write_text(('pack.name=月あかりのほうき '+suffix+'\npack.description=魔女の空飛ぶほうき v0.1.0 | Bedrock 26.50+\n') if ja else ('pack.name=Moonweave Broom '+pack+'\npack.description=A witch flying broom v0.1.0 | Bedrock 26.50+\n'))
 save(pack+'/texts/languages.json',['en_US','ja_JP'])
components={
 'minecraft:type_family':{'family':['witchbroom','inanimate']},
 'minecraft:collision_box':{'width':0.85,'height':1.0},
 'minecraft:physics':{'has_gravity':True,'has_collision':True,'push_towards_closest_space':True},
 'minecraft:can_fly':{},'minecraft:jump.static':{},'minecraft:is_tamed':{},'minecraft:persistent':{},
 'minecraft:health':{'value':10,'max':10},
 'minecraft:knockback_resistance':{'value':1.0},
 'minecraft:pushable_by_block':{},
 'minecraft:breathable':{'total_supply':15,'suffocate_time':0,'breathes_air':True,'breathes_water':True},
 'minecraft:damage_sensor':{'triggers':[{'cause':'fall','deals_damage':'no'}]},
 'minecraft:loot':{'table':'loot_tables/entities/broom.json'},
 'minecraft:movement':{'value':0.045},'minecraft:flying_speed':{'value':0.045},
 'minecraft:free_camera_controlled':{'strafe_speed_modifier':0.8,'backwards_movement_modifier':0.5},
 'minecraft:vertical_movement_action':{'vertical_velocity':0.22},
 'minecraft:behavior.player_ride_tamed':{'priority':1},
 'minecraft:body_rotation_always_follows_head':{},
 'minecraft:rideable':{'seat_count':1,'controlling_seat':0,'family_types':['player'],'pull_in_entities':False,'crouching_skip_interact':True,'rider_can_interact':False,'dismount_mode':'default','interact_text':'action.interact.witchbroom.ride','on_rider_enter_event':'witchbroom:mount','on_rider_exit_event':'witchbroom:land','seats':[{'position':[0,0.4,0],'third_person_camera_radius':4.0}]},
 'minecraft:interact':{'interactions':[{'on_interact':{'filters':{'all_of':[{'test':'is_family','subject':'other','value':'player'},{'test':'is_sneaking','subject':'other','value':True},{'test':'rider_count','subject':'self','operator':'equals','value':0}]},'event':'witchbroom:pack','target':'self'},'use_item':False,'cooldown':1.0,'interact_text':'action.interact.witchbroom.pack','spawn_items':{'table':'loot_tables/entities/broom.json','y_offset':0.5}}]},
 'minecraft:timer':{'looping':True,'time':2.0,'time_down_event':{'event':'witchbroom:reconcile','target':'self'}}
}
entity={'format_version':'1.26.50','minecraft:entity':{'description':{'identifier':'witchbroom:broom','is_spawnable':False,'is_summonable':True,'properties':{'witchbroom:occupied':{'type':'bool','default':False,'client_sync':True}}},'components':components,'component_groups':{
 'witchbroom:landed':{'minecraft:physics':{'has_gravity':True,'has_collision':True,'push_towards_closest_space':True}},
 'witchbroom:flying':{'minecraft:physics':{'has_gravity':False,'has_collision':True,'push_towards_closest_space':True}},
 'witchbroom:packed':{'minecraft:instant_despawn':{}}
},'events':{
 'witchbroom:mount':{'remove':{'component_groups':['witchbroom:landed']},'add':{'component_groups':['witchbroom:flying']},'set_property':{'witchbroom:occupied':True}},
 'witchbroom:land':{'add':{'component_groups':['witchbroom:landed']},'remove':{'component_groups':['witchbroom:flying']},'set_property':{'witchbroom:occupied':False},'stop_movement':{}},
 'witchbroom:pack':{'add':{'component_groups':['witchbroom:packed']}},
 'witchbroom:reconcile':{'sequence':[
  {'filters':{'all_of':[{'test':'bool_property','domain':'witchbroom:occupied','value':True},{'test':'rider_count','operator':'equals','value':0}]},'trigger':'witchbroom:land'},
  {'filters':{'all_of':[{'test':'bool_property','domain':'witchbroom:occupied','value':False},{'test':'rider_count','operator':'>','value':0}]},'trigger':'witchbroom:mount'}
 ]}
}}}
save('BP/entities/broom.json',entity)
save('BP/items/broom.json',{'format_version':'1.26.50','minecraft:item':{'description':{'identifier':'witchbroom:broom','menu_category':{'category':'equipment'}},'components':{'minecraft:display_name':{'value':'item.witchbroom:broom.name'},'minecraft:icon':{'textures':{'default':'witchbroom_broom'}},'minecraft:max_stack_size':1,'minecraft:hand_equipped':True,'minecraft:entity_placer':{'entity':'witchbroom:broom','use_on':[],'dispense_on':[]}}}})
save('BP/recipes/broom.json',{'format_version':'1.20.10','minecraft:recipe_shaped':{'description':{'identifier':'witchbroom:broom'},'tags':['crafting_table'],'pattern':['  S',' AS','WWW'],'key':{'S':{'item':'minecraft:stick'},'A':{'item':'minecraft:amethyst_shard'},'W':{'item':'minecraft:wheat'}},'unlock':[{'item':'minecraft:amethyst_shard'}],'result':{'item':'witchbroom:broom','count':1}}})
save('BP/loot_tables/entities/broom.json',{'pools':[{'rolls':1,'entries':[{'type':'item','name':'witchbroom:broom','weight':1}]}]})
save('RP/entity/broom.entity.json',{'format_version':'1.10.0','minecraft:client_entity':{'description':{'identifier':'witchbroom:broom','materials':{'default':'entity_alphatest'},'textures':{'default':'textures/entity/broom'},'geometry':{'default':'geometry.witchbroom.broom'},'animations':{'hover':'animation.witchbroom.hover'},'scripts':{'animate':['hover']},'render_controllers':['controller.render.witchbroom']}}})
save('RP/render_controllers/broom.render_controllers.json',{'format_version':'1.8.0','render_controllers':{'controller.render.witchbroom':{'geometry':'Geometry.default','materials':[{'*':'Material.default'}],'textures':['Texture.default']}}})
save('RP/animations/broom.animation.json',{'format_version':'1.8.0','animations':{'animation.witchbroom.hover':{'loop':True,'bones':{'broom':{'position':[0,"query.property('witchbroom:occupied') ? math.sin(query.life_time * 140) * 0.3 : 0",0],'rotation':["query.property('witchbroom:occupied') ? math.sin(query.life_time * 90) * 1.2 : 0",0,0]}}}}})
save('RP/textures/item_texture.json',{'resource_pack_name':'moonweave_broom','texture_name':'atlas.items','texture_data':{'witchbroom_broom':{'textures':'textures/items/broom'}}})
save('RP/particles/spark.json',{'format_version':'1.10.0','particle_effect':{'description':{'identifier':'witchbroom:spark','basic_render_parameters':{'material':'particles_alpha','texture':'textures/particle/spark'}},'components':{
 'minecraft:emitter_rate_instant':{'num_particles':3},'minecraft:emitter_lifetime_once':{'active_time':0.05},
 'minecraft:emitter_shape_sphere':{'radius':0.12,'direction':'outwards'},
 'minecraft:particle_initial_speed':0.05,'minecraft:particle_lifetime_expression':{'max_lifetime':0.7},
 'minecraft:particle_motion_dynamic':{'linear_acceleration':[0,0.12,0],'linear_drag_coefficient':1},
 'minecraft:particle_appearance_billboard':{'size':[0.045,0.045],'facing_camera_mode':'lookat_xyz','uv':{'texture_width':8,'texture_height':8,'uv':[0,0],'uv_size':[8,8]}},
 'minecraft:particle_appearance_tinting':{'color':[0.6,0.8,1.0,'1 - variable.particle_age / variable.particle_lifetime']}
}}})
for lang,txt in {
 'ja_JP':'''item.witchbroom:broom.name=月あかりのほうき
entity.witchbroom:broom.name=月あかりのほうき
action.interact.witchbroom.ride=ほうきに乗る
action.interact.witchbroom.pack=ほうきをしまう
witchbroom.controls=§b月あかりのほうき §f｜移動＋視線で飛行・ジャンプで上昇・しゃがむで降りる
witchbroom.landing=§dふんわり着地中 §f｜安全な地面へ
''',
 'en_US':'''item.witchbroom:broom.name=Moonweave Broom
entity.witchbroom:broom.name=Moonweave Broom
action.interact.witchbroom.ride=Ride broom
action.interact.witchbroom.pack=Pack broom
witchbroom.controls=§bMoonweave Broom §f| Move + look to fly | Jump: rise | Sneak: dismount
witchbroom.landing=§dSoft landing §f| Steer toward safe ground
'''}.items():
 with (ROOT/'RP/texts'/f'{lang}.lang').open('a') as f:f.write(txt)
print('Built manifests, entity, item, crafting, loot, client, particle, and localization data')
