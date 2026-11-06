// Synthetic fixture only: never open or populate the private human judgment store.
const {readFileSync}=require('node:fs');
const vm=require('node:vm');
const assert=require('node:assert/strict');
const template=readFileSync('scripts/judgment_batch_template.html','utf8');
const packet={schema_version:2,evaluation_only:true,packet_sha256:'fixture',
  queries:[{data_uri:'fixture-query'}],candidates:[{data_uri:'fixture-candidate'}],
  trials:Array.from({length:99},(_,i)=>({trial_id:'t'+i,query:0,candidate:0,repeat:i>=90}))};
const script=template.match(/<script>([\s\S]*)<\/script>/)[1].replace('__PACKET_DATA__',JSON.stringify(packet));
const store=new Map(),sessions=new Map();
class Element{
  constructor(){this.children=[];this.attrs={};this.value=''}
  append(...nodes){this.children.push(...nodes)}
  replaceChildren(){this.children=[]}
  setAttribute(k,v){this.attrs[k]=v}
}
function load(session='first',now=1000000,failStorage=false){
  const elements=new Map();sessions.set('denim-judgments-fixture-session',session);
  const storage=map=>({getItem:k=>map.get(k)||null,setItem:(k,v)=>map.set(k,v)});
  const ctx=vm.createContext({console,crypto:{randomUUID:()=>session},Date:class extends Date{static now(){return now}},
    sessionStorage:storage(sessions),localStorage:failStorage?{getItem(){throw Error('denied')},setItem(){throw Error('denied')}}:storage(store),
    document:{getElementById:id=>{if(!elements.has(id))elements.set(id,new Element());return elements.get(id)},createElement:()=>new Element()},
    window:{scrollTo(){}},setTimeout(){},URL:{},Blob:class{}});
  vm.runInContext(script,ctx);
  return {ctx,elements,run:code=>vm.runInContext(code,ctx)};
}
let ui=load();
assert.equal(ui.elements.get('cards').children.length,10);
assert.equal(ui.run('repeatAllowed()'),false);
// Choose one real DOM button in the synthetic screen, then reload the saved state.
const firstCard=ui.elements.get('cards').children[0];
firstCard.children[2].children[1].children[2].onclick();
ui=load();assert.equal(ui.run("state.answers.t0.scores.silhouette.grade"),2);
assert.equal(ui.elements.get('finish').disabled,true);
// Synthetic completion permits closing session1, never immediate repeats.
ui.run("primary.forEach(t=>state.answers[t.trial_id]={scores:{silhouette:{grade:2},surface:{grade:1}}});render();$('finish').onclick()");
assert.equal(ui.elements.get('cards').children.length,0);
ui=load('second',1000000+30*60*1000-1);
assert.equal(ui.run('repeatAllowed()'),false);
ui=load('first',1000000+30*60*1000);
assert.equal(ui.run('repeatAllowed()'),false);
ui=load('second',1000000+30*60*1000);
assert.equal(ui.run('repeatAllowed()'),true);
assert.equal(ui.elements.get('cards').children.length,9);
assert.equal(ui.run('Object.keys(state.answers).length'),90);
ui=load('third',1000000,true);
assert.equal(ui.run('storageOK'),false);
assert.equal(ui.elements.get('cards').children[0].children[2].children[1].children[0].disabled,true);
console.log('PASS: ten cards, autosave/reload, complete-first-stage gate, time AND new-session gate, nine repeats, storage failure lock');
