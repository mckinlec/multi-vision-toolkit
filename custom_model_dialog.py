# custom_model_dialog.py
"""
Dialog for configuring custom API vision models.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class CustomModelDialog:
    """Dialog for configuring custom API model settings."""
    
    def __init__(self, parent, existing_config: Optional[Dict[str, Any]] = None):
        """
        Initialize the custom model configuration dialog.
        
        Args:
            parent: Parent tkinter window
            existing_config: Existing configuration to edit (optional)
        """
        self.parent = parent
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Configure Custom Vision Model")
        self.dialog.geometry("600x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"600x500+{x}+{y}")
        
        self.setup_ui()
        
        # Load existing config if provided
        if existing_config:
            self.load_config(existing_config)
        
        # Make dialog modal
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_cancel)
        self.dialog.focus_set()
    
    def setup_ui(self):
        """Setup the dialog UI."""
        # Main container with padding
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Custom Vision Model Configuration",
            font=("Segoe UI", 14, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Form frame
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Model Name
        ttk.Label(form_frame, text="Model Name:").grid(row=0, column=0, sticky="w", pady=5)
        self.name_var = tk.StringVar(value="Custom Model")
        name_entry = ttk.Entry(form_frame, textvariable=self.name_var, width=40)
        name_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        ttk.Label(
            form_frame, 
            text="Display name for this model",
            font=("Segoe UI", 8),
            foreground="gray"
        ).grid(row=1, column=1, sticky="w", padx=(10, 0))
        
        # API URL
        ttk.Label(form_frame, text="API URL:").grid(row=2, column=0, sticky="w", pady=5)
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(form_frame, textvariable=self.url_var, width=40)
        url_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        ttk.Label(
            form_frame, 
            text="Full endpoint URL (e.g., https://api.example.com/v1/chat/completions)",
            font=("Segoe UI", 8),
            foreground="gray"
        ).grid(row=3, column=1, sticky="w", padx=(10, 0))
        
        # API Key
        ttk.Label(form_frame, text="API Key:").grid(row=4, column=0, sticky="w", pady=5)
        self.key_var = tk.StringVar()
        key_entry = ttk.Entry(form_frame, textvariable=self.key_var, width=40, show="*")
        key_entry.grid(row=4, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Show/hide API key checkbox
        self.show_key_var = tk.BooleanVar(value=False)
        show_key_check = ttk.Checkbutton(
            form_frame,
            text="Show API Key",
            variable=self.show_key_var,
            command=lambda: key_entry.config(show="" if self.show_key_var.get() else "*")
        )
        show_key_check.grid(row=5, column=1, sticky="w", padx=(10, 0))
        
        # API Format
        ttk.Label(form_frame, text="API Format:").grid(row=6, column=0, sticky="w", pady=5)
        self.format_var = tk.StringVar(value="openai")
        format_combo = ttk.Combobox(
            form_frame,
            textvariable=self.format_var,
            values=["openai", "anthropic", "generic"],
            state="readonly",
            width=37
        )
        format_combo.grid(row=6, column=1, sticky="ew", pady=5, padx=(10, 0))
        ttk.Label(
            form_frame, 
            text="openai: OpenAI/compatible APIs | anthropic: Claude API | generic: Custom format",
            font=("Segoe UI", 8),
            foreground="gray"
        ).grid(row=7, column=1, sticky="w", padx=(10, 0))
        
        # Model ID (optional)
        ttk.Label(form_frame, text="Model ID (optional):").grid(row=8, column=0, sticky="w", pady=5)
        self.model_id_var = tk.StringVar()
        model_id_entry = ttk.Entry(form_frame, textvariable=self.model_id_var, width=40)
        model_id_entry.grid(row=8, column=1, sticky="ew", pady=5, padx=(10, 0))
        ttk.Label(
            form_frame, 
            text="Specific model identifier to use (e.g., gpt-4-vision-preview)",
            font=("Segoe UI", 8),
            foreground="gray"
        ).grid(row=9, column=1, sticky="w", padx=(10, 0))
        
        # Configure grid weights
        form_frame.columnconfigure(1, weight=1)
        
        # Test connection button
        test_frame = ttk.Frame(main_frame)
        test_frame.pack(fill=tk.X, pady=(20, 10))
        
        self.test_button = ttk.Button(
            test_frame,
            text="Test Connection",
            command=self.test_connection
        )
        self.test_button.pack(side=tk.LEFT)
        
        self.test_status_label = ttk.Label(test_frame, text="")
        self.test_status_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(
            button_frame,
            text="Cancel",
            command=self.on_cancel
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Save",
            command=self.on_save
        ).pack(side=tk.RIGHT)
    
    def load_config(self, config: Dict[str, Any]):
        """Load existing configuration into the form."""
        self.name_var.set(config.get("name", "Custom Model"))
        self.url_var.set(config.get("url", ""))
        self.key_var.set(config.get("api_key", ""))
        self.format_var.set(config.get("format", "openai"))
        self.model_id_var.set(config.get("model_id", ""))
    
    def test_connection(self):
        """Test the API connection."""
        url = self.url_var.get().strip()
        api_key = self.key_var.get().strip()
        
        if not url:
            messagebox.showwarning("Missing Information", "Please enter an API URL")
            return
        
        if not api_key:
            messagebox.showwarning("Missing Information", "Please enter an API Key")
            return
        
        # Update status
        self.test_status_label.config(text="Testing...", foreground="blue")
        self.test_button.config(state="disabled")
        self.dialog.update()
        
        try:
            import requests
            
            # Simple test request (just check if endpoint is reachable)
            headers = {"Authorization": f"Bearer {api_key}"}
            
            # Try a simple HEAD or OPTIONS request first
            try:
                response = requests.options(url, headers=headers, timeout=5)
                success = response.status_code < 500
            except:
                # If OPTIONS fails, try a minimal POST
                try:
                    response = requests.post(
                        url,
                        headers=headers,
                        json={"test": "connection"},
                        timeout=5
                    )
                    success = response.status_code != 404
                except:
                    success = False
            
            if success:
                self.test_status_label.config(text="✓ Connection successful", foreground="green")
                messagebox.showinfo(
                    "Connection Test",
                    "Connection test successful! The API endpoint is reachable."
                )
            else:
                self.test_status_label.config(text="⚠ Connection may have issues", foreground="orange")
                messagebox.showwarning(
                    "Connection Test",
                    "Could not fully verify the connection. The endpoint may not be configured correctly."
                )
                
        except ImportError:
            messagebox.showerror(
                "Missing Dependency",
                "The 'requests' library is required for custom API models.\n\n"
                "Install with: pip install requests"
            )
            self.test_status_label.config(text="✗ Missing dependency", foreground="red")
        except Exception as e:
            self.test_status_label.config(text="✗ Connection failed", foreground="red")
            messagebox.showerror(
                "Connection Test Failed",
                f"Failed to connect to the API:\n\n{str(e)}\n\n"
                "Please check your URL and API key."
            )
        finally:
            self.test_button.config(state="normal")
    
    def on_save(self):
        """Save the configuration."""
        name = self.name_var.get().strip()
        url = self.url_var.get().strip()
        api_key = self.key_var.get().strip()
        format_type = self.format_var.get()
        model_id = self.model_id_var.get().strip()
        
        # Validate inputs
        if not name:
            messagebox.showwarning("Missing Information", "Please enter a model name")
            return
        
        if not url:
            messagebox.showwarning("Missing Information", "Please enter an API URL")
            return
        
        if not api_key:
            messagebox.showwarning("Missing Information", "Please enter an API Key")
            return
        
        # Validate URL format
        if not (url.startswith("http://") or url.startswith("https://")):
            messagebox.showwarning(
                "Invalid URL",
                "API URL must start with http:// or https://"
            )
            return
        
        # Build result
        self.result = {
            "name": name,
            "url": url,
            "api_key": api_key,
            "format": format_type,
            "model_id": model_id if model_id else None
        }
        
        self.dialog.destroy()
    
    def on_cancel(self):
        """Cancel the dialog."""
        self.result = None
        self.dialog.destroy()
    
    def show(self) -> Optional[Dict[str, Any]]:
        """Show the dialog and return the result."""
        self.parent.wait_window(self.dialog)
        return self.result


class CustomModelManager:
    """Manages saved custom model configurations."""
    
    def __init__(self, config_file: str = "custom_models.json"):
        """Initialize the custom model manager."""
        self.config_file = Path(config_file)
        self.configs = self.load_configs()
    
    def load_configs(self) -> Dict[str, Dict[str, Any]]:
        """Load saved configurations from file."""
        if not self.config_file.exists():
            return {}
        
        try:
            with open(self.config_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading custom model configs: {e}")
            return {}
    
    def save_configs(self):
        """Save configurations to file."""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.configs, f, indent=2)
            logger.info(f"Saved custom model configs to {self.config_file}")
        except Exception as e:
            logger.error(f"Error saving custom model configs: {e}")
    
    def add_config(self, name: str, config: Dict[str, Any]):
        """Add or update a configuration."""
        self.configs[name] = config
        self.save_configs()
    
    def get_config(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a configuration by name."""
        return self.configs.get(name)
    
    def delete_config(self, name: str):
        """Delete a configuration."""
        if name in self.configs:
            del self.configs[name]
            self.save_configs()
    
    def list_configs(self) -> list:
        """List all configuration names."""
        return list(self.configs.keys())
