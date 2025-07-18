"""Campaign-related functionality for Meta Ads API."""

import json
from typing import List, Optional, Dict, Any, Union
from .api import meta_api_tool, make_api_request
from .accounts import get_ad_accounts
from .server import mcp_server


@mcp_server.tool()
@meta_api_tool
async def get_campaigns(access_token: str = None, account_id: str = None, limit: int = 10, status_filter: str = "", after: str = "") -> str:
    """
    Get campaigns for a Meta Ads account with optional filtering.
    
    Note: By default, the Meta API returns a subset of available fields. 
    Other fields like 'effective_status', 'special_ad_categories', 
    'lifetime_budget', 'spend_cap', 'budget_remaining', 'promoted_object', 
    'source_campaign_id', etc., might be available but require specifying them
    in the API call (currently not exposed by this tool's parameters).
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        account_id: Meta Ads account ID (format: act_XXXXXXXXX)
        limit: Maximum number of campaigns to return (default: 10)
        status_filter: Filter by effective status (e.g., 'ACTIVE', 'PAUSED', 'ARCHIVED').
                       Maps to the 'effective_status' API parameter, which expects an array
                       (this function handles the required JSON formatting). Leave empty for all statuses.
        after: Pagination cursor to get the next set of results
    """
    # If no account ID is specified, try to get the first one for the user
    if not account_id:
        accounts_json = await get_ad_accounts(access_token=access_token, user_id="me", limit=1)
        accounts_data = json.loads(accounts_json)
        
        if "data" in accounts_data and accounts_data["data"]:
            account_id = accounts_data["data"][0]["id"]
        else:
            return json.dumps({"error": "No account ID specified and no accounts found for user"}, indent=2)
    
    endpoint = f"{account_id}/campaigns"
    params = {
        "fields": "id,name,objective,status,daily_budget,lifetime_budget,buying_type,start_time,stop_time,created_time,updated_time,bid_strategy,effective_status,special_ad_categories,special_ad_category_country,budget_remaining,configured_status,smart_promotion_type,source_campaign_id,pacing_type,spend_cap,budget_optimization,campaign_optimization_type",
        "limit": limit
    }
    
    if status_filter:
        # API expects an array, encode it as a JSON string
        params["effective_status"] = json.dumps([status_filter])
    
    if after:
        params["after"] = after
    
    data = await make_api_request(endpoint, access_token, params)
    
    return json.dumps(data, indent=2)


@mcp_server.tool()
@meta_api_tool
async def get_campaign_details(access_token: str = None, campaign_id: str = None) -> str:
    """
    Get detailed information about a specific campaign.

    Note: This function requests a specific set of fields ('id,name,objective,status,...'). 
    The Meta API offers many other fields for campaigns (e.g., 'effective_status', 'source_campaign_id', etc.) 
    that could be added to the 'fields' parameter in the code if needed.
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        campaign_id: Meta Ads campaign ID
    """
    if not campaign_id:
        return json.dumps({"error": "No campaign ID provided"}, indent=2)
    
    endpoint = f"{campaign_id}"
    params = {
        "fields": "id,name,objective,status,daily_budget,lifetime_budget,buying_type,start_time,stop_time,created_time,updated_time,bid_strategy,effective_status,special_ad_categories,special_ad_category_country,budget_remaining,configured_status,smart_promotion_type,source_campaign_id,pacing_type,spend_cap,budget_optimization,campaign_optimization_type"
    }
    
    data = await make_api_request(endpoint, access_token, params)
    
    return json.dumps(data, indent=2)


