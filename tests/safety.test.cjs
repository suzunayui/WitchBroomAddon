const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../BP/scripts/main.js'), 'utf8').replace(/^import .*?;\s*/m, '');
const TAG='witchbroom:soft_landing';
let assertions = 0;
function check(ok, message) { assert.ok(ok, message); assertions++; }
function player(id='alice') {
 return {id,isValid:true,isOnGround:false,isSwimming:false,tags:new Set(),effect:undefined,adds:0,hints:[],mount:undefined,
 hasTag(t){return this.tags.has(t)},addTag(t){this.tags.add(t)},removeTag(t){this.tags.delete(t)},
 getEffect(){return this.effect},addEffect(type,duration,options){this.effect={duration,amplifier:options.amplifier};this.adds++},
 getComponent(){return this.mount?{entityRidingOn:this.mount}:undefined},
 onScreenDisplay:{setActionBar(h){}},};
}
function broom(){ return {typeId:'witchbroom:broom',isValid:true,location:{x:0,y:64,z:0},getRotation(){return {x:0,y:0}},dimension:{spawnParticle(){}}}; }
function runtime(players) {
 const callbacks=[],spawn=[],warnings=[];
 const system={currentTick:0,runInterval(fn,n){check(n===1,'one tick interval');callbacks.push(fn)}};
 const world={getAllPlayers(){return players},afterEvents:{playerSpawn:{subscribe(fn){spawn.push(fn)}}}};
 vm.runInNewContext(source,{system,world,EntityComponentTypes:{Riding:'minecraft:riding'},console:{warn(m){warnings.push(m)}},Map,Set,Math,String});
 check(callbacks.length===1,'exactly one shared interval');
 return {players,spawn,warnings,tick(n=1){for(let i=0;i<n;i++){system.currentTick++;for(const p of players)if(p.effect&&p.effect.duration>0){p.effect.duration--;if(p.effect.duration===0)p.effect=undefined;}callbacks[0]();}}};
}
{
 const p=player();p.mount=broom();const r=runtime([p]);r.tick();
 check(p.tags.has(TAG),'mount persists safety tag');check(p.effect.duration===60,'mount protection immediate');
 p.mount=undefined;r.tick(1200);check(p.tags.has(TAG),'high altitude protection does not time out');check(p.effect.duration>=30,'effect continuously refreshed');
 p.isOnGround=true;r.tick(5);check(!p.tags.has(TAG),'guard cleared after stable landing');
 const adds=p.adds;r.tick(70);check(!p.effect,'last short effect expires');check(p.adds===adds,'no effect added after landing');
}
{
 const p=player();p.tags.add(TAG);const r=runtime([p]);r.tick();check(p.effect?.duration===60,'reload in air immediately restores protection');
 p.isOnGround=true;r.tick(5);check(p.tags.has(TAG),'spawn ground flag grace prevents immediate false landing');r.tick(30);check(!p.tags.has(TAG),'reload guard eventually clears on ground');
}
for(const effect of [{duration:1000,amplifier:0},{duration:1000,amplifier:2},{duration:-1,amplifier:0}]){
 const p=player();p.mount=broom();p.effect={...effect};const r=runtime([p]);r.tick();check(p.adds===0,'existing longer/stronger/infinite effect preserved');
 p.mount=undefined;p.isOnGround=true;r.tick(30);check(p.effect?.amplifier===effect.amplifier,'existing effect never removed');
}
{
 const p=player();p.mount=broom();const r=runtime([p]);r.tick();r.spawn[0]({player:p,initialSpawn:false});check(!p.tags.has(TAG),'death respawn clears old landing tag');
}
{
 const p=player();p.mount=broom();const q=player('bob');q.mount=broom();const r=runtime([p,q]);r.tick();
 check(p.tags.has(TAG)&&q.tags.has(TAG),'multiple riders protected independently');
 r.players.splice(0,1);r.tick(100);check(q.effect?.duration>=30,'disconnect does not stop remaining riders');
}
{
 const p=player();p.mount=broom();p.getComponent=()=>{throw Error('removed entity')};const q=player('bob');q.mount=broom();const r=runtime([p,q]);r.tick(100);
 check(q.tags.has(TAG),'invalid entity isolated per player');check(r.warnings.length===1,'diagnostic rate limited');
}
{
 const p=player();p.mount=broom();p.mount.dimension.spawnParticle=()=>{throw Error('unloaded chunk')};const r=runtime([p]);r.tick(100);check(p.effect?.duration>=30,'cosmetic failure never prevents safety');
}
{
 const p=player();p.mount={typeId:'minecraft:pig'};const r=runtime([p]);r.tick();check(!p.tags.has(TAG)&&p.adds===0,'unrelated mounts untouched');
}
console.log(`PASS: ${assertions} safety assertions (mocked stable API; not Minecraft runtime)`);
