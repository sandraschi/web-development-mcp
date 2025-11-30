"""
Integrated Vue 3 project scaffolding implementation.

This module combines all Vue 3 scaffolding functionality into a single module.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import shutil

logger = logging.getLogger(__name__)

class VueScaffolder:
    """Integrated scaffolder implementation for Vue 3 projects."""
    
    @staticmethod
    def create_project(project_name: str, project_path: Path, options: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new Vue 3 project.
        
        Args:
            project_name: Name of the project
            project_path: Path where the project should be created
            options: Project configuration options
            
        Returns:
            Dict containing project creation results
        """
        try:
            # Import and use the component classes
            from .vue_scaffolder_part1 import VueScaffolder as VueScaffolderPart1
            from .vue_scaffolder_part2 import VueScaffolderConfigs
            from .vue_scaffolder_part3 import VueScaffolderComponents
            
            # Create project structure
            VueScaffolderPart1._create_project_structure(project_path, options)
            
            # Create package.json
            VueScaffolderPart1._create_package_json(project_name, project_path, options)
            
            # Create config files
            VueScaffolderConfigs.create_config_files(project_path, options)
            
            # Create components and other project files
            VueScaffolderComponents.create_components(project_path, options)
            
            return {
                "success": True,
                "project_name": project_name,
                "project_path": str(project_path),
                "framework": "vue",
                "features_included": [
                    "Vue 3",
                    "TypeScript",
                    "Vite",
                    "Vue Router" if options.get("router", True) else None,
                    "Pinia" if options.get("pinia", True) else None,
                    "Testing" if options.get("testing", True) else None,
                    "ESLint" + (" (strict)" if options.get("eslint_strict", False) else ""),
                    "Prettier" if options.get("prettier", True) else None,
                ],
                "next_steps": [
                    f"cd {project_path}",
                    "npm install",
                    "npm run dev"
                ]
            }
            
        except Exception as e:
            logger.error(f"Error creating Vue app: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def validate_options(options: Dict[str, Any]) -> List[str]:
        """Validate Vue project options.
        
        Args:
            options: Options to validate
            
        Returns:
            List of validation errors, empty if valid
        """
        errors = []
        # Add any Vue-specific validation here
        return errors
