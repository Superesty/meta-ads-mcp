"""Utility functions for Meta Ads API."""

from typing import Optional, Dict, Any
import httpx
import io
from PIL import Image as PILImage
import base64
import time
import asyncio
import os
import json
import logging
import pathlib
import platform

# Check for Meta app credentials in environment
META_APP_ID = os.environ.get("META_APP_ID", "")
META_APP_SECRET = os.environ.get("META_APP_SECRET", "")

# Only show warnings about Meta credentials if we're not using Pipeboard
# Check for Pipeboard token in environment
using_pipeboard = bool(os.environ.get("PIPEBOARD_API_TOKEN", ""))

# Print warning if Meta app credentials are not configured and not using Pipeboard
if not using_pipeboard:
    if not META_APP_ID:
        print("WARNING: META_APP_ID environment variable is not set.")
        print("RECOMMENDED: Use Pipeboard authentication by setting PIPEBOARD_API_TOKEN instead.")
        print("ALTERNATIVE: For direct Meta authentication, set META_APP_ID to your Meta App ID.")
    if not META_APP_SECRET:
        print("WARNING: META_APP_SECRET environment variable is not set.")
        print("NOTE: This is only needed for direct Meta authentication. Pipeboard authentication doesn't require this.")
        print("RECOMMENDED: Use Pipeboard authentication by setting PIPEBOARD_API_TOKEN instead.")

# Configure logging to file
def setup_logging():
    """Set up logging to file for troubleshooting."""
    # Get platform-specific path for logs
    if platform.system() == "Windows":
        base_path = pathlib.Path(os.environ.get("APPDATA", ""))
    elif platform.system() == "Darwin":  # macOS
        base_path = pathlib.Path.home() / "Library" / "Application Support"
    else:  # Assume Linux/Unix
        base_path = pathlib.Path.home() / ".config"
    
    # Create directory if it doesn't exist
    log_dir = base_path / "meta-ads-mcp"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / "meta_ads_debug.log"
    
    # Configure file logger
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=str(log_file),
        filemode='a'  # Append mode
    )
    
    # Create a logger
    logger = logging.getLogger("meta-ads-mcp")
    logger.setLevel(logging.DEBUG)
    
    # Log startup information
    logger.info(f"Logging initialized. Log file: {log_file}")
    logger.info(f"Platform: {platform.system()} {platform.release()}")
    logger.info(f"Using Pipeboard authentication: {using_pipeboard}")
    
    return logger

# Create the logger instance to be imported by other modules
logger = setup_logging()

# Global store for ad creative images
ad_creative_images = {}

async def download_image(url: str) -> Optional[bytes]:
    """
    Download an image from a URL.
    
    Args:
        url: Image URL
        
    Returns:
        Image data as bytes if successful, None otherwise
    """
    try:
        print(f"Attempting to download image from URL: {url}")
        
        # Use minimal headers like curl does
        headers = {
            "User-Agent": "curl/8.4.0",
            "Accept": "*/*"
        }
        
        async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
            # Simple GET request just like curl
            response = await client.get(url, headers=headers)
            
            # Check response
            if response.status_code == 200:
                print(f"Successfully downloaded image: {len(response.content)} bytes")
                return response.content
            else:
                print(f"Failed to download image: HTTP {response.status_code}")
                return None
                
    except httpx.HTTPStatusError as e:
        print(f"HTTP Error when downloading image: {e}")
        return None
    except httpx.RequestError as e:
        print(f"Request Error when downloading image: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error downloading image: {e}")
        return None


async def try_multiple_download_methods(url: str) -> Optional[bytes]:
    """
    Try multiple methods to download an image, with different approaches for Meta CDN.
    
    Args:
        url: Image URL
        
    Returns:
        Image data as bytes if successful, None otherwise
    """
    # Method 1: Direct download with custom headers
    image_data = await download_image(url)
    if image_data:
        return image_data
    
    print("Direct download failed, trying alternative methods...")
    
    # Method 2: Try adding Facebook cookie simulation
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
            "Cookie": "presence=EDvF3EtimeF1697900316EuserFA21B00112233445566AA0EstateFDutF0CEchF_7bCC"  # Fake cookie
        }
        
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            print(f"Method 2 succeeded with cookie simulation: {len(response.content)} bytes")
            return response.content
    except Exception as e:
        print(f"Method 2 failed: {str(e)}")
    
    # Method 3: Try with session that keeps redirects and cookies
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            # First visit Facebook to get cookies
            await client.get("https://www.facebook.com/", timeout=30.0)
            # Then try the image URL
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            print(f"Method 3 succeeded with Facebook session: {len(response.content)} bytes")
            return response.content
    except Exception as e:
        print(f"Method 3 failed: {str(e)}")
    
    return None


def extract_creative_image_urls(creative: Dict[str, Any]) -> Dict[str, str]:
    """
    Extrae las URLs de imagen disponibles de un objeto de creatividad publicitaria.

    Args:
        creative: El diccionario que representa la creatividad de un anuncio.

    Returns:
        Un diccionario que contiene las URLs encontradas (thumbnail y/o principal).
    """
    image_urls = {}
    
    # Extraer la URL de la miniatura si existe
    if 'thumbnail_url' in creative and creative['thumbnail_url']:
        image_urls['thumbnail'] = creative['thumbnail_url']
        
    # Extraer la URL de la imagen principal si existe
    if 'image_url' in creative and creative['image_url']:
        image_urls['main_image'] = creative['image_url']
        
    # También se puede buscar en object_story_spec, que es una ubicación común
    if 'object_story_spec' in creative:
        link_data = creative['object_story_spec'].get('link_data', {})
        # A veces la URL está aquí en lugar de en el nivel superior
        if 'image_url' in link_data and link_data['image_url'] and 'main_image' not in image_urls:
            image_urls['main_image'] = link_data['image_url']
            
    return image_urls
    
def create_resource_from_image(image_bytes: bytes, resource_id: str, name: str) -> Dict[str, Any]:
    """
    Create a resource entry from image bytes.
    
    Args:
        image_bytes: Raw image data
        resource_id: Unique identifier for the resource
        name: Human-readable name for the resource
        
    Returns:
        Dictionary with resource information
    """
    ad_creative_images[resource_id] = {
        "data": image_bytes,
        "mime_type": "image/jpeg",
        "name": name
    }
    
    return {
        "resource_id": resource_id,
        "resource_uri": f"meta-ads://images/{resource_id}",
        "name": name,
        "size": len(image_bytes)
    } 
