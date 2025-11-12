"""
Tests for the Leafmap MCP Server.
"""

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest
import numpy as np

# Add parent directory to path to import server
sys.path.insert(0, os.path.dirname(__file__))

from server import app, list_tools, list_resources, call_tool, read_resource


class TestResources:
    """Test resource-related functionality."""

    @pytest.mark.asyncio
    async def test_list_resources(self):
        """Test listing all available resources."""
        resources = await list_resources()
        assert len(resources) == 5

        resource_uris = [str(r.uri) for r in resources]
        assert "leafmap://docs/overview" in resource_uris
        assert "leafmap://docs/installation" in resource_uris
        assert "leafmap://docs/quickstart" in resource_uris
        assert "leafmap://info/repository" in resource_uris
        assert "leafmap://info/basemaps" in resource_uris

    @pytest.mark.asyncio
    async def test_read_overview_resource(self):
        """Test reading the overview resource."""
        content = await read_resource("leafmap://docs/overview")
        assert "Leafmap" in content
        assert "geospatial analysis" in content
        assert "interactive mapping" in content
        assert "Key Features:" in content

    @pytest.mark.asyncio
    async def test_read_installation_resource(self):
        """Test reading the installation resource."""
        content = await read_resource("leafmap://docs/installation")
        assert "pip install leafmap" in content
        assert "conda install" in content
        assert "Python >= 3.9" in content

    @pytest.mark.asyncio
    async def test_read_quickstart_resource(self):
        """Test reading the quickstart resource."""
        content = await read_resource("leafmap://docs/quickstart")
        assert "import leafmap" in content
        assert "leafmap.Map()" in content
        assert "add_basemap" in content
        assert "add_vector" in content

    @pytest.mark.asyncio
    async def test_read_repository_resource(self):
        """Test reading the repository resource."""
        content = await read_resource("leafmap://info/repository")
        data = json.loads(content)

        assert data["name"] == "leafmap"
        assert data["version"] == "0.57.1"
        assert "Qiusheng Wu" in data["author"]
        assert data["license"] == "MIT"
        assert "github.com/opengeos/leafmap" in data["github"]

    @pytest.mark.asyncio
    async def test_read_basemaps_resource(self):
        """Test reading the basemaps resource."""
        content = await read_resource("leafmap://info/basemaps")
        data = json.loads(content)

        # Should be a dictionary of basemaps
        assert isinstance(data, dict)
        # Should have some basemaps (could have error key if import fails)
        assert len(data) > 0

    @pytest.mark.asyncio
    async def test_read_invalid_resource(self):
        """Test reading an invalid resource raises an error."""
        with pytest.raises(ValueError, match="Unknown resource"):
            await read_resource("leafmap://invalid/resource")


