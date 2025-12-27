# models/custom_api_model.py
"""
Custom API Model for external vision model integration.
Supports any vision API that accepts images and returns text descriptions.
"""
from typing import Tuple, Optional, Dict, Any, List
import logging
import base64
import json
from pathlib import Path
from PIL import Image
import io

from models.base_model import BaseVisionModel

logger = logging.getLogger(__name__)


class CustomAPIModel(BaseVisionModel):
    """
    Custom API model that connects to external vision APIs.
    Supports configuration via URL and API key.
    """
    
    def __init__(self, api_url: str, api_key: str, model_name: str = "custom", 
                 request_format: str = "openai", device=None):
        """
        Initialize custom API model.
        
        Args:
            api_url: The API endpoint URL
            api_key: API authentication key
            model_name: Display name for the model
            request_format: API format ('openai', 'anthropic', 'generic')
            device: Device for any local preprocessing (default: auto-detect)
        """
        self.api_url = api_url
        self.api_key = api_key
        self.custom_model_name = model_name
        self.request_format = request_format
        
        # Initialize base class
        super().__init__(device=device)
        
        logger.info(f"Initialized CustomAPIModel: {model_name} at {api_url}")
    
    def _get_model_name(self) -> str:
        """Return model name for template system."""
        return "custom"
    
    def _setup_model(self) -> None:
        """Setup model - for API models, we just validate connectivity."""
        try:
            import requests
            self.requests = requests
            logger.info("HTTP client initialized for custom API model")
        except ImportError:
            raise ImportError(
                "requests library required for custom API models. "
                "Install with: pip install requests"
            )
    
    def _encode_image_to_base64(self, image_path: str) -> str:
        """Encode image to base64 string."""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize if too large (max 2048px on longest side)
                max_size = 2048
                if max(img.size) > max_size:
                    ratio = max_size / max(img.size)
                    new_size = tuple(int(dim * ratio) for dim in img.size)
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                # Convert to base64
                buffered = io.BytesIO()
                img.save(buffered, format="JPEG", quality=95)
                img_bytes = buffered.getvalue()
                img_base64 = base64.b64encode(img_bytes).decode('utf-8')
                
                return img_base64
        except Exception as e:
            logger.error(f"Error encoding image {image_path}: {e}")
            raise
    
    def _build_request_payload(self, image_path: str, prompt: str) -> Dict[str, Any]:
        """Build API request payload based on format."""
        image_base64 = self._encode_image_to_base64(image_path)
        
        if self.request_format == "openai":
            # OpenAI Vision API format
            return {
                "model": self.custom_model_name or "gpt-4-vision-preview",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 1000
            }
        elif self.request_format == "anthropic":
            # Anthropic Claude API format
            return {
                "model": self.custom_model_name or "claude-3-opus-20240229",
                "max_tokens": 1024,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image_base64
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            }
        else:
            # Generic format - simple JSON structure
            return {
                "image": image_base64,
                "prompt": prompt,
                "max_tokens": 1000
            }
    
    def _extract_response_text(self, response_json: Dict[str, Any]) -> str:
        """Extract text from API response based on format."""
        try:
            if self.request_format == "openai":
                return response_json["choices"][0]["message"]["content"]
            elif self.request_format == "anthropic":
                return response_json["content"][0]["text"]
            else:
                # Generic format - try common field names
                if "text" in response_json:
                    return response_json["text"]
                elif "response" in response_json:
                    return response_json["response"]
                elif "description" in response_json:
                    return response_json["description"]
                elif "caption" in response_json:
                    return response_json["caption"]
                else:
                    # Return the whole response as string if we can't find the field
                    return json.dumps(response_json)
        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"Error extracting response text: {e}")
            return json.dumps(response_json)
    
    def _make_api_request(self, image_path: str, prompt: str) -> str:
        """Make API request and return response text."""
        try:
            # Build request
            headers = {
                "Content-Type": "application/json"
            }
            
            # Add API key to headers based on format
            if self.request_format == "openai":
                headers["Authorization"] = f"Bearer {self.api_key}"
            elif self.request_format == "anthropic":
                headers["x-api-key"] = self.api_key
                headers["anthropic-version"] = "2023-06-01"
            else:
                # Generic format - try both common auth methods
                headers["Authorization"] = f"Bearer {self.api_key}"
                headers["X-API-Key"] = self.api_key
            
            payload = self._build_request_payload(image_path, prompt)
            
            # Make request
            logger.info(f"Making API request to {self.api_url}")
            response = self.requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            # Check for errors
            response.raise_for_status()
            
            # Parse response
            response_json = response.json()
            text = self._extract_response_text(response_json)
            
            return text
            
        except self.requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise RuntimeError(f"API request failed: {e}")
        except Exception as e:
            logger.error(f"Error in API request: {e}")
            raise
    
    def analyze_image(self, image_path: str, quality: str = "standard", 
                     template_name: Optional[str] = None,
                     template_variables: Optional[Dict[str, Any]] = None) -> Tuple[str, Optional[str]]:
        """
        Analyze an image using the custom API.
        
        Args:
            image_path: Path to the image file
            quality: Quality level for template selection
            template_name: Specific template to use
            template_variables: Variables for template substitution
            
        Returns:
            Tuple[str, Optional[str]]: (description, clean_caption)
        """
        try:
            # Get prompt from template system
            prompt = self.get_prompt_from_template(
                quality=quality,
                template_name=template_name,
                template_variables=template_variables
            )
            
            # Make API request
            description = self._make_api_request(image_path, prompt)
            
            # Clean output
            clean_caption = self.clean_output(description)
            
            logger.info(f"Successfully analyzed image: {image_path}")
            return description, clean_caption
            
        except Exception as e:
            logger.error(f"Error analyzing image {image_path}: {e}")
            error_msg = f"Error: Failed to analyze image - {str(e)}"
            return error_msg, None
    
    def analyze_images_batch(self, image_paths: List[str], quality: str = "standard",
                            template_name: Optional[str] = None,
                            template_variables: Optional[Dict[str, Any]] = None) -> List[Tuple[str, Optional[str]]]:
        """
        Analyze multiple images in batch.
        
        Args:
            image_paths: List of image file paths
            quality: Quality level for template selection
            template_name: Specific template to use
            template_variables: Variables for template substitution
            
        Returns:
            List of (description, clean_caption) tuples
        """
        results = []
        for image_path in image_paths:
            try:
                result = self.analyze_image(
                    image_path,
                    quality=quality,
                    template_name=template_name,
                    template_variables=template_variables
                )
                results.append(result)
            except Exception as e:
                logger.error(f"Error in batch processing for {image_path}: {e}")
                results.append((f"Error: {str(e)}", None))
        
        return results
    
    def _get_legacy_prompt(self, quality: str) -> str:
        """Get legacy prompt for backward compatibility."""
        if quality == "detailed":
            return "Provide a detailed description of this image including all objects, colors, composition, and any text visible."
        elif quality == "creative":
            return "Create an artistic and evocative description of this image, capturing its mood and aesthetic qualities."
        else:  # standard
            return "Generate a clear and concise caption for this image."