@mcp_server.tool()
@meta_api_tool
async def create_campaign(
    access_token: str = None,
    account_id: str = None,
    name: str = None,
    objective: str = None,
    status: str = "PAUSED",
    special_ad_categories: List[str] = None,
    special_ad_category_country: List[str] = None,
    daily_budget = None,
    lifetime_budget = None,
    buying_type: str = None,
    bid_strategy: str = None,
    bid_cap = None,
    spend_cap = None,
    campaign_budget_optimization: bool = None,
    budget_optimization: bool = None,
    smart_promotion_type: str = None,
    source_campaign_id: str = None,
    pacing_type: List[str] = None,
    campaign_optimization_type: str = None,
    start_time: str = None,
    stop_time: str = None,
    ab_test_control_setups: Optional[List[Dict[str, Any]]] = None,
    adlabels: Optional[List[Dict[str, Any]]] = None,
    iterative_split_test_configs: Optional[List[Dict[str, Any]]] = None
) -> str:
    """
    Create a new campaign in a Meta Ads account with comprehensive field support.
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        account_id: Meta Ads account ID (format: act_XXXXXXXXX)
        name: Campaign name
        objective: Campaign objective. Validates ad objectives. enum{BRAND_AWARENESS, LEAD_GENERATION, LINK_CLICKS, CONVERSIONS, OUTCOME_TRAFFIC, OUTCOME_SALES, etc.}.
        status: Initial campaign status (default: PAUSED)
        special_ad_categories: List of special ad categories if applicable (["HOUSING"], ["EMPLOYMENT"], ["CREDIT"])
        special_ad_category_country: List of countries for special ad categories (["US"], ["CA"])
        daily_budget: Daily budget in account currency (in cents) as a string
        lifetime_budget: Lifetime budget in account currency (in cents) as a string
        buying_type: Buying type (e.g., 'AUCTION', 'RESERVED')
        bid_strategy: Bid strategy (e.g., 'LOWEST_COST', 'LOWEST_COST_WITH_BID_CAP', 'COST_CAP')
        bid_cap: Bid cap in account currency (in cents) as a string
        spend_cap: Spending limit for the campaign in account currency (in cents) as a string
        campaign_budget_optimization: Whether to enable campaign budget optimization (deprecated, use budget_optimization)
        budget_optimization: Whether to enable budget optimization (CBO)
        smart_promotion_type: Type of smart promotion (e.g., 'AUTOMATED_SHOPPING_ADS' for Advantage+ Shopping)
        source_campaign_id: Source campaign ID for duplication
        pacing_type: List of pacing types (e.g., ['standard', 'accelerated'])
        campaign_optimization_type: Optimization type for the campaign
        start_time: Start time in ISO 8601 format (e.g., '2023-12-01T12:00:00-0800')
        stop_time: Stop time in ISO 8601 format
        ab_test_control_setups: Settings for A/B testing (e.g., [{"name":"Creative A", "ad_format":"SINGLE_IMAGE"}])
        adlabels: List of ad labels for organization
        iterative_split_test_configs: Configurations for iterative split testing
    """
    # Check required parameters
    if not account_id:
        return json.dumps({"error": "No account ID provided"}, indent=2)
    
    if not name:
        return json.dumps({"error": "No campaign name provided"}, indent=2)
        
    if not objective:
        return json.dumps({"error": "No campaign objective provided"}, indent=2)
    
    # Special_ad_categories is required by the API, set default if not provided
    if special_ad_categories is None:
        special_ad_categories = []
    
    # For this example, we'll add a fixed daily budget if none is provided
    if not daily_budget and not lifetime_budget:
        daily_budget = "1000"  # Default to $10 USD
    
    endpoint = f"{account_id}/campaigns"
    
    params = {
        "name": name,
        "objective": objective,
        "status": status,
        "special_ad_categories": json.dumps(special_ad_categories)  # Properly format as JSON string
    }
    
    # Add special ad category country if provided
    if special_ad_category_country:
        params["special_ad_category_country"] = json.dumps(special_ad_category_country)
    
    # Convert budget values to strings if they aren't already
    if daily_budget is not None:
        params["daily_budget"] = str(daily_budget)
    
    if lifetime_budget is not None:
        params["lifetime_budget"] = str(lifetime_budget)
    
    # Add new parameters
    if buying_type:
        params["buying_type"] = buying_type
    
    if bid_strategy:
        params["bid_strategy"] = bid_strategy
    
    if bid_cap is not None:
        params["bid_cap"] = str(bid_cap)
    
    if spend_cap is not None:
        params["spend_cap"] = str(spend_cap)
    
    # Handle budget optimization (prefer budget_optimization over deprecated campaign_budget_optimization)
    if budget_optimization is not None:
        params["budget_optimization"] = "true" if budget_optimization else "false"
    elif campaign_budget_optimization is not None:
        params["campaign_budget_optimization"] = "true" if campaign_budget_optimization else "false"
    
    # Add Advantage+ Shopping support
    if smart_promotion_type:
        params["smart_promotion_type"] = smart_promotion_type
    
    # Add source campaign for duplication
    if source_campaign_id:
        params["source_campaign_id"] = source_campaign_id
    
    # Add pacing type
    if pacing_type:
        params["pacing_type"] = json.dumps(pacing_type)
    
    # Add campaign optimization type
    if campaign_optimization_type:
        params["campaign_optimization_type"] = campaign_optimization_type
    
    # Add start and stop times
    if start_time:
        params["start_time"] = start_time
    
    if stop_time:
        params["stop_time"] = stop_time
    
    # Add A/B test configurations
    if ab_test_control_setups:
        params["ab_test_control_setups"] = json.dumps(ab_test_control_setups)
    
    # Add ad labels for organization
    if adlabels:
        params["adlabels"] = json.dumps(adlabels)
    
    # Add iterative split test configurations
    if iterative_split_test_configs:
        params["iterative_split_test_configs"] = json.dumps(iterative_split_test_configs)
    
    try:
        data = await make_api_request(endpoint, access_token, params, method="POST")
        return json.dumps(data, indent=2)
    except Exception as e:
        error_msg = str(e)
        return json.dumps({
            "error": "Failed to create campaign",
            "details": error_msg,
            "params_sent": params
        }, indent=2)


