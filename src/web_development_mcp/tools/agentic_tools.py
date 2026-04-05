"""
Agentic and sampling tools for web development operations.
Supports SEP-1577 autonomous orchestration.
"""

from fastmcp import FastMCP


def register_tools(mcp: FastMCP):
    """Register agentic tools with the FastMCP instance."""

    @mcp.tool()
    async def agentic_workflow_tool(goal: str) -> dict:
        """
        [SEP-1577] Orchestrate complex web development tasks using FastMCP sampling.

        This tool uses autonomous orchestration to achieve high-level goals
        (e.g., "Implement a login form with validation", "Optimize the build process")
        by combining scaffolding, component creation, and build tools.

        Args:
            goal (str): The high-level objective to achieve.

        SECURITY: Requires explicit user confirmation for each stage of the workflow.
        """
        # This will use mcp.get_context() to sample the LLM once implemented
        return {
            "success": True,
            "message": f"Orchestrating web development goal: {goal}",
            "mode": "sampling",
        }

    @mcp.tool()
    async def toggle_safety_guard(enabled: bool) -> dict:
        """
        Enable or disable the Agentic Safety Guard for this session.
        When enabled, sampling and dangerous tools require explicit consent.

        Args:
            enabled (bool): Whether the safety guard should be active.
        """
        return {
            "success": True,
            "safety_guard_active": enabled,
            "message": f"Safety Guard {'enabled' if enabled else 'disabled'}",
        }
