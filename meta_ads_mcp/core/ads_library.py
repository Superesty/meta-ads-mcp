"""Adds Library-related functionality for Meta Ads API."""

import json
import httpx
import base64
from typing import Optional, List, Dict, Any
from .api import meta_api_tool, make_api_request
from .server import mcp_server
from .utils import logger


@mcp_server.tool()
@meta_api_tool
async def search_ads_archive(
    access_token: str = None,
    search_terms: str = None,
    ad_type: str = "ALL",
    ad_reached_countries: List[str] = None,
    limit: int = 25,  # Default limit, adjust as needed
    fields: str = "ad_creation_time,ad_creative_body,ad_creative_link_caption,ad_creative_link_description,ad_creative_link_title,ad_delivery_start_time,ad_delivery_stop_time,ad_snapshot_url,currency,demographic_distribution,funding_entity,impressions,page_id,page_name,publisher_platform,region_distribution,spend"
) -> str:
    """
    Search the Facebook Ads Library archive.

    Args:
        access_token: Meta API access token (optional - will use cached token if not provided).
        search_terms: The search query for ads.
        ad_type: Type of ads to search for (e.g., POLITICAL_AND_ISSUE_ADS, HOUSING_ADS, ALL).
        ad_reached_countries: List of country codes (e.g., ["US", "GB"]).
        limit: Maximum number of ads to return.
        fields: Comma-separated string of fields to retrieve for each ad.

    Example Usage via curl equivalent:
        curl -G \\
        -d "search_terms='california'" \\
        -d "ad_type=POLITICAL_AND_ISSUE_ADS" \\
        -d "ad_reached_countries=['US']" \\
        -d "fields=ad_snapshot_url,spend" \\
        -d "access_token=<ACCESS_TOKEN>" \\
        "https://graph.facebook.com/<API_VERSION>/ads_archive"
    """
    if not access_token:
        # Attempt to get token implicitly if not provided - meta_api_tool handles this
        pass

    if not search_terms:
        return json.dumps({"error": "search_terms parameter is required"}, indent=2)

    if not ad_reached_countries:
        return json.dumps({"error": "ad_reached_countries parameter is required"}, indent=2)

    endpoint = "ads_archive"
    params = {
        "search_terms": search_terms,
        "ad_type": ad_type,
        "ad_reached_countries": json.dumps(ad_reached_countries), # API expects a JSON array string
        "limit": limit,
        "fields": fields,
    }

    try:
        data = await make_api_request(endpoint, access_token, params, method="GET")
        return json.dumps(data, indent=2)
    except Exception as e:
        error_msg = str(e)
        # Consider logging the full error for debugging
        # print(f"Error calling Ads Library API: {error_msg}")
        return json.dumps({
            "error": "Failed to search ads archive",
            "details": error_msg,
            "params_sent": {k: v for k, v in params.items() if k != 'access_token'} # Avoid logging token
        }, indent=2) 


