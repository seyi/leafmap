#!/usr/bin/env python
"""
Test the notebook generation and execution workflow.
This demonstrates the end-to-end automation capabilities.
"""

import asyncio
import json
import os
from server import call_tool

async def test_notebook_workflow():
    """Test creating and executing a notebook workflow."""

    print("=" * 70)
    print("Testing Notebook Generation and Execution Workflow")
    print("=" * 70)

    # Test 1: Plan a workflow
    print("\n1. Planning a simple mapping workflow...")
    result = await call_tool("plan_workflow", {
        "goal": "Create a simple map with a custom basemap"
    })
    plan = json.loads(result[0].text)
    print(f"   Workflow type: {plan.get('workflow_type')}")
    print(f"   Number of steps: {len(plan.get('steps', []))}")

    # Test 2: Create a notebook
    print("\n2. Creating a Jupyter notebook...")
    notebook_path = "/tmp/test_leafmap_demo.ipynb"
    result = await call_tool("create_notebook", {
        "goal": "Create a simple interactive map with OpenStreetMap basemap",
        "output_path": notebook_path,
        "parameters": {
            "center": [37.7749, -122.4194],
            "zoom": 12
        }
    })
    create_result = json.loads(result[0].text)
    print(f"   Status: {create_result.get('status')}")
    print(f"   Notebook: {create_result.get('notebook_path')}")
    print(f"   Cells created: {create_result.get('cells_created')}")

    # Test 3: Execute the workflow (without opening)
    print("\n3. Executing the workflow...")
    result = await call_tool("execute_workflow", {
        "goal": "Create a simple interactive map showing San Francisco",
        "working_directory": "/tmp",
        "parameters": {
            "location": "San Francisco",
            "center": [37.7749, -122.4194],
            "zoom": 12
        },
        "timeout": 60,
        "open_notebook": False,  # Don't open browser in test
        "output_format": "none"
    })
    exec_result = json.loads(result[0].text)
    print(f"   Status: {exec_result.get('status')}")
    print(f"   Execution: {exec_result.get('execution_status')}")
    print(f"   Notebook: {exec_result.get('notebook_path')}")
    print(f"   Executed notebook: {exec_result.get('executed_notebook_path')}")
    print(f"   Outputs captured: {exec_result.get('outputs_count', 0)}")

    if exec_result.get('outputs_summary'):
        print("\n   Output summary:")
        for output in exec_result['outputs_summary'][:3]:
            print(f"     - Cell {output.get('cell')}: {output.get('type')}")
            if output.get('content'):
                content = output['content'][:100]
                print(f"       {content}...")

    # Test 4: Generate code snippet
    print("\n4. Generating code snippet...")
    result = await call_tool("generate_code", {
        "task": "Load a GeoJSON file and display it on a map",
        "backend": "ipyleaflet"
    })
    code_result = json.loads(result[0].text)
    print(f"   Code generated: {len(code_result.get('code', ''))} characters")
    print("\n   Sample code:")
    code_lines = code_result.get('code', '').split('\n')[:10]
    for line in code_lines:
        print(f"     {line}")

    print("\n" + "=" * 70)
    print("Workflow test completed!")
    print("=" * 70)
    print("\nKey capabilities demonstrated:")
    print("  ✓ Workflow planning")
    print("  ✓ Notebook creation")
    print("  ✓ Code execution")
    print("  ✓ Output capture")
    print("  ✓ Code generation")
    print("\nTo test with automatic browser opening, set:")
    print("  open_notebook=True, output_format='html'")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(test_notebook_workflow())