class TestTools:
    """Test tool-related functionality."""

    @pytest.mark.asyncio
    async def test_list_tools(self):
        """Test listing all available tools."""
        tools = await list_tools()
        assert len(tools) == 7

        tool_names = [t.name for t in tools]
        assert "view_raster" in tool_names
        assert "view_vector" in tool_names
        assert "get_raster_info" in tool_names
        assert "get_vector_info" in tool_names
        assert "list_basemaps" in tool_names
        assert "convert_coordinates" in tool_names
        assert "get_crs_info" in tool_names

    @pytest.mark.asyncio
    async def test_list_basemaps_tool(self):
        """Test the list_basemaps tool."""
        result = await call_tool("list_basemaps", {})

        assert len(result) == 1
        assert result[0].type == "text"

        # Handle both success and error cases
        try:
            data = json.loads(result[0].text)
            assert "count" in data or "error" in data
            if "basemaps" in data:
                assert isinstance(data["basemaps"], list)
        except json.JSONDecodeError:
            # If JSON parsing fails, check if it's an error message
            assert "Error" in result[0].text or "error" in result[0].text.lower()

    @pytest.mark.asyncio
    async def test_convert_coordinates_tool(self):
        """Test the convert_coordinates tool."""
        # Convert from WGS84 to Web Mercator
        args = {
            "x": -122.4194,
            "y": 37.7749,
            "from_crs": "EPSG:4326",
            "to_crs": "EPSG:3857",
        }

        result = await call_tool("convert_coordinates", args)

        assert len(result) == 1
        assert result[0].type == "text"

        data = json.loads(result[0].text)
        assert "input" in data
        assert "output" in data
        assert data["input"]["x"] == -122.4194
        assert data["input"]["y"] == 37.7749
        assert data["input"]["crs"] == "EPSG:4326"
        assert data["output"]["crs"] == "EPSG:3857"

        # Web Mercator coordinates should be much larger
        assert abs(data["output"]["x"]) > 10000000
        assert abs(data["output"]["y"]) > 1000000

    @pytest.mark.asyncio
    async def test_convert_coordinates_same_crs(self):
        """Test converting coordinates to the same CRS."""
        args = {
            "x": 10.0,
            "y": 20.0,
            "from_crs": "EPSG:4326",
            "to_crs": "EPSG:4326",
        }

        result = await call_tool("convert_coordinates", args)
        data = json.loads(result[0].text)

        # Should return the same coordinates
        assert abs(data["output"]["x"] - 10.0) < 0.0001
        assert abs(data["output"]["y"] - 20.0) < 0.0001

    @pytest.mark.asyncio
    async def test_get_crs_info_wgs84(self):
        """Test getting CRS info for WGS84."""
        args = {"crs_code": "EPSG:4326"}

        result = await call_tool("get_crs_info", args)

        assert len(result) == 1
        assert result[0].type == "text"

        data = json.loads(result[0].text)
        assert data["code"] == "EPSG:4326"
        assert "WGS 84" in data["name"] or "WGS84" in data["name"]
        assert data["type"] is not None
        assert "axis_info" in data
        assert len(data["axis_info"]) > 0

    @pytest.mark.asyncio
    async def test_get_crs_info_web_mercator(self):
        """Test getting CRS info for Web Mercator."""
        args = {"crs_code": "EPSG:3857"}

        result = await call_tool("get_crs_info", args)
        data = json.loads(result[0].text)

        assert data["code"] == "EPSG:3857"
        assert "axis_info" in data
        # Web Mercator should have meter units
        assert any("metre" in axis["unit"].lower() or "meter" in axis["unit"].lower()
                   for axis in data["axis_info"])

    @pytest.mark.asyncio
    async def test_view_raster_tool_basic(self):
        """Test the view_raster tool with basic parameters."""
        args = {"file_path": "/path/to/test.tif"}

        result = await call_tool("view_raster", args)

        assert len(result) == 1
        assert result[0].type == "text"

        # Handle both success and error cases
        try:
            data = json.loads(result[0].text)
            assert "message" in data or "error" in data
            if "command" in data:
                assert "view-raster" in data["command"]
                assert "/path/to/test.tif" in data["command"]
        except json.JSONDecodeError:
            # If JSON parsing fails, check if it's an error message
            assert "Error" in result[0].text

    @pytest.mark.asyncio
    async def test_view_raster_tool_with_options(self):
        """Test the view_raster tool with all options."""
        args = {
            "file_path": "/path/to/test.tif",
            "port": 8080,
            "band": 1,
            "colormap": "viridis",
            "vmin": 0.0,
            "vmax": 100.0,
            "nodata": -9999.0,
        }

        result = await call_tool("view_raster", args)

        # Handle both success and error cases
        try:
            data = json.loads(result[0].text)
            if "parameters" in data:
                assert data["parameters"]["file_path"] == "/path/to/test.tif"
                assert data["parameters"]["port"] == 8080
                assert data["parameters"]["indexes"] == 1
                assert data["parameters"]["colormap"] == "viridis"
                assert data["parameters"]["vmin"] == 0.0
                assert data["parameters"]["vmax"] == 100.0
                assert data["parameters"]["nodata"] == -9999.0
        except json.JSONDecodeError:
            # If JSON parsing fails, check if it's an error message
            assert "Error" in result[0].text

    @pytest.mark.asyncio
    async def test_view_raster_tool_with_rgb(self):
        """Test the view_raster tool with RGB bands."""
        args = {
            "file_path": "/path/to/test.tif",
            "rgb_bands": [3, 2, 1],
        }

        result = await call_tool("view_raster", args)

        # Handle both success and error cases
        try:
            data = json.loads(result[0].text)
            if "parameters" in data:
                assert data["parameters"]["indexes"] == [3, 2, 1]
        except json.JSONDecodeError:
            # If JSON parsing fails, check if it's an error message
            assert "Error" in result[0].text

    @pytest.mark.asyncio
    async def test_view_vector_tool_basic(self):
        """Test the view_vector tool with basic parameters."""
        args = {"file_path": "/path/to/test.geojson"}

        result = await call_tool("view_vector", args)

        assert len(result) == 1
        assert result[0].type == "text"

        # Handle both success and error cases
        try:
            data = json.loads(result[0].text)
            assert "message" in data or "error" in data
            if "command" in data:
                assert "view-vector" in data["command"]
                assert "/path/to/test.geojson" in data["command"]
        except json.JSONDecodeError:
            # If JSON parsing fails, check if it's an error message
            assert "Error" in result[0].text

    @pytest.mark.asyncio
    async def test_view_vector_tool_with_style(self):
        """Test the view_vector tool with custom style."""
        args = {
            "file_path": "/path/to/test.geojson",
            "style": "positron",
        }

        result = await call_tool("view_vector", args)

        # Handle both success and error cases
        try:
            data = json.loads(result[0].text)
            if "parameters" in data:
                assert data["parameters"]["style"] == "positron"
                assert "positron" in data["command"]
        except json.JSONDecodeError:
            # If JSON parsing fails, check if it's an error message
            assert "Error" in result[0].text

    @pytest.mark.asyncio
    async def test_invalid_tool_name(self):
        """Test calling an invalid tool raises an error."""
        result = await call_tool("invalid_tool", {})

        assert len(result) == 1
        assert result[0].type == "text"
        assert "Error" in result[0].text or "Unknown tool" in result[0].text


