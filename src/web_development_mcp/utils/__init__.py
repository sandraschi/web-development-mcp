"""
Web Development MCP - Utilities Module

Contains helper functions for file operations, template processing, and validation.
"""

from .file_operations import (
    create_directory,
    create_file,
    read_file,
    write_file,
    copy_file,
    path_exists,
    is_empty_directory,
    create_directory_structure,
    write_json_file,
    read_json_file
)

from .template_engine import (
    process_template,
    process_template_file,
    render_template_string,
    TemplateContext
)

from .validation import (
    is_valid_project_name,
    validate_project_path,
    validate_package_name,
    validate_node_version
)

from .package_resolver import (
    get_latest_package_versions,
    resolve_package_version,
    get_compatible_versions
)

__all__ = [
    # File operations
    'create_directory',
    'create_file',
    'read_file',
    'write_file',
    'copy_file',
    'path_exists',
    'is_empty_directory',
    'create_directory_structure',
    'write_json_file',
    'read_json_file',
    
    # Template engine
    'process_template',
    'process_template_file',
    'render_template_string',
    'TemplateContext',
    
    # Validation
    'is_valid_project_name',
    'validate_project_path',
    'validate_package_name',
    'validate_node_version',
    
    # Package resolution
    'get_latest_package_versions',
    'resolve_package_version',
    'get_compatible_versions'
]
