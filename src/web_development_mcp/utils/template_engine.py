"""
Template engine utilities for the Web Development MCP.

Provides functions for processing templates with variable substitution using Jinja2.
"""

import fnmatch
import json
import logging
import os
import shutil
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union

from jinja2 import (
    Environment,
    FileSystemLoader,
    StrictUndefined,
    TemplateError,
    TemplateNotFound,
    TemplateSyntaxError,
    select_autoescape,
)
from jinja2.ext import Extension

# Configure logger
logger = logging.getLogger(__name__)

# Type variable for template context
T = TypeVar("T", bound="TemplateContext")


@dataclass
class TemplateContext:
    """
    Context for template rendering with additional metadata and helper methods.

    Attributes:
        variables: Dictionary of variables available in the template
        source_path: Path to the source template file (optional)
        target_path: Path where the rendered output will be saved (optional)
        metadata: Additional metadata about the template processing
    """

    variables: Dict[str, Any]
    source_path: Optional[Path] = None
    target_path: Optional[Path] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def update(self, **kwargs) -> None:
        """Update the context variables with new values."""
        self.variables.update(kwargs)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the context to a dictionary."""
        return {
            "variables": self.variables,
            "source_path": str(self.source_path) if self.source_path else None,
            "target_path": str(self.target_path) if self.target_path else None,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Create a TemplateContext from a dictionary."""
        return cls(
            variables=data.get("variables", {}),
            source_path=Path(data["source_path"]) if data.get("source_path") else None,
            target_path=Path(data["target_path"]) if data.get("target_path") else None,
            metadata=data.get("metadata", {}),
        )

    def __str__(self) -> str:
        """Return a string representation of the context."""
        return json.dumps(self.to_dict(), indent=2)


