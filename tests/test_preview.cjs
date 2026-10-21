/* Run without a browser or dependencies: node tests/test_preview.cjs */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'site/explorer.js'), 'utf8');
const preview = JSON.parse(fs.readFileSync(path.join(root, 'site/preview.json'), 'utf8'));
class Element {
  constructor() { this.value = ''; this.children = []; this.listeners = {}; this.disabled = false; this.textContent = ''; }
  append(child) { this.children.push(child); }
  replaceChildren() { this.children = []; }
  addEventListener(type, callback) { this.listeners[type] = callback; }
  trigger(type) { this.listeners[type]({ preventDefault() {} }); }
}
async function scenario(fail) {
  const ids = ['query','corpus','sensor','filters','records','status','page','previous','next'];
  const elements = Object.fromEntries(ids.map(id => [id, new Element()]));
  vm.runInNewContext(source, {
    document: {getElementById: id => elements[id], createElement: () => new Element()},
    fetch: async () => ({ok: !fail, json: async () => preview}),
    setTimeout: callback => callback()
  });
  await new Promise(resolve => setImmediate(resolve));
  if (fail) {
    assert.match(elements.status.textContent, /could not load/);
    return;
  }
  assert.equal(elements.records.children.length, 12);
  elements.next.trigger('click');
  assert.match(elements.page.textContent, /Page 2/);
  elements.corpus.value = 'cloud-honeynet-2025';
  elements.sensor.value = 'Cowrie';
  elements.filters.trigger('change');
  assert.equal(elements.records.children.length, 12);
  assert(elements.records.children.every(row => row.children[0].textContent.startsWith('cloud-')));
  assert(elements.records.children.every(row => row.children[2].textContent === 'Cowrie'));
  elements.query.value = 'no-such-record'; elements.filters.trigger('input');
  assert.equal(elements.records.children.length, 0);
  assert.match(elements.status.textContent, /No preview records match/);
  assert(elements.next.disabled && elements.previous.disabled);
  elements.query.value = ''; elements.corpus.value = ''; elements.sensor.value = '';
  elements.filters.trigger('reset');
  assert.equal(elements.records.children.length, 12);
  assert.match(elements.page.textContent, /Page 1/);
}
(async () => { await scenario(false); await scenario(true); console.log('Preview search, filters, pagination, reset, empty and fetch-failure states passed.'); })().catch(error => { console.error(error); process.exitCode = 1; });
