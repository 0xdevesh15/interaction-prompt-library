#!/usr/bin/env node
// interaction-prompt-library MCP server (stdio, no dependencies)
// Exposes the reverse-engineered interaction prompt library to AI tools.
const { SERVER, TOOLS, callTool } = require('./core');

const PROTOCOL = '2024-11-05';

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
