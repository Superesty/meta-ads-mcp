# Meta Ads MCP Copilot Instructions

## Architecture Overview

This is a **Model Context Protocol (MCP) server** that enables AI models to interact with Meta's Ads API. The project follows a modular architecture:

- **`meta_ads_mcp/core/`** - Core MCP server implementation using FastMCP
- **`meta_ads_mcp/core/server.py`** - Main MCP server with tool registration and HTTP handling
- **Authentication layers** - Dual auth: Pipeboard (SaaS) and direct Meta OAuth
- **Tool modules** - Each API domain (campaigns, ads, adsets, etc.) in separate files

## Key Patterns

### Tool Registration Pattern
Tools are registered using FastMCP decorators:
```python
@mcp_server.tool()
@meta_api_tool  # Custom auth decorator
async def get_campaigns(access_token: str = None, account_id: str = None) -> str:
```

### Authentication Strategy
- **Primary**: Pipeboard token-based auth via `PIPEBOARD_API_TOKEN` env var
- **Fallback**: Direct Meta OAuth with `META_APP_ID`/`META_APP_SECRET`
- All auth logic centralized in `auth.py` and `pipeboard_auth.py`

### API Response Format
All tools return JSON strings (not dicts) for MCP compatibility:
```python
return json.dumps(data, indent=2)
```

### Error Handling
Use `GraphAPIError` for Meta API errors with automatic token invalidation on auth failures (codes 190, 102, 4).

## Development Workflows

### Running/Testing
```bash
# Development server
python -m meta_ads_mcp

# HTTP server for development/testing
python -m meta_ads_mcp --transport streamable-http --port 8080

# Quick start script (Windows-friendly)
python start_server.py --http --port 8080

# Authentication testing
python test_meta_ads_auth.py --app-id YOUR_APP_ID

# Run tests (requires test server)
pytest tests/

# Install in dev mode
pip install -e .
```

### Adding New Tools
1. Create/edit module in `meta_ads_mcp/core/`
2. Import `mcp_server` from `.server`
3. Apply `@mcp_server.tool()` and `@meta_api_tool` decorators
4. Follow async signature pattern with optional `access_token`
5. Return JSON string, not dict

### Authentication Testing
- Set `PIPEBOARD_API_TOKEN` for Pipeboard auth
- Set `META_APP_ID`/`META_APP_SECRET` for direct Meta auth
- Use `get_current_access_token()` to get active token
- Auth state persists in platform-specific cache directories

### Windows Compatibility
- Avoid Unicode emoji characters in print statements (use `[OK]`, `[ERROR]` instead)
- Use `python start_server.py` for user-friendly server startup
- Test scripts provided: `test_meta_ads_auth.py` and `start_server.py`

## Project-Specific Conventions

### File Organization
- One tool module per API domain (campaigns.py, ads.py, adsets.py)
- `api.py` contains base API client with `make_api_request()`
- `utils.py` has logging setup - use `from .utils import logger`
- Authentication split: `auth.py` (Meta OAuth) + `pipeboard_auth.py` (SaaS)

### Meta API Integration
- Uses Graph API v22.0 via `META_GRAPH_API_VERSION`
- Account IDs formatted as `act_XXXXXXXXX`
- Complex parameters (targeting, etc.) serialized to JSON strings for POST requests
- Image uploads return hashes for creative creation

### MCP-Specific Requirements
- Tools must be async and return strings (not dicts)
- Use consistent tool naming: `mcp_meta_ads_*`
- Optional `access_token` parameter pattern for all API tools
- Resource URIs: `meta-ads://resources` and `meta-ads://images/{id}`

### Error Handling Patterns
- Log errors with context using structured logger
- Return error objects in JSON format for client display
- Auto-invalidate tokens on specific Meta API error codes
- Graceful degradation when auth fails

## Integration Points

### External Dependencies
- **httpx** for async HTTP requests to Meta Graph API
- **FastMCP** for MCP server framework  
- **Pillow** for image processing/validation
- **requests** for Pipeboard API sync calls

### Data Flow
1. Client sends MCP tool request
2. `StreamableHTTPHandler` extracts auth from headers
3. `@meta_api_tool` decorator handles token resolution
4. `make_api_request()` calls Meta Graph API
5. Response serialized to JSON string for client

### Testing Strategy
- `conftest.py` provides server fixtures
- Tests require running MCP server instance
- Regression tests in `test_duplication_regression.py`
- HTTP transport tests for Streamable HTTP mode