@mcp_server.tool()
@meta_api_tool
async def update_campaign(
    access_token: str = None,
    campaign_id: str = None,
    name: str = None,
    status: str = None,
    special_ad_categories: List[str] = None,
    daily_budget = None,
    lifetime_budget = None,
    bid_strategy: str = None,
    bid_cap = None,
    spend_cap = None,
    campaign_budget_optimization: bool = None,
    objective: str = None,  # Add objective if it's updatable
    # Add other updatable fields as needed based on API docs
) -> str:
    """
    Update an existing campaign in a Meta Ads account.

    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        campaign_id: Meta Ads campaign ID (required)
        name: New campaign name
        status: New campaign status (e.g., 'ACTIVE', 'PAUSED')
        special_ad_categories: List of special ad categories if applicable
        daily_budget: New daily budget in account currency (in cents) as a string
        lifetime_budget: New lifetime budget in account currency (in cents) as a string
        bid_strategy: New bid strategy
        bid_cap: New bid cap in account currency (in cents) as a string
        spend_cap: New spending limit for the campaign in account currency (in cents) as a string
        campaign_budget_optimization: Enable/disable campaign budget optimization
        objective: New campaign objective (Note: May not always be updatable)
    """
    if not campaign_id:
        return json.dumps({"error": "No campaign ID provided"}, indent=2)

    endpoint = f"{campaign_id}"
    
    params = {}
    
    # Add parameters to the request only if they are provided
    if name is not None:
        params["name"] = name
    if status is not None:
        params["status"] = status
    if special_ad_categories is not None:
        # Note: Updating special_ad_categories might have specific API rules or might not be allowed after creation.
        # The API might require an empty list `[]` to clear categories. Check Meta Docs.
        params["special_ad_categories"] = json.dumps(special_ad_categories)
    if daily_budget is not None:
        params["daily_budget"] = str(daily_budget)
    if lifetime_budget is not None:
        params["lifetime_budget"] = str(lifetime_budget)
    if bid_strategy is not None:
        params["bid_strategy"] = bid_strategy
    if bid_cap is not None:
        params["bid_cap"] = str(bid_cap)
    if spend_cap is not None:
        params["spend_cap"] = str(spend_cap)
    if campaign_budget_optimization is not None:
        params["campaign_budget_optimization"] = "true" if campaign_budget_optimization else "false"
    if objective is not None:
        params["objective"] = objective # Caution: Objective changes might reset learning or be restricted

    if not params:
        return json.dumps({"error": "No update parameters provided"}, indent=2)

    try:
        # Use POST method for updates as per Meta API documentation
        data = await make_api_request(endpoint, access_token, params, method="POST")
        return json.dumps(data, indent=2)
    except Exception as e:
        error_msg = str(e)
        # Include campaign_id in error for better context
        return json.dumps({
            "error": f"Failed to update campaign {campaign_id}",
            "details": error_msg,
            "params_sent": params # Be careful about logging sensitive data if any
        }, indent=2)


