# Interaction Prompt Library

Frame-by-frame teardowns of the best interactions on the web, reverse-engineered into
build-ready prompts - plus an MCP server so AI tools can query the library directly.

## Sources
- **inspora.design** (source #1): 80 posts, Sep 2026 snapshot. All extracted, all media
  torn down frame-by-frame.
- **60fps.design** (source #2, planned): same treatment, folded into the same schema
  (every record has a `source` field; ids are namespaced `<source>:<slug>`).

## Contents
- `dist/` - static website (no build step, no dependencies):
  - `index.html` - searchable/filterable grid of all interactions
  - `i/<slug>.html` - one page per interaction: embedded media, frame-by-frame montage
    and phases, mechanics (trigger/elements/properties/timing/easing/loop), and the
    full build prompt with a copy button
  - `interactions.json` - the full dataset (also what the MCP server reads)
  - `frames/` - 3x3 nine-frame montages per media item
- `mcp/server.js` - MCP server (Node 18+, stdio, zero dependencies)
- `build.py` - regenerates `dist/` from `interactions.json`

## Run the site
Open `dist/index.html` directly, or serve it:
  python3 -m http.server -d dist 8000

## Run the MCP server
  node mcp/server.js
Claude Desktop / Cursor config:
  {
    "mcpServers": {
      "interaction-prompt-library": {
        "command": "node",
        "args": ["/path/to/insp-site/mcp/server.js"]
      }
    }
  }
Set IPL_DATA=/path/to/interactions.json to override the dataset location.

### MCP tools
- `list_interactions(category?, source?)` - list ids/titles/categories
- `search_interactions(query)` - ranked full-text search over titles, summaries,
  mechanics, and prompts
- `get_interaction_prompt(id)` - full teardown record: summary, frame-by-frame phases,
  mechanics, and the build prompt (accepts "inspora:1-12" or bare slug "1-12")

## Record schema (multi-source)
id, source, slug, title, category, desc, author, authorUrl, published, originalUrl,
pageUrl, media[{type,src,poster,meta{duration,w,h,fps},montage}], summary,
frames[{phase,desc}], mechanics{trigger,elements,properties,timing,easing,loop}, prompt
