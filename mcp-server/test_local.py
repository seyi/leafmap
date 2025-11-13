#!/usr/bin/env python
"""
Quick local testing script for the Leafmap MCP server.
Run this to test individual tools without Claude Desktop.
"""

import asyncio
import json
from server import call_tool

async def test_tools():
    """Test various MCP server tools."""

    print("=" * 60)
    print("Testing Leafmap MCP Server Tools")
    print("=" * 60)

    # Test 1: List basemaps
    print("\n1. Testing list_basemaps...")
    result = await call_tool("list_basemaps", {})
    print(json.dumps(json.loads(result[0].text), indent=2))

    # Test 2: Convert coordinates
    print("\n2. Testing convert_coordinates...")
    result = await call_tool("convert_coordinates", {
        "x": -122.4194,
        "y": 37.7749,
        "from_crs": "EPSG:4326",
        "to_crs": "EPSG:3857"
    })
    print(json.dumps(json.loads(result[0].text), indent=2))

    # Test 3: Search WhiteboxTools
    print("\n3. Testing search_whitebox_tools...")
    result = await call_tool("search_whitebox_tools", {
        "query": "watershed"
    })
    data = json.loads(result[0].text)
    print(f"Found {len(data.get('tools', []))} tools matching 'watershed'")
    if data.get('tools'):
        print(f"First result: {data['tools'][0]['name']}")

    # Test 4: Suggest colormap
    print("\n4. Testing suggest_colormap...")
    result = await call_tool("suggest_colormap", {
        "data_type": "elevation"
    })
    data = json.loads(result[0].text)
    print(f"Recommended: {data.get('recommended', [])}")

    # Test 5: List data sources
    print("\n5. Testing list_data_sources...")
    result = await call_tool("list_data_sources", {
        "data_category": "satellite"
    })
    data = json.loads(result[0].text)
    print(f"Found {len(data.get('data_sources', []))} satellite data sources")

    # Test 6: Plan workflow
    print("\n6. Testing plan_workflow...")
    result = await call_tool("plan_workflow", {
        "goal": "Create a simple elevation map from a GeoTIFF file"
    })
    data = json.loads(result[0].text)
    print(f"Workflow: {data.get('workflow_type')}")
    print(f"Steps: {len(data.get('steps', []))}")

    # Test 7: Generate code
    print("\n7. Testing generate_code...")
    result = await call_tool("generate_code", {
        "task": "Create a map with OpenStreetMap basemap",
        "backend": "ipyleaflet"
    })
    data = json.loads(result[0].text)
    print("Generated code snippet:")
    print(data.get('code', '')[:200] + "...")

    print("\n" + "=" * 60)
    print("All basic tests completed successfully!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_tools())
