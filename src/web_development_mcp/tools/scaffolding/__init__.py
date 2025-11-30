"""
Scaffolding module for creating project templates.

This package contains framework-specific scaffolding implementations.
"""

from pathlib import Path
from typing import Dict, Any, Protocol, Optional, List
import logging

logger = logging.getLogger(__name__)

class FrameworkScaffolder(Protocol):
    """Protocol for framework-specific scaffolding implementations."""
    
    @staticmethod
    def create_project(project_name: str, project_path: Path, options: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new project with the given framework.
        
        Args:
            project_name: Name of the project
            project_path: Path where the project should be created
            options: Framework-specific options
            
        Returns:
            Dict containing project creation results
        """
        ...
    
    @staticmethod
    def validate_options(options: Dict[str, Any]) -> List[str]:
        """Validate framework-specific options.
        
        Args:
            options: Options to validate
            
        Returns:
            List of validation errors, empty if valid
        """
        return []

# Import framework implementations
from .frameworks.react import ReactScaffolder
from .frameworks.vue import VueScaffolder
from .frameworks.sveltekit import SvelteKitScaffolder

def get_available_frameworks() -> Dict[str, Dict[str, Any]]:
    """Get information about all available frameworks.
    
    Returns:
        Dict mapping framework IDs to framework information
    """
    return {
        "react": {
            "name": "React",
            "description": "Popular component-based UI library",
            "features": ["TypeScript", "Vite", "React Router", "Testing Library", "ESLint"],
            "use_cases": ["SPAs", "Component libraries", "Complex UIs"],
            "popularity": "Most popular",
            "learning_curve": "Moderate",
            "scaffolder": ReactScaffolder
        },
        "vue": {
            "name": "Vue 3",
            "description": "Progressive JavaScript framework",
            "features": ["TypeScript", "Vite", "Vue Router", "Pinia", "ESLint"],
            "use_cases": ["SPAs", "Progressive web apps", "Quick prototypes"],
            "popularity": "Very popular",
            "learning_curve": "Easy",
            "scaffolder": VueScaffolder
        },
        "sveltekit": {
            "name": "SvelteKit",
            "description": "Compile-time optimized framework",
            "features": ["TypeScript", "Vite", "SvelteKit routing", "Built-in state", "ESLint"],
            "use_cases": ["Performance-critical apps", "Small bundles", "SSR"],
            "popularity": "Growing fast",
            "learning_curve": "Easy",
            "scaffolder": SvelteKitScaffolder
        },
        "next": {
            "name": "Next.js",
            "description": "Full-stack React framework",
            "features": ["TypeScript", "App Router", "Server components", "API routes", "ESLint"],
            "use_cases": ["Full-stack apps", "SSR/SSG", "E-commerce"],
            "popularity": "Very popular",
            "learning_curve": "Moderate",
            "scaffolder": None  # Not implemented yet
        },
        "vanilla": {
            "name": "Vanilla TypeScript",
            "description": "Modern TypeScript with Vite",
            "features": ["TypeScript", "Vite", "ESM", "Hot reload", "ESLint"],
            "use_cases": ["Libraries", "Learning", "Custom solutions"],
            "popularity": "Foundation",
            "learning_curve": "Easy",
            "scaffolder": None  # Not implemented yet
        }
    }
