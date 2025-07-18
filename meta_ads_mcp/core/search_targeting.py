"""Search and Targeting functionality for Meta Ads API."""

import json
from typing import Optional, List, Dict, Any, Union
from .api import meta_api_tool, make_api_request
from .accounts import get_ad_accounts
from .server import mcp_server


@mcp_server.tool()
@meta_api_tool
async def search_postal_codes(
    access_token: str = None,
    country_code: str = None,
    search_term: str = None,
    limit: int = 100,
    location_types: List[str] = None
) -> str:
    """
    Search for postal codes/ZIP codes for geographic targeting.
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        country_code: Country code (e.g., "US", "CA", "GB")
        search_term: Search term for postal codes or city names
        limit: Maximum number of results to return
        location_types: Types of locations to search (e.g., ["zip", "city", "region"])
    
    Returns:
        JSON response with postal code search results
    """
    if not country_code:
        return json.dumps({"error": "Country code is required for postal code search"}, indent=2)
    
    if not search_term:
        return json.dumps({"error": "Search term is required for postal code search"}, indent=2)
    
    endpoint = "search"
    params = {
        "type": "adgeolocation",
        "q": search_term,
        "country_code": country_code,
        "limit": limit
    }
    
    if location_types:
        params["location_types"] = json.dumps(location_types)
    
    try:
        data = await make_api_request(endpoint, access_token, params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({
            "error": "Failed to search postal codes",
            "details": str(e),
            "params_sent": params
        }, indent=2)


@mcp_server.tool()
@meta_api_tool
async def search_interests(
    access_token: str = None,
    search_term: str = None,
    limit: int = 100,
    locale: str = "en_US"
) -> str:
    """
    Search for interests for demographic targeting.
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        search_term: Search term for interests
        limit: Maximum number of results to return
        locale: Language locale for results
    
    Returns:
        JSON response with interest search results
    """
    if not search_term:
        return json.dumps({"error": "Search term is required for interest search"}, indent=2)
    
    endpoint = "search"
    params = {
        "type": "adinterest",
        "q": search_term,
        "limit": limit,
        "locale": locale
    }
    
    try:
        data = await make_api_request(endpoint, access_token, params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({
            "error": "Failed to search interests",
            "details": str(e),
            "params_sent": params
        }, indent=2)


@mcp_server.tool()
@meta_api_tool
async def search_behaviors(
    access_token: str = None,
    search_term: str = None,
    limit: int = 100,
    locale: str = "en_US"
) -> str:
    """
    Search for behaviors for demographic targeting.
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        search_term: Search term for behaviors
        limit: Maximum number of results to return
        locale: Language locale for results
    
    Returns:
        JSON response with behavior search results
    """
    if not search_term:
        return json.dumps({"error": "Search term is required for behavior search"}, indent=2)
    
    endpoint = "search"
    params = {
        "type": "adbehavior",
        "q": search_term,
        "limit": limit,
        "locale": locale
    }
    
    try:
        data = await make_api_request(endpoint, access_token, params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({
            "error": "Failed to search behaviors",
            "details": str(e),
            "params_sent": params
        }, indent=2)


@mcp_server.tool()
@meta_api_tool
async def search_demographics(
    access_token: str = None,
    search_term: str = None,
    limit: int = 100,
    locale: str = "en_US"
) -> str:
    """
    Search for demographics for targeting.
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        search_term: Search term for demographics
        limit: Maximum number of results to return
        locale: Language locale for results
    
    Returns:
        JSON response with demographic search results
    """
    if not search_term:
        return json.dumps({"error": "Search term is required for demographic search"}, indent=2)
    
    endpoint = "search"
    params = {
        "type": "adTargetingCategory",
        "q": search_term,
        "limit": limit,
        "locale": locale,
        "class": "demographics"
    }
    
    try:
        data = await make_api_request(endpoint, access_token, params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({
            "error": "Failed to search demographics",
            "details": str(e),
            "params_sent": params
        }, indent=2)


@mcp_server.tool()
@meta_api_tool
async def get_audience_size_estimate(
    access_token: str = None,
    account_id: str = None,
    targeting: Dict[str, Any] = None,
    optimization_goal: str = "LINK_CLICKS",
    daily_budget: int = 1000
) -> str:
    """
    Get audience size estimate for targeting specifications.
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        account_id: Meta Ads account ID (format: act_XXXXXXXXX)
        targeting: Targeting specifications to estimate
        optimization_goal: Optimization goal for the estimate
        daily_budget: Daily budget for the estimate (in cents)
    
    Returns:
        JSON response with audience size estimate
    """
    if not account_id:
        # Try to get the first account if not provided
        accounts_json = await get_ad_accounts(access_token=access_token, user_id="me", limit=1)
        accounts_data = json.loads(accounts_json)
        
        if "data" in accounts_data and accounts_data["data"]:
            account_id = accounts_data["data"][0]["id"]
        else:
            return json.dumps({"error": "No account ID specified and no accounts found for user"}, indent=2)
    
    if not targeting:
        return json.dumps({"error": "Targeting specifications are required for audience estimation"}, indent=2)
    
    endpoint = f"{account_id}/delivery_estimate"
    params = {
        "targeting_spec": json.dumps(targeting),
        "optimization_goal": optimization_goal,
        "daily_budget": str(daily_budget)
    }
    
    try:
        data = await make_api_request(endpoint, access_token, params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({
            "error": "Failed to get audience size estimate",
            "details": str(e),
            "params_sent": params
        }, indent=2)


@mcp_server.tool()
@meta_api_tool
async def get_targeting_browse_categories(
    access_token: str = None,
    type: str = "interests",
    parent_id: str = None,
    limit: int = 100
) -> str:
    """
    Browse targeting categories (interests, behaviors, demographics).
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        type: Type of categories to browse (interests, behaviors, demographics)
        parent_id: Parent category ID to browse subcategories
        limit: Maximum number of results to return
    
    Returns:
        JSON response with targeting categories
    """
    endpoint = "targetingbrowse"
    params = {
        "limit": limit
    }
    
    if type == "interests":
        params["type"] = "adinterest"
    elif type == "behaviors":
        params["type"] = "adbehavior"
    elif type == "demographics":
        params["type"] = "adTargetingCategory"
        params["class"] = "demographics"
    else:
        return json.dumps({"error": "Invalid type. Use 'interests', 'behaviors', or 'demographics'"}, indent=2)
    
    if parent_id:
        params["parent_id"] = parent_id
    
    try:
        data = await make_api_request(endpoint, access_token, params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({
            "error": "Failed to browse targeting categories",
            "details": str(e),
            "params_sent": params
        }, indent=2)


@mcp_server.tool()
@meta_api_tool
async def get_targeting_suggestions(
    access_token: str = None,
    account_id: str = None,
    targeting: Dict[str, Any] = None,
    limit: int = 100
) -> str:
    """
    Get targeting suggestions based on current targeting.
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        account_id: Meta Ads account ID (format: act_XXXXXXXXX)
        targeting: Current targeting specifications
        limit: Maximum number of suggestions to return
    
    Returns:
        JSON response with targeting suggestions
    """
    if not account_id:
        # Try to get the first account if not provided
        accounts_json = await get_ad_accounts(access_token=access_token, user_id="me", limit=1)
        accounts_data = json.loads(accounts_json)
        
        if "data" in accounts_data and accounts_data["data"]:
            account_id = accounts_data["data"][0]["id"]
        else:
            return json.dumps({"error": "No account ID specified and no accounts found for user"}, indent=2)
    
    if not targeting:
        return json.dumps({"error": "Targeting specifications are required for suggestions"}, indent=2)
    
    endpoint = f"{account_id}/targetingsearch"
    params = {
        "targeting_spec": json.dumps(targeting),
        "limit": limit
    }
    
    try:
        data = await make_api_request(endpoint, access_token, params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({
            "error": "Failed to get targeting suggestions",
            "details": str(e),
            "params_sent": params
        }, indent=2)


@mcp_server.tool()
@meta_api_tool
async def validate_targeting_spec(
    access_token: str = None,
    account_id: str = None,
    targeting: Dict[str, Any] = None,
    objective: str = "LINK_CLICKS"
) -> str:
    """
    Validate targeting specifications for compliance and effectiveness.
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        account_id: Meta Ads account ID (format: act_XXXXXXXXX)
        targeting: Targeting specifications to validate
        objective: Campaign objective for validation context
    
    Returns:
        JSON response with validation results
    """
    if not account_id:
        # Try to get the first account if not provided
        accounts_json = await get_ad_accounts(access_token=access_token, user_id="me", limit=1)
        accounts_data = json.loads(accounts_json)
        
        if "data" in accounts_data and accounts_data["data"]:
            account_id = accounts_data["data"][0]["id"]
        else:
            return json.dumps({"error": "No account ID specified and no accounts found for user"}, indent=2)
    
    if not targeting:
        return json.dumps({"error": "Targeting specifications are required for validation"}, indent=2)
    
    endpoint = f"{account_id}/targetingvalidation"
    params = {
        "targeting_spec": json.dumps(targeting),
        "objective": objective
    }
    
    try:
        data = await make_api_request(endpoint, access_token, params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({
            "error": "Failed to validate targeting specifications",
            "details": str(e),
            "params_sent": params
        }, indent=2)


@mcp_server.tool()
@meta_api_tool
async def get_country_list(
    access_token: str = None,
    locale: str = "en_US"
) -> str:
    """
    Get list of supported countries for targeting.
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        locale: Language locale for country names
    
    Returns:
        JSON response with supported countries
    """
    endpoint = "search"
    params = {
        "type": "adgeolocation",
        "location_types": json.dumps(["country"]),
        "q": "*",
        "limit": 500,
        "locale": locale
    }
    
    try:
        data = await make_api_request(endpoint, access_token, params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({
            "error": "Failed to get country list",
            "details": str(e),
            "params_sent": params
        }, indent=2)


@mcp_server.tool()
@meta_api_tool
async def search_cities(
    access_token: str = None,
    country_code: str = None,
    search_term: str = None,
    limit: int = 100,
    locale: str = "en_US"
) -> str:
    """
    Search for cities in a specific country for targeting.
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        country_code: Country code (e.g., "US", "CA", "GB")
        search_term: Search term for city names
        limit: Maximum number of results to return
        locale: Language locale for results
    
    Returns:
        JSON response with city search results
    """
    if not country_code:
        return json.dumps({"error": "Country code is required for city search"}, indent=2)
    
    if not search_term:
        return json.dumps({"error": "Search term is required for city search"}, indent=2)
    
    endpoint = "search"
    params = {
        "type": "adgeolocation",
        "q": search_term,
        "country_code": country_code,
        "location_types": json.dumps(["city"]),
        "limit": limit,
        "locale": locale
    }
    
    try:
        data = await make_api_request(endpoint, access_token, params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({
            "error": "Failed to search cities",
            "details": str(e),
            "params_sent": params
        }, indent=2)


@mcp_server.tool()
@meta_api_tool
async def get_language_list(
    access_token: str = None,
    locale: str = "en_US"
) -> str:
    """
    Get list of supported languages for targeting.
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        locale: Language locale for language names
    
    Returns:
        JSON response with supported languages
    """
    endpoint = "search"
    params = {
        "type": "adlocale",
        "q": "*",
        "limit": 200,
        "locale": locale
    }
    
    try:
        data = await make_api_request(endpoint, access_token, params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({
            "error": "Failed to get language list",
            "details": str(e),
            "params_sent": params
        }, indent=2)


@mcp_server.tool()
@meta_api_tool
async def create_targeting_spec(
    geo_locations: Dict[str, Any] = None,
    age_min: int = 18,
    age_max: int = 65,
    genders: List[int] = None,
    interests: List[Dict[str, Any]] = None,
    behaviors: List[Dict[str, Any]] = None,
    demographics: List[Dict[str, Any]] = None,
    custom_audiences: List[Dict[str, Any]] = None,
    lookalike_audiences: List[Dict[str, Any]] = None,
    excluded_custom_audiences: List[Dict[str, Any]] = None,
    connections: List[Dict[str, Any]] = None,
    excluded_connections: List[Dict[str, Any]] = None,
    locales: List[int] = None,
    device_platforms: List[str] = None,
    publisher_platforms: List[str] = None,
    facebook_positions: List[str] = None,
    instagram_positions: List[str] = None,
    audience_network_positions: List[str] = None,
    messenger_positions: List[str] = None,
    targeting_automation: Dict[str, Any] = None
) -> str:
    """
    Create a comprehensive targeting specification.
    
    Args:
        geo_locations: Geographic targeting (countries, regions, cities, zip codes)
        age_min: Minimum age for targeting
        age_max: Maximum age for targeting
        genders: List of genders to target (1=male, 2=female, 0=all)
        interests: List of interest targeting
        behaviors: List of behavior targeting
        demographics: List of demographic targeting
        custom_audiences: List of custom audiences to include
        lookalike_audiences: List of lookalike audiences to include
        excluded_custom_audiences: List of custom audiences to exclude
        connections: List of connection targeting
        excluded_connections: List of connections to exclude
        locales: List of language/locale targeting
        device_platforms: List of device platforms (mobile, desktop)
        publisher_platforms: List of publisher platforms (facebook, instagram, etc.)
        facebook_positions: List of Facebook ad positions
        instagram_positions: List of Instagram ad positions
        audience_network_positions: List of Audience Network positions
        messenger_positions: List of Messenger ad positions
        targeting_automation: Advantage+ targeting automation settings
    
    Returns:
        JSON targeting specification
    """
    targeting_spec = {}
    
    # Basic demographic targeting
    if geo_locations:
        targeting_spec["geo_locations"] = geo_locations
    
    if age_min:
        targeting_spec["age_min"] = age_min
    
    if age_max:
        targeting_spec["age_max"] = age_max
    
    if genders:
        targeting_spec["genders"] = genders
    
    if locales:
        targeting_spec["locales"] = locales
    
    # Detailed targeting
    flexible_spec = []
    
    if interests:
        flexible_spec.append({"interests": interests})
    
    if behaviors:
        flexible_spec.append({"behaviors": behaviors})
    
    if demographics:
        flexible_spec.append({"demographics": demographics})
    
    if flexible_spec:
        targeting_spec["flexible_spec"] = flexible_spec
    
    # Custom audiences
    if custom_audiences:
        targeting_spec["custom_audiences"] = custom_audiences
    
    if lookalike_audiences:
        targeting_spec["lookalike_audiences"] = lookalike_audiences
    
    if excluded_custom_audiences:
        targeting_spec["excluded_custom_audiences"] = excluded_custom_audiences
    
    # Connections
    if connections:
        targeting_spec["connections"] = connections
    
    if excluded_connections:
        targeting_spec["excluded_connections"] = excluded_connections
    
    # Device and platform targeting
    if device_platforms:
        targeting_spec["device_platforms"] = device_platforms
    
    if publisher_platforms:
        targeting_spec["publisher_platforms"] = publisher_platforms
    
    if facebook_positions:
        targeting_spec["facebook_positions"] = facebook_positions
    
    if instagram_positions:
        targeting_spec["instagram_positions"] = instagram_positions
    
    if audience_network_positions:
        targeting_spec["audience_network_positions"] = audience_network_positions
    
    if messenger_positions:
        targeting_spec["messenger_positions"] = messenger_positions
    
    # Advantage+ targeting automation
    if targeting_automation:
        targeting_spec["targeting_automation"] = targeting_automation
    
    return json.dumps({
        "targeting_spec": targeting_spec,
        "usage": "Use this targeting specification in the 'targeting' parameter when creating ad sets"
    }, indent=2)