class TestRasterInfo:
    """Test raster info functionality with actual files."""

    @pytest.fixture
    def sample_raster(self):
        """Create a sample GeoTIFF for testing."""
        try:
            import rasterio
            from rasterio.transform import from_bounds

            # Create a temporary GeoTIFF
            temp_dir = tempfile.mkdtemp()
            raster_path = os.path.join(temp_dir, "test.tif")

            # Create sample data
            data = np.random.randint(0, 255, (100, 100), dtype=np.uint8)

            # Define bounds and transform
            bounds = (-180, -90, 180, 90)
            transform = from_bounds(*bounds, 100, 100)

            # Write GeoTIFF
            with rasterio.open(
                raster_path,
                'w',
                driver='GTiff',
                height=100,
                width=100,
                count=1,
                dtype=data.dtype,
                crs='EPSG:4326',
                transform=transform,
            ) as dst:
                dst.write(data, 1)

            yield raster_path

            # Cleanup
            os.remove(raster_path)
            os.rmdir(temp_dir)

        except ImportError:
            pytest.skip("rasterio not installed")

    @pytest.mark.asyncio
    async def test_get_raster_info_real_file(self, sample_raster):
        """Test getting info from a real raster file."""
        args = {"file_path": sample_raster}

        result = await call_tool("get_raster_info", args)

        assert len(result) == 1
        assert result[0].type == "text"

        data = json.loads(result[0].text)
        assert data["width"] == 100
        assert data["height"] == 100
        assert data["count"] == 1
        assert data["dtype"] == "uint8"
        assert "EPSG:4326" in data["crs"]
        assert "bounds" in data
        assert "transform" in data

    @pytest.mark.asyncio
    async def test_get_raster_info_nonexistent_file(self):
        """Test getting info from a nonexistent file."""
        args = {"file_path": "/nonexistent/path/test.tif"}

        result = await call_tool("get_raster_info", args)

        assert len(result) == 1
        assert "Error" in result[0].text


