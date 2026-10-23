const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root,'site/scenarios.js'),'utf8');
const rows = JSON.parse(fs.readFileSync(path.join(root,'site/defensive-preview.json'),'utf8'));
class Element {
  constructor() { this.value=''; this.textContent=''; this.children=[]; this.events={}; this.disabled=true; }
  addEventListener(name,fn) { this.events[name]=fn; }
  replaceChildren() { this.children=[]; }
  append(row) { this.children.push(row); }
}
async function check(data,ok=true) {
  const elements=Object.fromEntries(['scenario-task','scenario-status','scenario-input','scenario-answer'].map(id=>[id,new Element()]));
  vm.runInNewContext(source,{document:{getElementById:id=>elements[id],createElement:()=>new Element()},fetch:async()=>({ok,json:async()=>data})});
  await new Promise(resolve=>setImmediate(resolve));
  const select=elements['scenario-task'];
  if (!ok || !data.length || !data[0].task) {
    assert(select.disabled); assert.match(elements['scenario-status'].textContent,/could not load/); return;
  }
  assert.equal(select.children.length,rows.length); assert(!select.disabled);
  assert.equal(elements['scenario-input'].textContent,rows[0].messages[1].content);
  select.value=rows.at(-1).task; select.events.change();
  assert.equal(elements['scenario-input'].textContent,rows.at(-1).messages[1].content);
  assert.deepEqual(JSON.parse(elements['scenario-answer'].textContent),JSON.parse(rows.at(-1).messages[2].content));
}
(async()=>{await check(rows);await check([],true);await check([{}],true);await check(rows,false);console.log('Scenario selection, source/license status, responses, empty, invalid and fetch failure passed.');})().catch(error=>{console.error(error);process.exitCode=1;});
