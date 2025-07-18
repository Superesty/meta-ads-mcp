# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Server
```bash
# Standard MCP server (stdio transport)
python -m meta_ads_mcp

# HTTP server for development/testing
python -m meta_ads_mcp --transport streamable-http --port 8080

# User-friendly startup (Windows compatible)
python start_server.py --http --port 8080
```

### Testing
```bash
# Run all tests (requires server running on localhost:8080)
python -m pytest tests/ -v

# Start test server first
python -m meta_ads_mcp --transport streamable-http --port 8080 &

# Run specific test
python -m pytest tests/test_http_transport.py -v

# Run duplication regression tests
python -m pytest tests/test_duplication_regression.py -v
```

### Development Installation
```bash
# Install in development mode
pip install -e .

# Install via uvx (production)
uvx meta-ads-mcp
```

## Authentication Setup

### Environment Variables
- `PIPEBOARD_API_TOKEN`: Primary authentication (recommended)
- `META_APP_ID` / `META_APP_SECRET`: Custom app authentication (fallback)
- `META_ACCESS_TOKEN`: Direct token (advanced use cases)
- `MCP_LOG_LEVEL`: Logging verbosity (DEBUG, INFO, WARNING, ERROR)

### Quick Authentication Test
```bash
# Test Pipeboard authentication
python test_meta_ads_auth.py

# Test with custom app
python test_meta_ads_auth.py --app-id YOUR_APP_ID
```

## Architecture Overview

This is a **Model Context Protocol (MCP) server** for Meta's Ads API with dual transport support:

### Core Components
- **`meta_ads_mcp/core/server.py`**: Main MCP server using FastMCP framework
- **Transport Layer**: Supports both `stdio` (MCP clients) and `streamable-http` (web/n8n)
- **Authentication**: Dual-provider system (Pipeboard SaaS + custom Meta OAuth)
- **API Layer**: `core/api.py` with unified Meta Graph API v22.0 integration

### Tool Module Pattern
Each API domain is a separate module in `meta_ads_mcp/core/`:
- `accounts.py` - Ad account management
- `campaigns.py` - Campaign operations  
- `adsets.py` - Ad set management
- `ads.py` - Individual ad operations
- `insights.py` - Performance analytics
- `duplication.py` - Campaign/ad set duplication

### Tool Registration Pattern
```python
@mcp_server.tool()
@meta_api_tool  # Handles auth + error handling
async def tool_name(access_token: str = None, param: str = None) -> str:
    # Tool implementation
    return json.dumps(result, indent=2)  # Always return JSON strings
```

### Authentication Flow
1. **Pipeboard (Primary)**: `PIPEBOARD_API_TOKEN` → automatic OAuth handling
2. **Custom Meta App (Fallback)**: `META_APP_ID`/`META_APP_SECRET` → local OAuth flow
3. **HTTP Headers**: `Authorization: Bearer`, `X-META-ACCESS-TOKEN`, `X-META-APP-ID`

### Error Handling
- Use `GraphAPIError` for Meta API errors
- Auto-invalidate tokens on auth failure codes (190, 102, 4)
- Return error objects as JSON strings for MCP compatibility
- Log with context using structured logger from `utils.py`

## Development Guidelines

### Adding New Tools
1. Create/edit module in `meta_ads_mcp/core/`
2. Import `mcp_server` from `.server`
3. Apply `@mcp_server.tool()` and `@meta_api_tool` decorators
4. Follow async signature with optional `access_token` parameter
5. Return JSON string (not dict) for MCP compatibility
6. Use `make_api_request()` from `api.py` for Meta API calls

### Meta API Integration
- Graph API v22.0 via `META_GRAPH_API_VERSION` constant
- Account IDs format: `act_XXXXXXXXX`
- Complex parameters (targeting, etc.) serialized to JSON strings for POST
- Image uploads return hashes for creative creation
- Use `from .utils import logger` for logging

### Code Conventions
- All tools must be async and return strings
- Tool naming: `mcp_meta_ads_*` prefix
- Optional `access_token` parameter pattern for all API tools
- Consistent error response format in JSON
- Windows compatibility (avoid Unicode in prints, use `[OK]`/`[ERROR]`)

### Testing Requirements
- Tests require running MCP server instance on localhost:8080
- Use fixtures from `conftest.py`
- Test both success and failure cases
- Regression tests for critical functionality (duplication)
- HTTP transport integration tests validate full request/response cycle

## Meta Ads API Reference

### Hierarchy Structure
Meta Ads API follows a strict hierarchy:
```
Campaign (objective, budget_optimization)
├── Ad Set (targeting, optimization_goal, billing_event)
    └── Ad (links creative to ad set)
        └── Ad Creative (content: images, videos, text)
```

### Key API Concepts
- **Objectives**: CONVERSIONS, LEAD_GENERATION, SALES, TRAFFIC, etc.
- **Targeting**: Complex JSON object with geo_locations, age_min/max, interests
- **Budget Types**: daily_budget vs lifetime_budget (strings in cents)
- **Optimization Goals**: LINK_CLICKS, IMPRESSIONS, CONVERSIONS, etc.
- **Bid Strategies**: LOWEST_COST_WITHOUT_CAP, COST_CAP, BID_CAP

### Special Considerations
- **CBO (Campaign Budget Optimization)**: Set `budget_optimization: true` at campaign level
- **Special Ad Categories**: Required for housing, employment, credit ads
- **Dynamic Creative**: Use `asset_feed_spec` for multiple creative variations
- **Video Uploads**: Async process requiring upload monitoring before creative creation
- **Lead Forms**: Separate form creation for LEAD_GENERATION campaigns

## Key Files
- `start_server.py`: User-friendly server startup with dependency checks
- `meta_ads_auth.sh`: Bash script for Pipeboard authentication setup
- `core/http_auth_integration.py`: HTTP authentication handler
- `core/callback_server.py`: OAuth callback server for custom Meta apps
- `core/resources.py`: MCP resource interface (ad images)
- `meta_api_docu/meta_api.md`: Comprehensive Spanish Meta API documentation