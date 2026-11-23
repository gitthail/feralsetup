// Script and archive checks only; this is not a visual browser test.
const fs=require('fs'),vm=require('vm'),path=require('path'),assert=require('assert');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'docs/Guide.html'),'utf8');
const script=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
assert.equal(script.length,1);
const ids=new Set([...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]));
for(const m of html.matchAll(/href="#([^"]+)"/g))assert(ids.has(m[1]),m[1]);
const nodes={};
for(const id of ids){const pre={textContent:''},button={disabled:false};nodes[id]={value:'',textContent:'',hidden:false,addEventListener(){},querySelector(s){return s==='pre'?pre:button}};}
Object.assign(nodes.cat,{value:'3'});Object.assign(nodes.bear,{value:'1'});Object.assign(nodes.aquatic,{value:'2'});Object.assign(nodes.travel,{value:'4'});Object.assign(nodes.bearSpell,{value:'Bear Form'});Object.assign(nodes.poison,{value:'Cure Poison'});
let archive;
const sandbox={TextEncoder,Uint8Array,Uint32Array,Blob,setTimeout(){},URL:{createObjectURL(blob){archive=blob;return 'blob:test'},revokeObjectURL(){}},document:{documentElement:{outerHTML:html.replace(/^<!doctype html>\s*/i,'')},getElementById(id){assert(nodes[id],id);return nodes[id]},createElement(){return {click(){}}}},navigator:{}};
vm.createContext(sandbox);vm.runInContext(script[0],sandbox);
assert(nodes['macro-status'].textContent.includes('32 macros'));
nodes.search.value='Faerie Fire';vm.runInContext('renderMacros()',sandbox);
const visible=Object.keys(nodes).filter(k=>/^macro-\d+$/.test(k)&&!nodes[k].hidden);assert.equal(visible.length,1);
assert(nodes[visible[0]].querySelector('pre').textContent.includes('/cast Faerie Fire'));
nodes.cat.value='2';nodes.search.value='Prowl';vm.runInContext('renderMacros()',sandbox);
assert(Object.keys(nodes).filter(k=>/^macro-\d+$/.test(k)).some(k=>nodes[k].querySelector('pre').textContent.includes('[form:2] Prowl')));
vm.runInContext('downloadBundle()',sandbox);
(async()=>{fs.writeFileSync(process.argv[2]||'/tmp/feral-guide-download.zip',Buffer.from(await archive.arrayBuffer()));console.log('PASS: guide scripts, anchors, search, form configuration, macro limits display and offline ZIP generation.');})();