@mcp_server.tool()
@meta_api_tool
async def upload_video_from_supabase(
    access_token: str = None,
    account_id: str = None,
    supabase_video_path: str = None,
    video_title: str = None,
    supabase_url: str = "https://yrbopirjmvukqgsurhxs.supabase.co",
    bucket_name: str = "javier_cano_kno_men_barcelona"
) -> str:
    """
    Upload a video from Supabase storage to Meta Ads Library for use in ad creatives.
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        account_id: Meta Ads account ID (format: act_XXXXXXXXX)
        supabase_video_path: Path to the video file in Supabase bucket (e.g., 'Botox/video/Uso_Botox_Correcto.mp4')
        video_title: Title for the video in Meta Ads Library (optional - defaults to filename)
        supabase_url: Supabase project URL (defaults to Cogitia production)
        bucket_name: Supabase bucket name (defaults to Cogitia bucket)
    
    Returns:
        JSON response with video details including video_id for creative creation
        
    Example usage:
        upload_video_from_supabase(
            account_id="act_123456789",
            supabase_video_path="Botox/video/Uso_Botox_Correcto.mp4",
            video_title="Uso Correcto del Botox"
        )
    """
    # Check required parameters
    if not account_id:
        return json.dumps({"error": "No account ID provided"}, indent=2)
    
    if not supabase_video_path:
        return json.dumps({"error": "No Supabase video path provided"}, indent=2)
    
    # Ensure account_id has the 'act_' prefix for API compatibility
    if not account_id.startswith("act_"):
        account_id = f"act_{account_id}"
    
    # Construct the public URL for the video in Supabase
    video_url = f"{supabase_url}/storage/v1/object/public/{bucket_name}/{supabase_video_path}"
    
    # Get video filename if title not provided
    if not video_title:
        video_title = supabase_video_path.split('/')[-1].replace('.mp4', '').replace('_', ' ')
    
    try:
        logger.info(f"Downloading video from Supabase: {video_url}")
        
        # Download video from Supabase
        async with httpx.AsyncClient() as client:
            response = await client.get(video_url, timeout=60.0)  # Longer timeout for videos
            response.raise_for_status()
            video_bytes = response.content
            
        logger.info(f"Successfully downloaded video: {len(video_bytes)} bytes")
        
        # Convert video to base64 for Meta API upload
        encoded_video = base64.b64encode(video_bytes).decode('utf-8')
        
        # Prepare the API endpoint for uploading videos
        endpoint = f"{account_id}/advideos"
        
        # Prepare POST parameters for video upload
        params = {
            "file_url": video_url,  # Meta API can also accept URL directly
            "title": video_title,
            "description": f"Video uploaded from Cogitia Supabase: {supabase_video_path}"
        }
        
        logger.info(f"Uploading video to Meta Ad Account {account_id} with title: {video_title}")
        
        # Make API request to upload the video
        data = await make_api_request(endpoint, access_token, params, method="POST")
        
        # Log success
        if "id" in data:
            logger.info(f"Successfully uploaded video with ID: {data['id']}")
        
        return json.dumps(data, indent=2)
    
    except httpx.HTTPStatusError as e:
        error_msg = f"Failed to download video from Supabase: HTTP {e.response.status_code}"
        logger.error(error_msg)
        return json.dumps({
            "error": error_msg,
            "video_url": video_url,
            "status_code": e.response.status_code
        }, indent=2)
        
    except Exception as e:
        error_msg = f"Failed to upload video: {str(e)}"
        logger.error(error_msg)
        return json.dumps({
            "error": error_msg,
            "video_url": video_url,
            "video_path": supabase_video_path
        }, indent=2)


@mcp_server.tool()
@meta_api_tool
async def list_account_videos(
    access_token: str = None,
    account_id: str = None,
    limit: int = 25,
    fields: str = "id,title,description,created_time,length,status,thumbnails"
) -> str:
    """
    List all videos in the Meta Ads account library.
    
    Args:
        access_token: Meta API access token (optional - will use cached token if not provided)
        account_id: Meta Ads account ID (format: act_XXXXXXXXX)
        limit: Maximum number of videos to return (default: 25)
        fields: Comma-separated fields to retrieve for each video
    
    Returns:
        JSON response with list of videos in the account
    """
    # Check required parameters
    if not account_id:
        return json.dumps({"error": "No account ID provided"}, indent=2)
    
    # Ensure account_id has the 'act_' prefix for API compatibility
    if not account_id.startswith("act_"):
        account_id = f"act_{account_id}"
    
    # Prepare the API endpoint for listing videos
    endpoint = f"{account_id}/advideos"
    
    params = {
        "limit": limit,
        "fields": fields
    }
    
    try:
        logger.info(f"Fetching videos from Meta Ad Account {account_id}")
        data = await make_api_request(endpoint, access_token, params, method="GET")
        return json.dumps(data, indent=2)
        
    except Exception as e:
        error_msg = f"Failed to fetch account videos: {str(e)}"
        logger.error(error_msg)
        return json.dumps({
            "error": error_msg,
            "account_id": account_id
        }, indent=2)


