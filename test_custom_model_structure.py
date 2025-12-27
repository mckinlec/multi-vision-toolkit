#!/usr/bin/env python3
"""
Simplified test script for custom API model - checks code structure only.
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
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_template_system():
    """Test that custom model is integrated with template system."""
    logger.info("Testing template system integration...")
    
    try:
        from templates.template_manager import TemplateManager, ModelNames, VALID_MODEL_NAMES
        
        # Check that custom is in valid model names
        if ModelNames.CUSTOM not in VALID_MODEL_NAMES:
            logger.error("FAIL: CUSTOM not in VALID_MODEL_NAMES")
            return False
        logger.info("PASS: CUSTOM is in VALID_MODEL_NAMES")
        
        # Create template manager
        tm = TemplateManager()
        
        # Get templates for custom model
        templates = tm.get_model_templates("custom")
        logger.info(f"PASS: Found {len(templates)} templates for custom model")
        
        if templates:
            for name in sorted(templates.keys()):
                logger.info(f"  - {name}")
        
        # Test rendering a template
        rendered = tm.render_template("custom", "caption_standard", {"trigger_word": " <test>"})
        if rendered:
            logger.info(f"PASS: Successfully rendered template")
        else:
            logger.warning("WARNING: Template rendering returned None")
        
        return True
    except Exception as e:
        logger.error(f"FAIL: Template system test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_code_structure():
    """Verify that key files exist and have correct structure."""
    logger.info("Testing code structure...")
    
    base_dir = Path(__file__).parent
    
    # Check that custom_api_model.py exists
    custom_model_file = base_dir / "models" / "custom_api_model.py"
    if not custom_model_file.exists():
        logger.error(f"FAIL: {custom_model_file} does not exist")
        return False
    logger.info(f"PASS: {custom_model_file} exists")
    
    # Check that custom_model_dialog.py exists
    dialog_file = base_dir / "custom_model_dialog.py"
    if not dialog_file.exists():
        logger.error(f"FAIL: {dialog_file} does not exist")
        return False
    logger.info(f"PASS: {dialog_file} exists")
    
    # Check that main.py has custom-api in model list
    main_file = base_dir / "main.py"
    with open(main_file, 'r') as f:
        main_content = f.read()
    
    if 'custom-api' not in main_content:
        logger.error("FAIL: 'custom-api' not found in main.py")
        return False
    logger.info("PASS: 'custom-api' found in main.py")
    
    if 'CustomAPIModel' not in main_content:
        logger.error("FAIL: 'CustomAPIModel' not found in main.py")
        return False
    logger.info("PASS: 'CustomAPIModel' reference found in main.py")
    
    if 'custom_model_config' not in main_content:
        logger.error("FAIL: 'custom_model_config' not found in main.py")
        return False
    logger.info("PASS: 'custom_model_config' found in main.py")
    
    # Check requirements.txt has requests
    req_file = base_dir / "requirements.txt"
    with open(req_file, 'r') as f:
        req_content = f.read()
    
    if 'requests' not in req_content:
        logger.error("FAIL: 'requests' not found in requirements.txt")
        return False
    logger.info("PASS: 'requests' found in requirements.txt")
    
    return True

def test_custom_model_file_structure():
    """Check that custom model file has correct class structure."""
    logger.info("Testing custom model file structure...")
    
    custom_model_file = Path(__file__).parent / "models" / "custom_api_model.py"
    
    with open(custom_model_file, 'r') as f:
        content = f.read()
    
    required_elements = [
        'class CustomAPIModel',
        'BaseVisionModel',
        'def __init__',
        'def analyze_image',
        'def analyze_images_batch',
        'def _get_model_name',
        'def _make_api_request',
        'api_url',
        'api_key',
        'request_format'
    ]
    
    all_found = True
    for element in required_elements:
        if element in content:
            logger.info(f"PASS: Found '{element}'")
        else:
            logger.error(f"FAIL: Missing '{element}'")
            all_found = False
    
    return all_found

def test_dialog_file_structure():
    """Check that dialog file has correct class structure."""
    logger.info("Testing dialog file structure...")
    
    dialog_file = Path(__file__).parent / "custom_model_dialog.py"
    
    with open(dialog_file, 'r') as f:
        content = f.read()
    
    required_elements = [
        'class CustomModelDialog',
        'class CustomModelManager',
        'def show',
        'def test_connection',
        'def on_save',
        'url_var',
        'key_var',
        'format_var'
    ]
    
    all_found = True
    for element in required_elements:
        if element in content:
            logger.info(f"PASS: Found '{element}'")
        else:
            logger.error(f"FAIL: Missing '{element}'")
            all_found = False
    
    return all_found

def main():
    """Run all tests."""
    logger.info("="*60)
    logger.info("Custom API Model Code Structure Test")
    logger.info("="*60)
    
    results = {
        "Code Structure": test_code_structure(),
        "Custom Model File": test_custom_model_file_structure(),
        "Dialog File": test_dialog_file_structure(),
        "Template System": test_template_system(),
    }
    
    logger.info("\n" + "="*60)
    logger.info("Test Results Summary")
    logger.info("="*60)
    
    for test_name, result in results.items():
        status = "PASS ✓" if result else "FAIL ✗"
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
