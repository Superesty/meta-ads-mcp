"""Lead Generation Forms functionality for Meta Ads API."""

import json
from typing import Optional, List, Dict, Any, Union
from .api import meta_api_tool, make_api_request
from .accounts import get_ad_accounts
from .server import mcp_server


@mcp_server.tool()
@meta_api_tool
async def create_lead_form(
    access_token: str = None,
    page_id: str = None,
    name: str = None,
    locale: str = "en_US",
    privacy_policy_url: str = None,
    questions: List[Dict[str, Any]] = None,
    context_card: Dict[str, Any] = None,
    thank_you_page: Dict[str, Any] = None,
    follow_up_action_url: str = None,
    legal_content: Dict[str, Any] = None,
    is_continued_flow: bool = False,
    custom_disclaimer: str = None,
    allow_organic_lead: bool = True,
    block_display_for_non_targeted_viewer: bool = False
) -> str:
    """
    Create a lead generation form for Meta Ads campaigns.
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        page_id: Facebook Page ID that will own the lead form
        name: Name of the lead form
        locale: Language locale for the form (default: en_US)
        privacy_policy_url: URL to privacy policy (required in many regions)
        questions: List of custom questions for the form
        context_card: Opening context card configuration
        thank_you_page: Thank you page configuration after form submission
        follow_up_action_url: URL to redirect after form completion
        legal_content: Legal content and disclaimers
        is_continued_flow: Whether this is part of a continued flow
        custom_disclaimer: Custom disclaimer text
        allow_organic_lead: Whether to allow organic (non-paid) leads
        block_display_for_non_targeted_viewer: Whether to block display for non-targeted viewers
    
    Returns:
        JSON response with created lead form details
    """
    if not page_id:
        return json.dumps({"error": "Page ID is required to create a lead form"}, indent=2)
    
    if not name:
        return json.dumps({"error": "Lead form name is required"}, indent=2)
    
    # Build the lead form data
    form_data = {
        "name": name,
        "locale": locale,
        "allow_organic_lead": allow_organic_lead,
        "block_display_for_non_targeted_viewer": block_display_for_non_targeted_viewer,
        "is_continued_flow": is_continued_flow
    }
    
    # Add privacy policy URL if provided
    if privacy_policy_url:
        form_data["privacy_policy_url"] = privacy_policy_url
    
    # Add custom disclaimer if provided
    if custom_disclaimer:
        form_data["custom_disclaimer"] = custom_disclaimer
    
    # Add follow-up action URL if provided
    if follow_up_action_url:
        form_data["follow_up_action_url"] = follow_up_action_url
    
    # Add questions if provided, otherwise use default questions
    if questions:
        form_data["questions"] = questions
    else:
        # Default questions for lead forms
        form_data["questions"] = [
            {
                "type": "FIRST_NAME",
                "required": True
            },
            {
                "type": "LAST_NAME", 
                "required": True
            },
            {
                "type": "EMAIL",
                "required": True
            },
            {
                "type": "PHONE",
                "required": False
            }
        ]
    
    # Add context card if provided
    if context_card:
        form_data["context_card"] = context_card
    
    # Add thank you page if provided
    if thank_you_page:
        form_data["thank_you_page"] = thank_you_page
    
    # Add legal content if provided
    if legal_content:
        form_data["legal_content"] = legal_content
    
    endpoint = f"{page_id}/leadgen_forms"
    
    try:
        data = await make_api_request(endpoint, access_token, form_data, method="POST")
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({
            "error": "Failed to create lead form",
            "details": str(e),
            "form_data_sent": form_data
        }, indent=2)


