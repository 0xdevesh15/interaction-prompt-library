// Hosted interaction-prompt-library MCP endpoint: streamable HTTP, stateless.
// Uses the official MCP TypeScript SDK (@modelcontextprotocol/server + /node).
const { McpServer } = require('@modelcontextprotocol/server');
const { NodeStreamableHTTPServerTransport } = require('@modelcontextprotocol/node');
const { z } = require('zod');
const { SERVER, TOOLS, callTool } = require('../mcp/core');

function textResult(obj) {
  return { content: [{ type: 'text', text: JSON.stringify(obj, null, 2) }] };
}

function buildServer() {
  const server = new McpServer(SERVER);
  server.registerTool('list_interactions', {
    description: TOOLS[0].description,
    inputSchema: z.object({
      category: z.string().optional(),
      source: z.string().optional()
    })
  }, async (args) => textResult(callTool('list_interactions', args)));
  server.registerTool('search_interactions', {
    description: TOOLS[1].description,
    inputSchema: z.object({ query: z.string() })
  }, async ({ query }) => textResult(callTool('search_interactions', { query })));
  server.registerTool('get_interaction_prompt', {
    description: TOOLS[2].description,
    inputSchema: z.object({ id: z.string() })
  }, async ({ id }) => textResult(callTool('get_interaction_prompt', { id })));
  return server;
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.writeHead(405, { 'content-type': 'application/json', 'allow': 'POST' });
    res.end(JSON.stringify({
      error: 'Method not allowed. This is an MCP streamable-HTTP endpoint: POST JSON-RPC here. Setup: https://16ms.vercel.app/mcp/'
    }));
    return;
  }
  const server = buildServer();
  const transport = new NodeStreamableHTTPServerTransport({ sessionIdGenerator: undefined });
  try {
    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
  } catch (err) {
    if (!res.headersSent) {
      res.writeHead(500, { 'content-type': 'application/json' });
      res.end(JSON.stringify({ error: String(err && err.message || err) }));
    } else { res.end(); }
  }
};