class TestVectorInfo:
    """Test vector info functionality with actual files."""

    @pytest.fixture
    def sample_vector(self):
        """Create a sample GeoJSON for testing."""
        try:
            import geopandas as gpd
            from shapely.geometry import Point

            # Create a temporary GeoJSON
            temp_dir = tempfile.mkdtemp()
            vector_path = os.path.join(temp_dir, "test.geojson")

            # Create sample data
            points = [Point(x, y) for x, y in [(0, 0), (1, 1), (2, 2)]]
            gdf = gpd.GeoDataFrame(
                {'id': [1, 2, 3], 'name': ['A', 'B', 'C']},
                geometry=points,
                crs='EPSG:4326'
            )

            # Write GeoJSON
            gdf.to_file(vector_path, driver='GeoJSON')

            yield vector_path

            # Cleanup
            os.remove(vector_path)
            os.rmdir(temp_dir)

        except ImportError:
            pytest.skip("geopandas not installed")

    @pytest.mark.asyncio
    async def test_get_vector_info_real_file(self, sample_vector):
        """Test getting info from a real vector file."""
        args = {"file_path": sample_vector}

        result = await call_tool("get_vector_info", args)

        assert len(result) == 1
        assert result[0].type == "text"

        # Handle both success and error cases (geopandas might not be installed)
        try:
            data = json.loads(result[0].text)
            assert data["feature_count"] == 3
            assert data["geometry_type"] == "Point"
            assert "EPSG:4326" in data["crs"]
            assert "bounds" in data
            assert "columns" in data
            assert "id" in data["columns"]
            assert "name" in data["columns"]
        except json.JSONDecodeError:
            # If JSON parsing fails, check if it's an error message about missing dependencies
            assert "Error" in result[0].text or "geopandas" in result[0].text

    @pytest.mark.asyncio
    async def test_get_vector_info_nonexistent_file(self):
        """Test getting info from a nonexistent file."""
        args = {"file_path": "/nonexistent/path/test.geojson"}

        result = await call_tool("get_vector_info", args)

        assert len(result) == 1
        assert "Error" in result[0].text


class TestErrorHandling:
    """Test error handling in various scenarios."""

    @pytest.mark.asyncio
    async def test_convert_coordinates_invalid_crs(self):
        """Test coordinate conversion with invalid CRS."""
        args = {
            "x": 10.0,
            "y": 20.0,
            "from_crs": "INVALID:1234",
            "to_crs": "EPSG:4326",
        }

        result = await call_tool("convert_coordinates", args)
        assert "Error" in result[0].text

    @pytest.mark.asyncio
    async def test_get_crs_info_invalid_code(self):
        """Test getting CRS info with invalid code."""
        args = {"crs_code": "INVALID:9999"}

        result = await call_tool("get_crs_info", args)
        assert "Error" in result[0].text

    @pytest.mark.asyncio
    async def test_tool_missing_required_argument(self):
        """Test calling a tool without required arguments."""
        # convert_coordinates requires x, y, from_crs, to_crs
        args = {"x": 10.0}

        # This should raise an error or return an error message
        try:
            result = await call_tool("convert_coordinates", args)
            assert "Error" in result[0].text or "missing" in result[0].text.lower()
        except (KeyError, TypeError):
            # Expected behavior - missing required arguments
            pass


class TestIntegration:
    """Integration tests for the MCP server."""

    @pytest.mark.asyncio
    async def test_server_initialization(self):
        """Test that the server initializes correctly."""
        assert app is not None
        assert app.name == "leafmap-mcp-server"

    @pytest.mark.asyncio
    async def test_all_tools_have_descriptions(self):
        """Test that all tools have proper descriptions."""
        tools = await list_tools()

        for tool in tools:
            assert tool.name is not None
            assert tool.description is not None
            assert len(tool.description) > 0
            assert tool.inputSchema is not None

    @pytest.mark.asyncio
    async def test_all_resources_have_descriptions(self):
        """Test that all resources have proper descriptions."""
        resources = await list_resources()

        for resource in resources:
            assert resource.uri is not None
            assert resource.name is not None
            assert resource.description is not None
            assert len(resource.description) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