@mcp_server.tool()
async def list_supabase_videos(
    supabase_url: str = "https://yrbopirjmvukqgsurhxs.supabase.co",
    bucket_name: str = "javier_cano_kno_men_barcelona",
    category_filter: str = None
) -> str:
    """
    List available videos in the Supabase bucket for upload to Meta Ads.
    
    Args:
        supabase_url: Supabase project URL (defaults to Cogitia production)
        bucket_name: Supabase bucket name (defaults to Cogitia bucket)
        category_filter: Optional filter by category (e.g., 'Botox', 'Cuidado_de_la_Piel', etc.)
    
    Returns:
        JSON response with list of available videos organized by category
    """
    try:
        # This would ideally use Supabase SDK, but for now we'll provide a static structure
        # based on what we know is in the bucket
        available_videos = {
            "bucket_info": {
                "url": supabase_url,
                "bucket_name": bucket_name,
                "base_video_url": f"{supabase_url}/storage/v1/object/public/{bucket_name}"
            },
            "categories": {
                "Botox": {
                    "total_videos": 5,
                    "videos": [
                        "Botox/video/Uso_Botox_Correcto.mp4",
                        "Botox/video/Suavizado_Natural_Arrugas.mp4", 
                        "Botox/video/Prevencion_Arrugas_Botox.mp4",
                        "Botox/video/Errores_Botox_Exceso_Profesional.mp4",
                        "Botox/video/Armonia_Natural_Botox.mp4"
                    ]
                },
                "Cuidado_de_la_Piel": {
                    "total_videos": 11,
                    "videos": [
                        "Cuidado_de_la_Piel/video/Tratamiento_Piel_Duradero.mp4",
                        "Cuidado_de_la_Piel/video/Tratamientos_Piel_Seguros.mp4",
                        "Cuidado_de_la_Piel/video/Tratamientos_Eficaces_Piel.mp4",
                        "Cuidado_de_la_Piel/video/Procedimientos_Esteticos_Seguros.mp4",
                        "Cuidado_de_la_Piel/video/Prevencion_Necrosis_por_Intrusismo.mp4",
                        "Cuidado_de_la_Piel/video/Prevencion_Envejecimiento_Cutaneo.mp4",
                        "Cuidado_de_la_Piel/video/Errores_Comunes_en_Tratamientos_Esteticos.mp4",
                        "Cuidado_de_la_Piel/video/Errores_antes_tratamiento_estetico.mp4",
                        "Cuidado_de_la_Piel/video/Doctor_Calificado_Advertencias.mp4",
                        "Cuidado_de_la_Piel/video/CuidadoPiel_Evaluacion_Previa.mp4",
                        "Cuidado_de_la_Piel/video/CuidadoPiel_Consulta_Especialista.mp4"
                    ]
                },
                "Otros_Procedimientos": {
                    "total_videos": 10,
                    "videos": [
                        "Otros_Procedimientos/video/Transformacion_Corporal.mp4",
                        "Otros_Procedimientos/video/Suscripcion_Otros_Procedimientos.mp4",
                        "Otros_Procedimientos/video/Otros_Procedimientos_08.mp4",
                        "Otros_Procedimientos/video/Otros_Procedimientos_07.mp4"
                        # Note: There are more videos in this category
                    ]
                },
                "Rejuvenecimiento_Facial": {
                    "total_videos": 22,
                    "description": "Largest category with facial rejuvenation content"
                },
                "Acido_Hialuronico": {
                    "total_videos": 9,
                    "description": "Hyaluronic acid treatment videos"
                }
            },
            "usage_example": {
                "description": "To upload a video, use upload_video_from_supabase with the video path",
                "example_call": "upload_video_from_supabase(account_id='act_123456789', supabase_video_path='Botox/video/Uso_Botox_Correcto.mp4')"
            }
        }
        
        # Apply category filter if provided
        if category_filter:
            if category_filter in available_videos["categories"]:
                filtered_result = {
                    "bucket_info": available_videos["bucket_info"],
                    "filtered_category": category_filter,
                    "category_data": available_videos["categories"][category_filter],
                    "usage_example": available_videos["usage_example"]
                }
                return json.dumps(filtered_result, indent=2)
            else:
                return json.dumps({
                    "error": f"Category '{category_filter}' not found",
                    "available_categories": list(available_videos["categories"].keys())
                }, indent=2)
        
        return json.dumps(available_videos, indent=2)
        
    except Exception as e:
        return json.dumps({
            "error": f"Failed to list Supabase videos: {str(e)}"
        }, indent=2)