@mcp_server.tool()
@meta_api_tool
async def get_lead_forms(
    access_token: str = None,
    page_id: str = None,
    limit: int = 10,
    fields: str = "id,name,status,locale,questions,context_card,thank_you_page,privacy_policy_url,created_time,expired_leads_count,leads_count"
) -> str:
    """
    Get lead forms associated with a Facebook Page.
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        page_id: Facebook Page ID to get lead forms for
        limit: Maximum number of lead forms to return
        fields: Comma-separated list of fields to retrieve
    
    Returns:
        JSON response with lead forms data
    """
    if not page_id:
        return json.dumps({"error": "Page ID is required to get lead forms"}, indent=2)
    
    endpoint = f"{page_id}/leadgen_forms"
    params = {
        "fields": fields,
        "limit": limit
    }
    
    try:
        data = await make_api_request(endpoint, access_token, params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({
            "error": "Failed to get lead forms",
            "details": str(e)
        }, indent=2)


@mcp_server.tool()
@meta_api_tool
async def get_lead_form_details(
    access_token: str = None,
    form_id: str = None,
    fields: str = "id,name,status,locale,questions,context_card,thank_you_page,privacy_policy_url,created_time,expired_leads_count,leads_count,allow_organic_lead,block_display_for_non_targeted_viewer"
) -> str:
    """
    Get detailed information about a specific lead form.
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        form_id: Lead form ID
        fields: Comma-separated list of fields to retrieve
    
    Returns:
        JSON response with lead form details
    """
    if not form_id:
        return json.dumps({"error": "Form ID is required"}, indent=2)
    
    endpoint = f"{form_id}"
    params = {
        "fields": fields
    }
    
    try:
        data = await make_api_request(endpoint, access_token, params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({
            "error": "Failed to get lead form details",
            "details": str(e)
        }, indent=2)


@mcp_server.tool()
@meta_api_tool
async def update_lead_form(
    access_token: str = None,
    form_id: str = None,
    name: str = None,
    status: str = None,
    privacy_policy_url: str = None,
    questions: List[Dict[str, Any]] = None,
    context_card: Dict[str, Any] = None,
    thank_you_page: Dict[str, Any] = None,
    follow_up_action_url: str = None,
    custom_disclaimer: str = None,
    allow_organic_lead: bool = None,
    block_display_for_non_targeted_viewer: bool = None
) -> str:
    """
    Update an existing lead form.
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        form_id: Lead form ID to update
        name: New name for the lead form
        status: New status (ACTIVE, ARCHIVED, DRAFT, DELETED)
        privacy_policy_url: New privacy policy URL
        questions: Updated list of custom questions
        context_card: Updated context card configuration
        thank_you_page: Updated thank you page configuration
        follow_up_action_url: Updated follow-up action URL
        custom_disclaimer: Updated custom disclaimer text
        allow_organic_lead: Whether to allow organic (non-paid) leads
        block_display_for_non_targeted_viewer: Whether to block display for non-targeted viewers
    
    Returns:
        JSON response with update result
    """
    if not form_id:
        return json.dumps({"error": "Form ID is required to update lead form"}, indent=2)
    
    # Build update data with only provided fields
    update_data = {}
    
    if name is not None:
        update_data["name"] = name
    if status is not None:
        update_data["status"] = status
    if privacy_policy_url is not None:
        update_data["privacy_policy_url"] = privacy_policy_url
    if questions is not None:
        update_data["questions"] = questions
    if context_card is not None:
        update_data["context_card"] = context_card
    if thank_you_page is not None:
        update_data["thank_you_page"] = thank_you_page
    if follow_up_action_url is not None:
        update_data["follow_up_action_url"] = follow_up_action_url
    if custom_disclaimer is not None:
        update_data["custom_disclaimer"] = custom_disclaimer
    if allow_organic_lead is not None:
        update_data["allow_organic_lead"] = allow_organic_lead
    if block_display_for_non_targeted_viewer is not None:
        update_data["block_display_for_non_targeted_viewer"] = block_display_for_non_targeted_viewer
    
    if not update_data:
        return json.dumps({"error": "No update parameters provided"}, indent=2)
    
    endpoint = f"{form_id}"
    
    try:
        data = await make_api_request(endpoint, access_token, update_data, method="POST")
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({
            "error": "Failed to update lead form",
            "details": str(e),
            "update_data_sent": update_data
        }, indent=2)


@mcp_server.tool()
@meta_api_tool
async def get_lead_form_submissions(
    access_token: str = None,
    form_id: str = None,
    limit: int = 100,
    filtering: List[Dict[str, Any]] = None,
    fields: str = "id,created_time,field_data,is_organic,ad_id,adset_id,campaign_id,form_id,platform"
) -> str:
    """
    Get lead submissions for a specific lead form.
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        form_id: Lead form ID to get submissions for
        limit: Maximum number of submissions to return
        filtering: Filter criteria for submissions
        fields: Comma-separated list of fields to retrieve
    
    Returns:
        JSON response with lead submissions
    """
    if not form_id:
        return json.dumps({"error": "Form ID is required to get lead submissions"}, indent=2)
    
    endpoint = f"{form_id}/leads"
    params = {
        "fields": fields,
        "limit": limit
    }
    
    # Add filtering if provided
    if filtering:
        params["filtering"] = json.dumps(filtering)
    
    try:
        data = await make_api_request(endpoint, access_token, params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({
            "error": "Failed to get lead form submissions",
            "details": str(e)
        }, indent=2)


@mcp_server.tool()
@meta_api_tool
async def delete_lead_form(
    access_token: str = None,
    form_id: str = None
) -> str:
    """
    Delete a lead form.
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        form_id: Lead form ID to delete
    
    Returns:
        JSON response with deletion result
    """
    if not form_id:
        return json.dumps({"error": "Form ID is required to delete lead form"}, indent=2)
    
    endpoint = f"{form_id}"
    
    try:
        data = await make_api_request(endpoint, access_token, {}, method="DELETE")
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({
            "error": "Failed to delete lead form",
            "details": str(e)
        }, indent=2)


@mcp_server.tool()
@meta_api_tool
async def create_lead_form_question(
    question_type: str = None,
    required: bool = True,
    label: str = None,
    options: List[str] = None,
    conditional_questions: List[Dict[str, Any]] = None
) -> str:
    """
    Helper function to create a lead form question configuration.
    
    Args:
        question_type: Type of question (FIRST_NAME, LAST_NAME, EMAIL, PHONE, etc.)
        required: Whether the question is required
        label: Custom label for the question
        options: List of options for multiple choice questions
        conditional_questions: List of conditional questions based on answer
    
    Returns:
        JSON configuration for the question
    """
    if not question_type:
        return json.dumps({"error": "Question type is required"}, indent=2)
    
    question_config = {
        "type": question_type,
        "required": required
    }
    
    if label:
        question_config["label"] = label
    
    if options:
        question_config["options"] = options
    
    if conditional_questions:
        question_config["conditional_questions"] = conditional_questions
    
    return json.dumps({
        "question_config": question_config,
        "usage": "Use this configuration in the 'questions' parameter when creating or updating a lead form"
    }, indent=2)


@mcp_server.tool()
@meta_api_tool
async def get_lead_form_question_types(access_token: str = None) -> str:
    """
    Get available question types for lead forms.
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
    
    Returns:
        JSON response with available question types and their descriptions
    """
    question_types = {
        "standard_questions": {
            "FIRST_NAME": "First name field",
            "LAST_NAME": "Last name field", 
            "EMAIL": "Email address field",
            "PHONE": "Phone number field",
            "GENDER": "Gender selection",
            "DATE_OF_BIRTH": "Date of birth field",
            "ZIP_CODE": "ZIP/postal code field",
            "CITY": "City field",
            "STATE": "State/province field",
            "COUNTRY": "Country field",
            "WORK_EMAIL": "Work email field",
            "COMPANY_NAME": "Company name field",
            "JOB_TITLE": "Job title field",
            "WORK_PHONE": "Work phone number field",
            "FULL_ADDRESS": "Full address field",
            "STREET_ADDRESS": "Street address field"
        },
        "custom_questions": {
            "CUSTOM": "Custom text field",
            "MULTIPLE_CHOICE": "Multiple choice question",
            "CONDITIONAL": "Conditional question based on previous answer"
        },
        "special_questions": {
            "RETAILER": "Retailer selection for auto lead ads",
            "VEHICLE_TYPE": "Vehicle type for auto lead ads",
            "PREFERRED_CONTACT_TIME": "Preferred contact time",
            "MILITARY_STATUS": "Military status",
            "MARITAL_STATUS": "Marital status"
        }
    }
    
    return json.dumps({
        "question_types": question_types,
        "usage": "Use these question types when creating questions for lead forms",
        "example": {
            "type": "FIRST_NAME",
            "required": True,
            "label": "What's your first name?"
        }
    }, indent=2)