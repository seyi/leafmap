#!/usr/bin/env python3
"""
Leafmap MCP Server

A Model Context Protocol (MCP) server that provides tools for geospatial analysis
and interactive mapping using the leafmap library.
"""

import json
import logging
import os
import sys
from typing import Any, Sequence

# Add parent directory to path to import leafmap
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import (
        Resource,
        Tool,
        TextContent,
        ImageContent,
        EmbeddedResource,
    )
except ImportError:
    print("Error: MCP SDK not installed. Install with: pip install mcp", file=sys.stderr)
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("leafmap-mcp-server")

# Initialize MCP server
app = Server("leafmap-mcp-server")


@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="leafmap://docs/overview",
            name="Leafmap Documentation Overview",
            mimeType="text/plain",
            description="Overview of leafmap features and capabilities",
        ),
        Resource(
            uri="leafmap://docs/installation",
            name="Installation Guide",
            mimeType="text/plain",
            description="How to install leafmap and its dependencies",
        ),
        Resource(
            uri="leafmap://docs/quickstart",
            name="Quick Start Guide",
            mimeType="text/plain",
            description="Quick start guide for using leafmap",
        ),
        Resource(
            uri="leafmap://info/repository",
            name="Repository Information",
            mimeType="application/json",
            description="Information about the leafmap repository",
        ),
        Resource(
            uri="leafmap://info/basemaps",
            name="Available Basemaps",
            mimeType="application/json",
            description="List of available basemaps in leafmap",
        ),
    ]


@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific resource."""
    if uri == "leafmap://docs/overview":
        return """Leafmap: Interactive Geospatial Analysis Tool

Leafmap is a Python package for geospatial analysis and interactive mapping
in a Jupyter environment. It provides tools for:

Key Features:
- Creating interactive maps with one line of code
- Supporting multiple backends (ipyleaflet, folium, kepler.gl, pydeck, bokeh)
- Changing basemaps interactively
- Adding XYZ, WMS, and vector tile services
- Displaying vector data (Shapefile, GeoJSON, GeoPackage, etc.)
- Displaying raster data (GeoTIFFs, COGs, etc.)
- Creating custom legends and colorbars
- Creating split-panel maps and linked maps
- Downloading and visualizing OpenStreetMap data
- Creating and editing vector data interactively
- Searching for geospatial data (STAC, Microsoft Planetary Computer, etc.)
- Inspecting pixel values interactively
- Creating choropleth maps and heat maps
- Displaying data from PostGIS databases
- Creating time series animations
- Analyzing geospatial data with WhiteboxTools (500+ tools)
- Segmenting and classifying remote sensing imagery
- Building interactive web apps (Voila, Streamlit, Solara)

Documentation: https://leafmap.org
GitHub: https://github.com/opengeos/leafmap
"""

    elif uri == "leafmap://docs/installation":
        return """Installation Guide

Basic Installation:
    pip install leafmap

With all optional dependencies:
    pip install "leafmap[all]"

Specific features:
    pip install "leafmap[backends]"    # Multiple mapping backends
    pip install "leafmap[lidar]"       # LiDAR data support
    pip install "leafmap[raster]"      # Raster data support
    pip install "leafmap[vector]"      # Vector data support
    pip install "leafmap[maplibre]"    # MapLibre support
    pip install "leafmap[apps]"        # Web app frameworks
    pip install "leafmap[ai]"          # AI/ML capabilities

Using conda:
    conda install -c conda-forge leafmap

Requirements:
- Python >= 3.9
- See requirements.txt for full dependency list
"""

    elif uri == "leafmap://docs/quickstart":
        return """Quick Start Guide

1. Create a basic map:
    import leafmap
    m = leafmap.Map()
    m

2. Add a basemap:
    m.add_basemap("OpenTopoMap")

3. Add vector data:
    m.add_vector("path/to/file.geojson")
    # Or from URL:
    url = "https://example.com/data.geojson"
    m.add_vector(url)

4. Add raster data:
    m.add_raster("path/to/file.tif", layer_name="My Raster")

5. View raster file from command line:
    leafmap view-raster path/to/file.tif
    # Or:
    view-raster path/to/file.tif --colormap viridis --band 1