class TemplateEngine:
    """
    Advanced template engine for processing template files with Jinja2.

    This class provides a high-level interface for rendering templates with support for
    template inheritance, custom filters, global variables, and more.
    """

    def __init__(
        self,
        template_dirs: Optional[Union[str, Path, List[Union[str, Path]]]] = None,
        autoescape: bool = True,
        auto_reload: bool = False,
        cache_size: int = 50,
        extensions: Optional[List[Union[str, Type[Extension]]]] = None,
        **env_options,
    ):
        """Initialize the template engine.

        Args:
            template_dirs: Directory or list of directories containing templates.
            autoescape: Whether to enable auto-escaping of variables (default: True).
            auto_reload: Whether to reload templates if they change (default: False).
            cache_size: Maximum number of templates to keep in memory (default: 50).
            extensions: List of Jinja2 extensions to load.
            **env_options: Additional options to pass to the Jinja2 Environment.
        """
        if template_dirs is None:
            template_dirs = []
        elif isinstance(template_dirs, (str, Path)):
            template_dirs = [template_dirs]

        # Convert to Path objects and ensure they exist
        self.template_dirs = [Path(d).resolve() for d in template_dirs if Path(d).exists()]

        # Default Jinja2 environment options
        default_env_options = {
            "loader": FileSystemLoader([str(d) for d in self.template_dirs]),
            "undefined": StrictUndefined,
            "trim_blocks": True,
            "lstrip_blocks": True,
            "keep_trailing_newline": True,
            "autoescape": select_autoescape() if autoescape else False,
            "auto_reload": auto_reload,
            "cache_size": cache_size,
            "extensions": extensions or [],
        }

        # Update with any user-provided options
        default_env_options.update(env_options)

        # Initialize Jinja2 environment
        self.env = Environment(**default_env_options)

        # Register default filters and globals
        self._register_defaults()

    def _register_defaults(self) -> None:
        """Register default filters and globals."""
        # Default filters
        self.env.filters.update(
            {
                "to_json": json.dumps,
                "from_json": json.loads,
                "to_nice_json": lambda x, indent=2: json.dumps(x, indent=indent),
                "to_yaml": lambda x: str(x),  # Placeholder - would use PyYAML if available
                "from_yaml": lambda x: x,  # Placeholder
            }
        )

        # Default globals
        self.env.globals.update(
            {
                "now": self._get_current_time,
                "env": dict(os.environ),
            }
        )

    @staticmethod
    def _get_current_time(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Get current time formatted as a string."""
        from datetime import datetime

        return datetime.now().strftime(fmt)

    def add_filter(self, name: str, filter_func: Callable) -> None:
        """Add a custom filter to the template environment.

        Args:
            name: Name of the filter.
            filter_func: The filter function to add.
        """
        self.env.filters[name] = filter_func

    def add_global(self, name: str, value: Any) -> None:
        """Add a global variable to the template environment.

        Args:
            name: Name of the global variable.
            value: Value of the global variable.
        """
        self.env.globals[name] = value

    def add_template_dir(self, template_dir: Union[str, Path]) -> None:
        """Add a template directory to the search path.

        Args:
            template_dir: Directory containing templates.
        """
        template_dir = Path(template_dir).resolve()
        if template_dir.exists() and template_dir not in self.template_dirs:
            self.template_dirs.append(template_dir)
            # Update the loader's search path
            if hasattr(self.env.loader, "searchpath"):
                self.env.loader.searchpath.append(str(template_dir))
            else:
                logger.warning("Cannot update search path for current loader type")

    @lru_cache(maxsize=100)
    def get_template_info(self, template_name: str) -> Dict[str, Any]:
        """Get information about a template.

        Args:
            template_name: Name of the template.

        Returns:
            Dict containing template metadata.
        """
        try:
            template = self.env.get_template(template_name)
            return {
                "name": template.name,
                "filename": template.filename,
                "is_up_to_date": not template.should_reload,
                "variables": list(template.blocks.keys()) if hasattr(template, "blocks") else [],
            }
        except (TemplateNotFound, TemplateSyntaxError) as e:
            logger.error(f"Error getting template info for {template_name}: {e}")
            return {"error": str(e)}

    def render(self, template_name: str, context: Optional[Dict[str, Any]] = None, **kwargs) -> str:
        """Render a template with the given context.

        Args:
            template_name: Name of the template file to render.
            context: Dictionary of variables to pass to the template.
            **kwargs: Additional variables to pass to the template.

        Returns:
            str: Rendered template content.

        Raises:
            TemplateError: If there's an error rendering the template.
        """
        if context is None:
            context = {}

        # Merge additional keyword arguments into the context
        if kwargs:
            context.update(kwargs)

        try:
            template = self.env.get_template(template_name)
            return template.render(**context)
        except TemplateError as e:
            logger.error(f"Error rendering template {template_name}: {e}")
            raise

    def render_string(
        self, template_string: str, context: Optional[Dict[str, Any]] = None, **kwargs
    ) -> str:
        """Render a template string with the given context.

        Args:
            template_string: Template as a string.
            context: Dictionary of variables to pass to the template.
            **kwargs: Additional variables to pass to the template.

        Returns:
            str: Rendered template content.

        Raises:
            TemplateError: If there's an error rendering the template.
        """
        if context is None:
            context = {}

        # Merge additional keyword arguments into the context
        if kwargs:
            context.update(kwargs)

        try:
            template = self.env.from_string(template_string)
            return template.render(**context)
        except TemplateError as e:
            logger.error(f"Error rendering template string: {e}")
            raise

    def render_to_file(
        self,
        template_name: str,
        output_path: Union[str, Path],
        context: Optional[Dict[str, Any]] = None,
        encoding: str = "utf-8",
        **kwargs,
    ) -> Path:
        """Render a template and save it to a file.

        Args:
            template_name: Name of the template file to render.
            output_path: Path where the rendered template should be saved.
            context: Dictionary of variables to pass to the template.
            encoding: File encoding to use.
            **kwargs: Additional variables to pass to the template.

        Returns:
            Path: Path to the rendered file.

        Raises:
            TemplateError: If there's an error rendering the template.
            OSError: If there's an error writing the file.
        """
        if context is None:
            context = {}

        # Merge additional keyword arguments into the context
        if kwargs:
            context.update(kwargs)

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            rendered_content = self.render(template_name, context)

            # Create a backup if the file already exists
            if output_path.exists():
                backup_path = output_path.with_suffix(f"{output_path.suffix}.bak")
                shutil.copy2(output_path, backup_path)
                logger.debug(f"Created backup at {backup_path}")

            # Write the rendered content
            with open(output_path, "w", encoding=encoding) as f:
                f.write(rendered_content)

            logger.info(f"Rendered template to {output_path}")
            return output_path

        except (TemplateError, OSError) as e:
            logger.error(f"Error rendering template to {output_path}: {e}")
            raise

    def render_directory(
        self,
        template_dir: Union[str, Path],
        output_dir: Union[str, Path],
        context: Optional[Dict[str, Any]] = None,
        exclude: Optional[List[str]] = None,
        **kwargs,
    ) -> List[Path]:
        """Render all templates in a directory to an output directory.

        Args:
            template_dir: Directory containing template files.
            output_dir: Directory where rendered files should be saved.
            context: Variables to pass to all templates.
            exclude: List of file patterns to exclude.
            **kwargs: Additional variables to pass to the templates.

        Returns:
            List[Path]: Paths to the rendered files.
        """
        if context is None:
            context = {}
        if exclude is None:
            exclude = []

        template_dir = Path(template_dir)
        output_dir = Path(output_dir)
        rendered_files = []

        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)

        # Process each file in the template directory
        for template_path in template_dir.glob("**/*"):
            if not template_path.is_file():
                continue

            # Skip excluded files
            rel_path = template_path.relative_to(template_dir)
            if any(fnmatch.fnmatch(rel_path.as_posix(), pattern) for pattern in exclude):
                logger.debug(f"Skipping excluded file: {rel_path}")
                continue

            # Determine output path
            output_path = output_dir / rel_path

            # Skip binary files
            try:
                template_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                logger.debug(f"Copying binary file: {rel_path}")
                output_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(template_path, output_path)
                rendered_files.append(output_path)
                continue

            # Render template file
            try:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                self.render_to_file(
                    template_name=str(rel_path), output_path=output_path, context=context, **kwargs
                )
                rendered_files.append(output_path)
            except Exception as e:
                logger.error(f"Error processing {rel_path}: {e}")
                raise

        return rendered_files


def process_template_file(
    template_path: Union[str, Path],
    context: Optional[Dict[str, Any]] = None,
    output_path: Optional[Union[str, Path]] = None,
    encoding: str = "utf-8",
    **kwargs,
) -> str:
    """Process a template file with the given context and save it to a file.

    This is an alias for process_template for backward compatibility.

    Args:
        template_path: Path to the template file.
        context: Dictionary of variables to pass to the template.
        output_path: Optional path to save the rendered template.
        encoding: File encoding to use (default: 'utf-8').
        **kwargs: Additional variables to pass to the template.

    Returns:
        str: The rendered template content.
    """
    return process_template(template_path, context, output_path, encoding, **kwargs)


def process_template(
    template_path: Union[str, Path],
    context: Optional[Dict[str, Any]] = None,
    output_path: Optional[Union[str, Path]] = None,
    encoding: str = "utf-8",
    **kwargs,
) -> str:
    """Process a template file with the given context and optionally save it to a file.

    This is a convenience function that creates a TemplateEngine instance and processes
    a single template file.

    Args:
        template_path: Path to the template file.
        context: Dictionary of variables to pass to the template.
        output_path: Optional path to save the rendered template. If not provided,
                    the rendered content is returned but not saved.
        encoding: File encoding to use (default: 'utf-8').
        **kwargs: Additional variables to pass to the template.

    Returns:
        str: The rendered template content.

    Raises:
        FileNotFoundError: If the template file doesn't exist.
        TemplateError: If there's an error rendering the template.
        OSError: If there's an error writing the output file.
    """
    if context is None:
        context = {}

    # Merge additional keyword arguments into the context
    if kwargs:
        context.update(kwargs)

    template_path = Path(template_path)
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")

    try:
        # Create a template engine with the template's directory
        engine = TemplateEngine(template_path.parent)

        # Render the template
        rendered_content = engine.render(template_path.name, context)

        # Save to output file if specified
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Create a backup if the file already exists
            if output_path.exists():
                backup_path = output_path.with_suffix(f"{output_path.suffix}.bak")
                shutil.copy2(output_path, backup_path)
                logger.debug(f"Created backup at {backup_path}")

            with open(output_path, "w", encoding=encoding) as f:
                f.write(rendered_content)

            logger.info(f"Rendered template to {output_path}")

        return rendered_content

    except (TemplateError, OSError) as e:
        logger.error(f"Error processing template {template_path}: {e}")
        raise


def render_template_string(
    template_string: str, context: Optional[Dict[str, Any]] = None, **kwargs
) -> str:
    """Render a template string with the given context.

    This is a convenience function that creates a TemplateEngine instance and renders
    a template string with the provided context.

    Args:
        template_string: The template as a string.
        context: Dictionary of variables to pass to the template.
        **kwargs: Additional variables to pass to the template.

    Returns:
        str: The rendered template content.

    Raises:
        TemplateError: If there's an error rendering the template.
    """
    try:
        # Create a template engine with no template directories
        engine = TemplateEngine()

        # Merge context and kwargs
        ctx = context.copy() if context else {}
        ctx.update(kwargs)

        # Render the template
        return engine.render_string(template_string, ctx)

    except TemplateError as e:
        logger.error(f"Error rendering template string: {e}")
        raise


def process_template_string(
    template_string: str,
    context: Optional[Dict[str, Any]] = None,
    output_path: Optional[Union[str, Path]] = None,
    encoding: str = "utf-8",
    **kwargs,
) -> str:
    """Process a template string with the given context and optionally save it to a file.

    This is a convenience function that creates a TemplateEngine instance and processes
    a template string.

    Args:
        template_string: The template as a string.
        context: Dictionary of variables to pass to the template.
        output_path: Optional path to save the rendered template. If not provided,
                    the rendered content is returned but not saved.
        encoding: File encoding to use (default: 'utf-8').
        **kwargs: Additional variables to pass to the template.

    Returns:
        str: The rendered template content.

    Raises:
        TemplateError: If there's an error rendering the template.
        OSError: If there's an error writing the output file.
    """
    try:
        # Render the template string
        rendered = render_template_string(template_string, context, **kwargs)

        # Save to file if output_path is provided
        if output_path is not None:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Create a backup if the file already exists
            if output_path.exists():
                backup_path = output_path.with_suffix(f"{output_path.suffix}.bak")
                shutil.copy2(output_path, backup_path)
                logger.debug(f"Created backup at {backup_path}")

            output_path.write_text(rendered, encoding=encoding)
            logger.info(f"Rendered template saved to {output_path}")

        return rendered

    except (TemplateError, OSError) as e:
        logger.error(f"Error processing template string: {e}")
        raise


def render_directory(
    template_dir: Union[str, Path],
    output_dir: Union[str, Path],
    context: Optional[Dict[str, Any]] = None,
    exclude: Optional[List[str]] = None,
    **kwargs,
) -> List[Path]:
    """Render all templates in a directory to an output directory.

    This is a convenience function that creates a TemplateEngine instance and processes
    all template files in the specified directory.

    Args:
        template_dir: Directory containing template files.
        output_dir: Directory where rendered files should be saved.
        context: Variables to pass to all templates.
        exclude: List of file patterns to exclude.
        **kwargs: Additional variables to pass to the templates.

    Returns:
        List[Path]: Paths to the rendered files.

    Raises:
        NotADirectoryError: If template_dir is not a directory.
        OSError: If there's an error reading or writing files.
    """
    template_dir = Path(template_dir)
    if not template_dir.is_dir():
        raise NotADirectoryError(f"Template directory not found: {template_dir}")

    try:
        engine = TemplateEngine(template_dir)
        return engine.render_directory(
            template_dir=template_dir,
            output_dir=output_dir,
            context=context,
            exclude=exclude,
            **kwargs,
        )
    except Exception as e:
        logger.error(f"Error rendering directory {template_dir}: {e}")
        raise


def get_template_variables(template_path: Union[str, Path]) -> Dict[str, Any]:
    """Extract variable names from a template file.

    Args:
        template_path: Path to the template file.

    Returns:
        Dict containing template variables and their default values (if any).
    """
    template_path = Path(template_path)
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")

    try:
        # Read the template content
        content = template_path.read_text(encoding="utf-8")

        # Simple regex to find variable patterns like {{ variable }} or {{ variable|default('value') }}
        import re

        pattern = r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)(?:\|.*?)?\s*\}"
        variables = set(re.findall(pattern, content))

        # Try to extract default values for variables with defaults
        defaults = {}
        default_pattern = r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\|default\(["\'](.*?)["\']\)\s*\}'
        for var, default in re.findall(default_pattern, content):
            defaults[var] = default

        # Return variables with their defaults if available
        result = {}
        for var in sorted(variables):
            result[var] = defaults.get(var, None)

        return result

    except Exception as e:
        logger.error(f"Error extracting variables from {template_path}: {e}")
        return {}


def validate_template(
    template_path: Union[str, Path], context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Validate a template by attempting to render it with the given context.

    Args:
        template_path: Path to the template file.
        context: Variables to use for validation.

    Returns:
        Dict containing validation results.
    """
    if context is None:
        context = {}

    template_path = Path(template_path)
    if not template_path.exists():
        return {
            "valid": False,
            "error": f"Template file not found: {template_path}",
            "missing_variables": [],
        }

    try:
        # Try to render the template
        engine = TemplateEngine(template_path.parent)
        rendered = engine.render(template_path.name, context)

        # Check for undefined variables in the rendered content
        import re

        undefined_vars = set()
        for match in re.finditer(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}", rendered):
            var_name = match.group(1)
            if var_name not in context:
                undefined_vars.add(var_name)

        return {
            "valid": len(undefined_vars) == 0,
            "rendered": rendered,
            "missing_variables": sorted(undefined_vars),
        }

    except TemplateError as e:
        return {"valid": False, "error": str(e), "missing_variables": []}
