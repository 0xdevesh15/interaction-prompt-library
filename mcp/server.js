#!/usr/bin/env node
// interaction-prompt-library MCP server (stdio, no dependencies)
// Exposes the reverse-engineered interaction prompt library to AI tools.
const fs = require('fs');
const path = require('path');

const DATA_PATH = process.env.IPL_DATA || path.join(__dirname, '..', 'dist', 'interactions.json');
const records = JSON.parse(fs.readFileSync(DATA_PATH, 'utf8'));

const SERVER = { name: 'interaction-prompt-library', version: '1.0.0' };
const PROTOCOL = '2024-11-05';

const TOOLS = [
  {
    name: 'list_interactions',
    description: 'List every interaction teardown in the library (id, title, category, author, source). Optionally filter by category or source.',
    inputSchema: {
      type: 'object',
      properties: {
        category: { type: 'string', description: 'Filter by category, e.g. Motion, Product, Web, Branding, Illustration, 3D' },
        source: { type: 'string', description: 'Filter by source site, e.g. inspora' }
      }
    }
  },
  {
    name: 'search_interactions',
    description: 'Full-text search over interaction titles, summaries, mechanics, and build prompts. Returns ranked matches with summaries.',
    inputSchema: {
      type: 'object',
      properties: { query: { type: 'string', description: 'What you are looking for, e.g. "glass refraction", "toggle", "scroll stack"' } },
      required: ['query']
    }
  },
  {
    name: 'get_interaction_prompt',
    description: 'Get the full teardown for one interaction by id or slug: summary, frame-by-frame phases, mechanics (trigger/elements/properties/timing/easing/loop), and the detailed build prompt.',
    inputSchema: {
      type: 'object',
      properties: { id: { type: 'string', description: 'Interaction id (e.g. "inspora:1-12") or slug (e.g. "1-12", "multi-action-button")' } },
      required: ['id']
    }
  }
];

function findRecord(id) {
  return records.find(r => r.id === id || r.slug === id) || null;
}

function score(r, terms) {
  const hay = [r.title, r.desc, r.category, r.summary, r.prompt,
    ...(r.frames || []).map(f => f.desc),
    ...Object.values(r.mechanics || {}).flat()
  ].join(' ').toLowerCase();
  let s = 0;
  for (const t of terms) {
    const matches = hay.split(t).length - 1;
    if (matches) s += matches * (r.title.toLowerCase().includes(t) ? 5 : 1);
  }
  return s;
}

function callTool(name, args) {
  if (name === 'list_interactions') {
    let out = records;
    if (args.category) out = out.filter(r => (r.category || '').toLowerCase() === args.category.toLowerCase());
    if (args.source) out = out.filter(r => r.source === args.source);
    return {
      count: out.length,
      interactions: out.map(r => ({ id: r.id, title: r.title, category: r.category, author: r.author, source: r.source, pageUrl: r.pageUrl }))
    };
  }
  if (name === 'search_interactions') {
    const terms = (args.query || '').toLowerCase().split(/\s+/).filter(Boolean);
    const ranked = records.map(r => ({ r, s: score(r, terms) })).filter(x => x.s > 0).sort((a, b) => b.s - a.s).slice(0, 10);
    return {
      count: ranked.length,
      results: ranked.map(({ r, s }) => ({ id: r.id, title: r.title, category: r.category, summary: r.summary, relevance: s }))
    };
  }
  if (name === 'get_interaction_prompt') {
    const r = findRecord(args.id || '');
    if (!r) return { error: `No interaction found for id "${args.id}". Use list_interactions or search_interactions to find ids.` };
    return r;
  }
  return { error: `Unknown tool: ${name}` };
}

function respond(id, result, error) {
  const msg = { jsonrpc: '2.0', id };
  if (error) msg.error = error; else msg.result = result;
  process.stdout.write(JSON.stringify(msg) + '\n');
}

function handle(msg) {
  let req;
  try { req = JSON.parse(msg); } catch { return; }
  const { id, method, params } = req;
  if (method === 'initialize') {
    return respond(id, { protocolVersion: PROTOCOL, capabilities: { tools: {} }, serverInfo: SERVER });
  }
  if (method === 'notifications/initialized' || method === 'initialized') return;
  if (method === 'ping') return respond(id, {});
  if (method === 'tools/list') return respond(id, { tools: TOOLS });
  if (method === 'tools/call') {
    const out = callTool(params?.name, params?.arguments || {});
    return respond(id, { content: [{ type: 'text', text: JSON.stringify(out, null, 2) }] });
  }
  if (id !== undefined) return respond(id, null, { code: -32601, message: `Method not found: ${method}` });
}

let buf = '';
process.stdin.on('data', d => {
  buf += d;
  let i;
  while ((i = buf.indexOf('\n')) >= 0) {
    const line = buf.slice(0, i).trim();
    buf = buf.slice(i + 1);
    if (line) handle(line);
  }
});