6. View vector file from command line:
    leafmap view-vector path/to/file.geojson
    # Or:
    view-vector path/to/file.shp --style dark-matter

7. Create split-panel map:
    m = leafmap.Map()
    m.split_map(left_layer="OpenStreetMap", right_layer="Esri.WorldImagery")

8. Search and add STAC data:
    m = leafmap.Map()
    m.add_stac_layer(
        url="https://planetarycomputer.microsoft.com/api/stac/v1",
        collection="landsat-c2-l2",
        items=["LC08_L2SP_047027_20201204_02_T1"],
    )

For more examples, visit: https://leafmap.org/notebooks/
"""

    elif uri == "leafmap://info/repository":
        return json.dumps(
            {
                "name": "leafmap",
                "version": "0.57.1",
                "description": "A Python package for geospatial analysis and interactive mapping in a Jupyter environment",
                "author": "Qiusheng Wu",
                "email": "giswqs@gmail.com",
                "license": "MIT",
                "github": "https://github.com/opengeos/leafmap",
                "documentation": "https://leafmap.org",
                "pypi": "https://pypi.org/project/leafmap",
                "conda": "https://anaconda.org/conda-forge/leafmap",
                "youtube": "https://youtube.com/@giswqs",
            },
            indent=2,
        )

    elif uri == "leafmap://info/basemaps":
        try:
            from leafmap import basemaps as bm

            basemap_dict = {}
            for attr in dir(bm):
                if not attr.startswith("_"):
                    obj = getattr(bm, attr)
                    if isinstance(obj, dict) and "url" in obj:
                        basemap_dict[attr] = {
                            "name": obj.get("name", attr),
                            "url": obj.get("url", ""),
                            "attribution": obj.get("attribution", ""),
                        }

            return json.dumps(basemap_dict, indent=2)
        except Exception as e:
            return json.dumps({"error": str(e)}, indent=2)

    else:
        raise ValueError(f"Unknown resource: {uri}")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="view_raster",
            description="View a raster file (GeoTIFF, COG, etc.) interactively in a web browser. "
            "This tool creates a local tile server and generates an interactive HTML viewer "
            "with features like opacity control, basemap selection, and coordinate display.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path or URL to the raster file",
                    },
                    "port": {
                        "type": "integer",
                        "description": "Port for the tile server (optional)",
                    },
                    "band": {
                        "type": "integer",
                        "description": "Band index to display (1-based, optional)",
                    },
                    "rgb_bands": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "description": "List of band indices for RGB visualization (e.g., [3, 2, 1])",
                    },
                    "colormap": {
                        "type": "string",
                        "description": "Colormap name to apply (e.g., 'viridis', 'terrain')",
                    },
                    "vmin": {
                        "type": "number",
                        "description": "Minimum value for color mapping",
                    },
                    "vmax": {
                        "type": "number",
                        "description": "Maximum value for color mapping",
                    },
                    "nodata": {
                        "type": "number",
                        "description": "Nodata value",
                    },
                },
                "required": ["file_path"],
            },
        ),
        Tool(
            name="view_vector",
            description="View a vector file (Shapefile, GeoJSON, GeoPackage, etc.) interactively "
            "in a web browser using MapLibre. The viewer supports various map styles and "
            "interactive features like zooming, panning, and feature inspection.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path or URL to the vector file",
                    },
                    "style": {
                        "type": "string",
                        "description": "Map style (e.g., 'dark-matter', 'positron', 'voyager')",
                        "default": "dark-matter",
                    },
                },
                "required": ["file_path"],
            },
        ),
        Tool(
            name="get_raster_info",
            description="Get metadata information about a raster file including bands, CRS, "
            "bounds, resolution, and data type. Useful for understanding raster properties "
            "before visualization or analysis.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path or URL to the raster file",
                    },
                },
                "required": ["file_path"],
            },
        ),
        Tool(
            name="get_vector_info",
            description="Get information about a vector file including geometry type, CRS, "
            "feature count, bounds, and attribute fields. Helps understand vector data "
            "structure before further processing.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path or URL to the vector file",
                    },
                },
                "required": ["file_path"],
            },
        ),
        Tool(
            name="list_basemaps",
            description="List all available basemaps in leafmap. Returns a comprehensive list "
            "of basemap providers and their tile URLs that can be used in interactive maps.",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="convert_coordinates",
            description="Convert coordinates between different coordinate reference systems (CRS). "
            "Supports conversion between common CRS like WGS84 (EPSG:4326), Web Mercator "
            "(EPSG:3857), and many others.",
            inputSchema={
                "type": "object",
                "properties": {
                    "x": {
                        "type": "number",
                        "description": "X coordinate (longitude or easting)",
                    },
                    "y": {
                        "type": "number",
                        "description": "Y coordinate (latitude or northing)",
                    },
                    "from_crs": {
                        "type": "string",
                        "description": "Source CRS (e.g., 'EPSG:4326')",
                    },
                    "to_crs": {
                        "type": "string",
                        "description": "Target CRS (e.g., 'EPSG:3857')",
                    },
                },
                "required": ["x", "y", "from_crs", "to_crs"],
            },
        ),
        Tool(
            name="get_crs_info",
            description="Get information about a coordinate reference system (CRS) by its code "
            "(e.g., EPSG:4326). Returns details about the CRS including name, type, units, "
            "and area of use.",
            inputSchema={
                "type": "object",
                "properties": {
                    "crs_code": {
                        "type": "string",
                        "description": "CRS code (e.g., 'EPSG:4326', 'EPSG:3857')",
                    },
                },
                "required": ["crs_code"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls."""
    try:
        if name == "view_raster":
            file_path = arguments["file_path"]
            port = arguments.get("port")
            band = arguments.get("band")
            rgb_bands = arguments.get("rgb_bands")
            colormap = arguments.get("colormap")
            vmin = arguments.get("vmin")
            vmax = arguments.get("vmax")
            nodata = arguments.get("nodata")

            # Determine indexes parameter
            indexes = None
            if rgb_bands:
                indexes = rgb_bands
            elif band:
                indexes = band

            # Import here to avoid issues if dependencies aren't installed
            from leafmap.cli import view_raster

            # Note: view_raster normally opens a browser, but we'll just provide instructions
            result = {
                "message": "To view the raster file, run the following command:",
                "command": f"view-raster {file_path}",
                "parameters": {
                    "file_path": file_path,
                    "port": port,
                    "indexes": indexes,
                    "colormap": colormap,
                    "vmin": vmin,
                    "vmax": vmax,
                    "nodata": nodata,
                },
                "note": "This will open an interactive viewer in your default web browser.",
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "view_vector":
            file_path = arguments["file_path"]
            style = arguments.get("style", "dark-matter")

            from leafmap.cli import view_vector

            result = {
                "message": "To view the vector file, run the following command:",
                "command": f"view-vector {file_path} --style {style}",
                "parameters": {
                    "file_path": file_path,
                    "style": style,
                },
                "note": "This will open an interactive viewer in your default web browser.",
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "get_raster_info":
            file_path = arguments["file_path"]

            try:
                import rasterio

                with rasterio.open(file_path) as src:
                    info = {
                        "file": file_path,
                        "driver": src.driver,
                        "width": src.width,
                        "height": src.height,
                        "count": src.count,
                        "dtype": str(src.dtypes[0]),
                        "crs": str(src.crs) if src.crs else None,
                        "bounds": {
                            "left": src.bounds.left,
                            "bottom": src.bounds.bottom,
                            "right": src.bounds.right,
                            "top": src.bounds.top,
                        },
                        "transform": [x for x in src.transform],
                        "resolution": (src.res[0], src.res[1]),
                        "nodata": src.nodata,
                        "band_names": [src.descriptions[i] or f"Band {i+1}" for i in range(src.count)],
                    }

                    return [TextContent(type="text", text=json.dumps(info, indent=2))]
            except ImportError:
                return [
                    TextContent(
                        type="text",
                        text="Error: rasterio is not installed. Install with: pip install rasterio",
                    )
                ]
            except Exception as e:
                return [TextContent(type="text", text=f"Error reading raster: {str(e)}")]

        elif name == "get_vector_info":
            file_path = arguments["file_path"]

            try:
                from leafmap.common import read_vector

                gdf = read_vector(file_path)

                info = {
                    "file": file_path,
                    "feature_count": len(gdf),
                    "geometry_type": gdf.geom_type.iloc[0] if len(gdf) > 0 else None,
                    "crs": str(gdf.crs) if gdf.crs else None,
                    "bounds": {
                        "minx": float(gdf.total_bounds[0]),
                        "miny": float(gdf.total_bounds[1]),
                        "maxx": float(gdf.total_bounds[2]),
                        "maxy": float(gdf.total_bounds[3]),
                    } if len(gdf) > 0 else None,
                    "columns": list(gdf.columns),
                    "column_types": {col: str(dtype) for col, dtype in gdf.dtypes.items()},
                }

                return [TextContent(type="text", text=json.dumps(info, indent=2))]
            except ImportError:
                return [
                    TextContent(
                        type="text",
                        text="Error: geopandas is not installed. Install with: pip install geopandas",
                    )
                ]
            except Exception as e:
                return [TextContent(type="text", text=f"Error reading vector: {str(e)}")]

        elif name == "list_basemaps":
            try:
                from leafmap import basemaps as bm

                basemap_list = []
                for attr in dir(bm):
                    if not attr.startswith("_"):
                        obj = getattr(bm, attr)
                        if isinstance(obj, dict) and "url" in obj:
                            basemap_list.append(
                                {
                                    "name": attr,
                                    "display_name": obj.get("name", attr),
                                    "url": obj.get("url", ""),
                                    "attribution": obj.get("attribution", ""),
                                }
                            )

                result = {
                    "count": len(basemap_list),
                    "basemaps": basemap_list,
                }

                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            except Exception as e:
                return [TextContent(type="text", text=f"Error listing basemaps: {str(e)}")]

        elif name == "convert_coordinates":
            x = arguments["x"]
            y = arguments["y"]
            from_crs = arguments["from_crs"]
            to_crs = arguments["to_crs"]

            try:
                from pyproj import Transformer

                transformer = Transformer.from_crs(from_crs, to_crs, always_xy=True)
                new_x, new_y = transformer.transform(x, y)

                result = {
                    "input": {"x": x, "y": y, "crs": from_crs},
                    "output": {"x": new_x, "y": new_y, "crs": to_crs},
                }

                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            except ImportError:
                return [
                    TextContent(
                        type="text",
                        text="Error: pyproj is not installed. Install with: pip install pyproj",
                    )
                ]
            except Exception as e:
                return [TextContent(type="text", text=f"Error converting coordinates: {str(e)}")]

        elif name == "get_crs_info":
            crs_code = arguments["crs_code"]

            try:
                from pyproj import CRS

                crs = CRS.from_string(crs_code)

                info = {
                    "code": crs_code,
                    "name": crs.name,
                    "type": crs.type_name,
                    "axis_info": [
                        {"name": axis.name, "abbrev": axis.abbrev, "direction": axis.direction, "unit": str(axis.unit_name)}
                        for axis in crs.axis_info
                    ],
                    "area_of_use": {
                        "name": crs.area_of_use.name if crs.area_of_use else None,
                        "bounds": {
                            "west": crs.area_of_use.west,
                            "south": crs.area_of_use.south,
                            "east": crs.area_of_use.east,
                            "north": crs.area_of_use.north,
                        } if crs.area_of_use else None,
                    },
                    "datum": crs.datum.name if crs.datum else None,
                    "coordinate_system": crs.coordinate_system.name if hasattr(crs, 'coordinate_system') and crs.coordinate_system else None,
                }

                return [TextContent(type="text", text=json.dumps(info, indent=2))]
            except ImportError:
                return [
                    TextContent(
                        type="text",
                        text="Error: pyproj is not installed. Install with: pip install pyproj",
                    )
                ]
            except Exception as e:
                return [TextContent(type="text", text=f"Error getting CRS info: {str(e)}")]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        logger.error(f"Error in tool {name}: {str(e)}", exc_info=True)
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Run the MCP server."""
    logger.info("Starting Leafmap MCP Server")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
