"""
File operations utilities for the Web Development MCP.

Provides functions for working with files and directories in a cross-platform way.
"""

import json
import shutil
from dataclasses import dataclass
from pathlib import Path
from string import Template
from typing import Any, Dict, Generator, List, Optional, Union


@dataclass
class FileInfo:
    """File information container."""

    path: Path
    size: int
    mtime: float
    is_dir: bool
    is_file: bool = True
    is_symlink: bool = False


def create_directory(path: Union[str, Path], exist_ok: bool = True) -> Path:
    """
    Create a directory if it doesn't exist.

    Args:
        path: Path to the directory to create
        exist_ok: If True, don't raise an error if the directory already exists

    Returns:
        Path: The path to the created directory
    """
    path = Path(path) if not isinstance(path, Path) else path
    path.mkdir(parents=True, exist_ok=exist_ok)
    return path


def create_file(file_path: Union[str, Path], content: str = "", encoding: str = "utf-8") -> Path:
    """
    Create a file with the given content.

    Args:
        file_path: Path to the file to create
        content: Content to write to the file
        encoding: File encoding (default: utf-8)

    Returns:
        Path: The path to the created file
    """
    file_path = Path(file_path) if not isinstance(file_path, Path) else file_path
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding=encoding) as f:
        f.write(content)

    return file_path


def create_file_from_template(
    template_path: Union[str, Path],
    output_path: Union[str, Path],
    context: Optional[Dict[str, Any]] = None,
    encoding: str = "utf-8",
) -> Path:
    """
    Create a file from a template file with variable substitution.

    Args:
        template_path: Path to the template file
        output_path: Path where the rendered file will be created
        context: Dictionary of variables for template substitution
        encoding: File encoding (default: utf-8)

    Returns:
        Path: The path to the created file
    """
    template_path = Path(template_path) if not isinstance(template_path, Path) else template_path
    output_path = Path(output_path) if not isinstance(output_path, Path) else output_path

    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")

    # Read the template content
    template_content = read_file(template_path, encoding=encoding)

    # Perform variable substitution if context is provided
    if context:
        template = Template(template_content)
        content = template.safe_substitute(context)
    else:
        content = template_content

    # Create the output file
    return create_file(output_path, content, encoding=encoding)


def read_file(file_path: Union[str, Path], encoding: str = "utf-8") -> str:
    """
    Read the contents of a file.

    Args:
        file_path: Path to the file to read
        encoding: File encoding (default: utf-8)

    Returns:
        str: The contents of the file
    """
    file_path = Path(file_path) if not isinstance(file_path, Path) else file_path
    with open(file_path, encoding=encoding) as f:
        return f.read()


def read_file_lines(file_path: Union[str, Path], encoding: str = "utf-8") -> List[str]:
    """
    Read the contents of a file as a list of lines.

    Args:
        file_path: Path to the file to read
        encoding: File encoding (default: utf-8)

    Returns:
        List[str]: List of lines in the file
    """
    file_path = Path(file_path) if not isinstance(file_path, Path) else file_path
    with open(file_path, encoding=encoding) as f:
        return [line.rstrip("\n") for line in f]


def read_file_chunks(
    file_path: Union[str, Path], chunk_size: int = 8192, encoding: str = "utf-8"
) -> Generator[str, None, None]:
    """
    Read a file in chunks.

    Args:
        file_path: Path to the file to read
        chunk_size: Size of each chunk in bytes (default: 8KB)
        encoding: File encoding (default: utf-8)

    Yields:
        str: Chunks of file content
    """
    file_path = Path(file_path) if not isinstance(file_path, Path) else file_path
    with open(file_path, encoding=encoding) as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk


def write_file(file_path: Union[str, Path], content: str, encoding: str = "utf-8") -> Path:
    """
    Write content to a file, creating parent directories if needed.

    Args:
        file_path: Path to the file to write
        content: Content to write to the file
        encoding: File encoding (default: utf-8)

    Returns:
        Path: The path to the written file
    """
    file_path = Path(file_path) if not isinstance(file_path, Path) else file_path
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding=encoding) as f:
        f.write(content)

    return file_path


def append_to_file(file_path: Union[str, Path], content: str, encoding: str = "utf-8") -> Path:
    """
    Append content to a file, creating it if it doesn't exist.

    Args:
        file_path: Path to the file to append to
        content: Content to append to the file
        encoding: File encoding (default: utf-8)

    Returns:
        Path: The path to the modified file
    """
    file_path = Path(file_path) if not isinstance(file_path, Path) else file_path
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "a", encoding=encoding) as f:
        f.write(content)

    return file_path


def write_lines(file_path: Union[str, Path], lines: List[str], encoding: str = "utf-8") -> Path:
    """
    Write a list of lines to a file.

    Args:
        file_path: Path to the file to write
        lines: List of strings to write as lines
        encoding: File encoding (default: utf-8)

    Returns:
        Path: The path to the written file
    """
    file_path = Path(file_path) if not isinstance(file_path, Path) else file_path
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding=encoding) as f:
        f.writelines(f"{line}\n" for line in lines)

    return file_path


def copy_file(
    source: Union[str, Path], destination: Union[str, Path], overwrite: bool = False
) -> Path:
    """
    Copy a file from source to destination.

    Args:
        source: Path to the source file
        destination: Path to the destination file
        overwrite: If True, overwrite the destination file if it exists

    Returns:
        Path: The path to the destination file
    """
    source = Path(source) if not isinstance(source, Path) else source
    destination = Path(destination) if not isinstance(destination, Path) else destination

    if not source.is_file():
        raise FileNotFoundError(f"Source file not found: {source}")

    if destination.exists() and not overwrite:
        raise FileExistsError(f"Destination file already exists: {destination}")

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return destination


def path_exists(path: Union[str, Path]) -> bool:
    """
    Check if a path exists.

    Args:
        path: Path to check

    Returns:
        bool: True if the path exists, False otherwise
    """
    path = Path(path) if not isinstance(path, Path) else path
    return path.exists()


def is_empty_directory(path: Union[str, Path]) -> bool:
    """
    Check if a directory is empty.

    Args:
        path: Path to the directory to check

    Returns:
        bool: True if the directory exists and is empty, False otherwise
    """
    path = Path(path) if not isinstance(path, Path) else path
    if not path.is_dir():
        return False
    return not any(path.iterdir())


def create_directory_structure(base_path: Union[str, Path], directories: List[str]) -> None:
    """
    Create multiple directories under a base path.

    Args:
        base_path: Base directory path
        directories: List of directory names to create
    """
    base_path = Path(base_path) if not isinstance(base_path, Path) else base_path
    for directory in directories:
        (base_path / directory).mkdir(parents=True, exist_ok=True)


def write_json_file(path: Union[str, Path], data: Dict[str, Any], indent: int = 2) -> Path:
    """
    Write data to a JSON file.

    Args:
        path: Path to the JSON file
        data: Data to write (must be JSON-serializable)
        indent: Number of spaces to use for indentation

    Returns:
        Path: The path to the written file
    """
    path = Path(path) if not isinstance(path, Path) else path
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
    return path


def read_json_file(path: Union[str, Path]) -> Dict[str, Any]:
    """
    Read data from a JSON file.

    Args:
        path: Path to the JSON file

    Returns:
        Dict[str, Any]: The parsed JSON data
    """
    path = Path(path) if not isinstance(path, Path) else path
    with open(path, encoding="utf-8") as f:
        return json.load(f)
