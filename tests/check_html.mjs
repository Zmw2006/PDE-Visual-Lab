// 用最小 DOM 替身执行真正的单文件页面脚本，不需要安装浏览器或 npm 包。
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

const html = readFileSync(new URL('../index.html', import.meta.url), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)?.[1];
assert.ok(script, 'index.html 必须包含可离线执行的脚本');
assert.doesNotMatch(html, /<script[^>]+src=|<link[^>]+href=https?:/i);

class Element {
  constructor() {
    this.children = [];
    this.attributes = {};
    this.listeners = {};
    this.dataset = {};
    this.hidden = false;
    this.value = '0';
    this.classList = { toggle: () => {} };
  }
  setAttribute(key, value) { this.attributes[key] = value; }
  removeAttribute(key) { delete this.attributes[key]; }
  appendChild(child) { this.children.push(child); }
  replaceChildren(...children) { this.children = children; }
  addEventListener(name, handler) { this.listeners[name] = handler; }
  click() { this.listeners.click?.(); }
  input() { this.listeners.input?.(); }
}

const ids = new Map();
const get = id => {
  if (!ids.has(id)) ids.set(id, new Element());
  return ids.get(id);
};
const menu = ['transport', 'burgers', 'heat', 'wave'].map(topic => {
  const button = new Element();
  button.dataset.topic = topic;
  return button;
});
const document = {
  getElementById: get,
  querySelectorAll: () => menu,
  createElementNS: () => new Element(),
  createElement: () => new Element(),
};
const context = vm.createContext({ document, Math, Number, Array, Object, String,
  RangeError, requestAnimationFrame: () => 1, cancelAnimationFrame: () => {} });
vm.runInContext(script, context, { filename: 'index.html' });

const approx = (actual, expected, tolerance = 1e-11) =>
  assert.ok(Math.abs(actual - expected) < tolerance, `${actual} ≠ ${expected}`);
const model = vm.runInContext('model', context);
for (const x of [-2, -0.3, 0, 1.4]) {
  approx(model.transport(x + 0.9, 0.6, 1.5), model.gaussian(x));
  approx(model.heat(x, 0, 0.3), Math.sin(x) + 0.5 * Math.sin(2*x));
  approx(model.wave(x, 0, 1.0), model.gaussian(x));
}
for (const time of [0, 0.5, 0.98]) {
  for (const foot of [-2, -0.4, 0, 0.8, 2.4]) {
    approx(model.burgersFoot(model.burgersX(foot, time), time), foot);
  }
}
assert.throws(() => model.burgersFoot(0, 1), RangeError);

for (const button of menu) {
  button.click();
  assert.ok(get('title').textContent, `${button.dataset.topic}: 标题为空`);
  assert.ok(get('chart').children.some(child => child.attributes.d), `${button.dataset.topic}: 无曲线`);
  assert.ok(get('result').textContent, `${button.dataset.topic}: 无结果说明`);
}
menu[1].click();
get('time').value = '.4';
get('time').input();
assert.match(get('result').textContent, /初始点 ξ/);
get('time').value = '1.2';
get('time').input();
assert.match(get('result').textContent, /不能读作单值/);
get('reset').click();
assert.equal(Number(get('time').value), 0.4);
console.log('离线页面：四个模块、解析式、反查、临界时刻及重置均通过');