@mcp_server.tool()
@meta_api_tool
async def create_advantage_plus_shopping_campaign(
    access_token: str = None,
    account_id: str = None,
    name: str = None,
    status: str = "PAUSED",
    daily_budget = None,
    lifetime_budget = None,
    start_time: str = None,
    stop_time: str = None,
    special_ad_categories: List[str] = None,
    special_ad_category_country: List[str] = None
) -> str:
    """
    Create an Advantage+ Shopping Campaign (ASC) - Meta's automated shopping campaign type.
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        account_id: Meta Ads account ID (format: act_XXXXXXXXX)
        name: Campaign name
        status: Initial campaign status (default: PAUSED)
        daily_budget: Daily budget in account currency (in cents) as a string
        lifetime_budget: Lifetime budget in account currency (in cents) as a string
        start_time: Start time in ISO 8601 format (e.g., '2023-12-01T12:00:00-0800')
        stop_time: Stop time in ISO 8601 format
        special_ad_categories: List of special ad categories if applicable
        special_ad_category_country: List of countries for special ad categories
    
    Returns:
        JSON response with created Advantage+ Shopping Campaign details
    """
    # Check required parameters
    if not account_id:
        return json.dumps({"error": "No account ID provided"}, indent=2)
    
    if not name:
        return json.dumps({"error": "No campaign name provided"}, indent=2)
    
    # Special_ad_categories is required by the API, set default if not provided
    if special_ad_categories is None:
        special_ad_categories = []
    
    # For Advantage+ Shopping, we need at least one budget type
    if not daily_budget and not lifetime_budget:
        daily_budget = "1000"  # Default to $10 USD
    
    endpoint = f"{account_id}/campaigns"
    
    params = {
        "name": name,
        "objective": "OUTCOME_SALES",  # Required for Advantage+ Shopping
        "smart_promotion_type": "AUTOMATED_SHOPPING_ADS",  # This makes it an ASC
        "status": status,
        "special_ad_categories": json.dumps(special_ad_categories)
    }
    
    # Add special ad category country if provided
    if special_ad_category_country:
        params["special_ad_category_country"] = json.dumps(special_ad_category_country)
    
    # Convert budget values to strings if they aren't already
    if daily_budget is not None:
        params["daily_budget"] = str(daily_budget)
    
    if lifetime_budget is not None:
        params["lifetime_budget"] = str(lifetime_budget)
    
    # Add start and stop times
    if start_time:
        params["start_time"] = start_time
    
    if stop_time:
        params["stop_time"] = stop_time
    
    try:
        data = await make_api_request(endpoint, access_token, params, method="POST")
        return json.dumps(data, indent=2)
    except Exception as e:
        error_msg = str(e)
        return json.dumps({
            "error": "Failed to create Advantage+ Shopping Campaign",
            "details": error_msg,
            "params_sent": params
        }, indent=2)


