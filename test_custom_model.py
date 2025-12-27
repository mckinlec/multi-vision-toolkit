#!/usr/bin/env python3
"""
Test script for custom API model functionality.
"""
import sys
import os
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all required modules can be imported."""
    logger.info("Testing imports...")
    
    try:
        from models.custom_api_model import CustomAPIModel
        logger.info("✓ CustomAPIModel imported successfully")
    except Exception as e:
        logger.error(f"✗ Failed to import CustomAPIModel: {e}")
        return False
    
    try:
        from custom_model_dialog import CustomModelDialog, CustomModelManager
        logger.info("✓ CustomModelDialog imported successfully")
    except Exception as e:
        logger.error(f"✗ Failed to import CustomModelDialog: {e}")
        return False
    
    try:
        from templates.template_manager import TemplateManager, ModelNames
        logger.info("✓ TemplateManager imported successfully")
        logger.info(f"  Valid model names: {', '.join(sorted(ModelNames.__dict__.keys() if hasattr(ModelNames, '__dict__') else []))}")
    except Exception as e:
        logger.error(f"✗ Failed to import TemplateManager: {e}")
        return False
    
    return True

def test_custom_model_instantiation():
    """Test that CustomAPIModel can be instantiated."""
    logger.info("\nTesting CustomAPIModel instantiation...")
    
    try:
        from models.custom_api_model import CustomAPIModel
        
        # Create a test instance (won't actually connect)
        model = CustomAPIModel(
            api_url="https://api.example.com/v1/chat/completions",
            api_key="test_key_12345",
            model_name="test-model",
            request_format="openai"
        )
        logger.info("✓ CustomAPIModel instantiated successfully")
        logger.info(f"  Model name: {model.custom_model_name}")
        logger.info(f"  API URL: {model.api_url}")
        logger.info(f"  Request format: {model.request_format}")
        
        # Test that it has required methods
        assert hasattr(model, 'analyze_image'), "Missing analyze_image method"
        assert hasattr(model, 'analyze_images_batch'), "Missing analyze_images_batch method"
        assert hasattr(model, '_get_model_name'), "Missing _get_model_name method"
        logger.info("✓ CustomAPIModel has all required methods")
        
        # Test template system integration
        model_name = model._get_model_name()
        logger.info(f"✓ Model name for templates: {model_name}")
        
        return True
    except Exception as e:
        logger.error(f"✗ Failed to instantiate CustomAPIModel: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_template_system():
    """Test that custom model is integrated with template system."""
    logger.info("\nTesting template system integration...")
    
    try:
        from templates.template_manager import TemplateManager, ModelNames, VALID_MODEL_NAMES
        
        # Check that custom is in valid model names
        if ModelNames.CUSTOM not in VALID_MODEL_NAMES:
            logger.error("✗ CUSTOM not in VALID_MODEL_NAMES")
            return False
        logger.info("✓ CUSTOM is in VALID_MODEL_NAMES")
        
        # Create template manager
        tm = TemplateManager()
        
        # Get templates for custom model
        templates = tm.get_model_templates("custom")
        logger.info(f"✓ Found {len(templates)} templates for custom model")
        
        if templates:
            logger.info("  Available templates:")
            for name in sorted(templates.keys()):
                logger.info(f"    - {name}")
        
        # Test rendering a template
        rendered = tm.render_template("custom", "caption_standard", {"trigger_word": " <test>"})
        if rendered:
            logger.info(f"✓ Successfully rendered template: {rendered}")
        else:
            logger.warning("⚠ Template rendering returned None")
        
        return True
    except Exception as e:
        logger.error(f"✗ Failed template system test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_model_manager():
    """Test ModelManager integration."""
    logger.info("\nTesting ModelManager integration...")
    
    try:
        # We can't fully test this without running the full app,
        # but we can check the code changes
        import main
        
        # Check that ModelManager has custom_model_config attribute
        model_manager = main.ModelManager()
        assert hasattr(model_manager, 'custom_model_config'), "ModelManager missing custom_model_config"
        logger.info("✓ ModelManager has custom_model_config attribute")
        
        # Check initial value
        assert model_manager.custom_model_config is None, "custom_model_config should start as None"
        logger.info("✓ custom_model_config initialized to None")
        
        return True
    except Exception as e:
        logger.error(f"✗ Failed ModelManager test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_request_building():
    """Test API request payload building."""
    logger.info("\nTesting API request payload building...")
    
    try:
        from models.custom_api_model import CustomAPIModel
        
        # Test different formats
        formats = ["openai", "anthropic", "generic"]
        
        for fmt in formats:
            logger.info(f"  Testing {fmt} format...")
            model = CustomAPIModel(
                api_url="https://api.example.com/v1/chat/completions",
                api_key="test_key",
                model_name="test-model",
                request_format=fmt
            )
            
            # We can't build actual payloads without test images,
            # but we can verify the format is stored
            assert model.request_format == fmt
            logger.info(f"  ✓ {fmt} format set correctly")
        
        return True
    except Exception as e:
        logger.error(f"✗ Failed request building test: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    logger.info("="*60)
    logger.info("Custom API Model Test Suite")
    logger.info("="*60)
    
    results = {
        "Imports": test_imports(),
        "Model Instantiation": test_custom_model_instantiation(),
        "Template System": test_template_system(),
        "Model Manager": test_model_manager(),
        "Request Building": test_request_building(),
    }
    
    logger.info("\n" + "="*60)
    logger.info("Test Results Summary")
    logger.info("="*60)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{test_name:.<40} {status}")
    
    all_passed = all(results.values())
    logger.info("="*60)
    
    if all_passed:
        logger.info("All tests passed! ✓")
        return 0
    else:
        logger.error("Some tests failed! ✗")
        return 1

if __name__ == "__main__":
    sys.exit(main())