@mcp_server.tool()
@meta_api_tool
async def get_campaign_objectives(access_token: str = None) -> str:
    """
    Get available campaign objectives and their descriptions.
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
    
    Returns:
        JSON response with campaign objectives and descriptions
    """
    objectives = {
        "standard_objectives": {
            "BRAND_AWARENESS": {
                "description": "Increase brand awareness and reach",
                "optimization_goals": ["BRAND_AWARENESS", "REACH", "IMPRESSIONS"],
                "billing_events": ["IMPRESSIONS"]
            },
            "REACH": {
                "description": "Reach the maximum number of people",
                "optimization_goals": ["REACH", "IMPRESSIONS"],
                "billing_events": ["IMPRESSIONS"]
            },
            "TRAFFIC": {
                "description": "Drive traffic to your website or app",
                "optimization_goals": ["LINK_CLICKS", "LANDING_PAGE_VIEWS"],
                "billing_events": ["LINK_CLICKS", "IMPRESSIONS"]
            },
            "ENGAGEMENT": {
                "description": "Get more engagement on your posts",
                "optimization_goals": ["ENGAGEMENT", "LINK_CLICKS"],
                "billing_events": ["IMPRESSIONS"]
            },
            "APP_INSTALLS": {
                "description": "Get more app installs",
                "optimization_goals": ["APP_INSTALLS", "LINK_CLICKS"],
                "billing_events": ["IMPRESSIONS"]
            },
            "VIDEO_VIEWS": {
                "description": "Get more video views",
                "optimization_goals": ["VIDEO_VIEWS", "IMPRESSIONS"],
                "billing_events": ["IMPRESSIONS"]
            },
            "LEAD_GENERATION": {
                "description": "Collect lead information",
                "optimization_goals": ["LEAD_GENERATION"],
                "billing_events": ["IMPRESSIONS"]
            },
            "MESSAGES": {
                "description": "Get more messages",
                "optimization_goals": ["CONVERSATIONS"],
                "billing_events": ["IMPRESSIONS"]
            },
            "CONVERSIONS": {
                "description": "Get more conversions on your website",
                "optimization_goals": ["CONVERSIONS", "LINK_CLICKS"],
                "billing_events": ["IMPRESSIONS"]
            },
            "CATALOG_SALES": {
                "description": "Promote products from your catalog",
                "optimization_goals": ["CONVERSIONS", "LINK_CLICKS"],
                "billing_events": ["IMPRESSIONS"]
            },
            "STORE_VISITS": {
                "description": "Drive visits to your physical store",
                "optimization_goals": ["STORE_VISITS"],
                "billing_events": ["IMPRESSIONS"]
            }
        },
        "outcome_objectives": {
            "OUTCOME_TRAFFIC": {
                "description": "Drive quality traffic to your destination",
                "optimization_goals": ["LINK_CLICKS", "LANDING_PAGE_VIEWS"],
                "billing_events": ["LINK_CLICKS", "IMPRESSIONS"]
            },
            "OUTCOME_ENGAGEMENT": {
                "description": "Get more meaningful engagement",
                "optimization_goals": ["ENGAGEMENT", "LINK_CLICKS"],
                "billing_events": ["IMPRESSIONS"]
            },
            "OUTCOME_LEADS": {
                "description": "Generate high-quality leads",
                "optimization_goals": ["LEAD_GENERATION"],
                "billing_events": ["IMPRESSIONS"]
            },
            "OUTCOME_SALES": {
                "description": "Drive purchases and sales",
                "optimization_goals": ["CONVERSIONS", "LINK_CLICKS"],
                "billing_events": ["IMPRESSIONS"]
            },
            "OUTCOME_APP_PROMOTION": {
                "description": "Promote your mobile app",
                "optimization_goals": ["APP_INSTALLS", "LINK_CLICKS"],
                "billing_events": ["IMPRESSIONS"]
            },
            "OUTCOME_AWARENESS": {
                "description": "Increase brand or product awareness",
                "optimization_goals": ["BRAND_AWARENESS", "REACH", "IMPRESSIONS"],
                "billing_events": ["IMPRESSIONS"]
            }
        },
        "advantage_plus_objectives": {
            "OUTCOME_SALES": {
                "description": "Used with Advantage+ Shopping Campaigns",
                "smart_promotion_type": "AUTOMATED_SHOPPING_ADS",
                "optimization_goals": ["CONVERSIONS"],
                "billing_events": ["IMPRESSIONS"]
            }
        }
    }
    
    return json.dumps({
        "objectives": objectives,
        "usage": "Use these objectives when creating campaigns. Each objective has specific optimization goals and billing events available."
    }, indent=2) 