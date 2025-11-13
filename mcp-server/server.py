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
        Resource(
            uri="leafmap://docs/backends",
            name="Mapping Backends Guide",
            mimeType="text/plain",
            description="Guide to using different mapping backends (ipyleaflet, folium, etc.)",
        ),
        Resource(
            uri="leafmap://examples/ipyleaflet",
            name="ipyleaflet Examples",
            mimeType="text/plain",
            description="Code examples for using leafmap with ipyleaflet backend",
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

    elif uri == "leafmap://docs/backends":
        return """Leafmap Mapping Backends Guide

Leafmap supports multiple mapping backends, each with its own strengths:

## 1. ipyleaflet (Default in Jupyter)

The default backend for Jupyter environments. Provides interactive widgets
and bidirectional communication between Python and the map.

**Installation:**
    pip install leafmap
    # ipyleaflet is included by default

**Usage:**
    import leafmap

    # Create map with ipyleaflet (default in Jupyter)
    m = leafmap.Map(center=[40, -100], zoom=4)

    # Add basemap
    m.add_basemap("OpenTopoMap")

    # Add vector data
    m.add_vector("path/to/file.geojson", layer_name="My Data")

    # Add raster data
    m.add_raster("path/to/file.tif", colormap="terrain")

    # Display map
    m

**Key Features:**
- Interactive Jupyter widgets
- Bidirectional Python ↔ JavaScript communication
- Drawing tools and layer controls
- Split-panel maps
- Time series animations

## 2. folium

Static HTML map generation, great for embedding in web pages.
Automatically used in marimo notebooks and when USE_MKDOCS is set.

**Installation:**
    pip install leafmap  # folium included by default

**Usage:**
    import leafmap.foliumap as leafmap

    # Or let leafmap auto-detect
    m = leafmap.Map(center=[40, -100], zoom=4)
    m.add_basemap("OpenStreetMap")

    # Save to HTML
    m.save("map.html")

**Key Features:**
- Standalone HTML output
- No Python kernel required after generation
- Good for static reports and websites

## 3. plotly

Interactive maps with Plotly's powerful visualization capabilities.

**Installation:**
    pip install "leafmap[backends]"

**Usage:**
    import leafmap.plotlymap as leafmap

    m = leafmap.Map()
    m.add_basemap()

## 4. pydeck

WebGL-powered maps for large datasets, based on deck.gl.

**Installation:**
    pip install "leafmap[backends]"

**Usage:**
    import leafmap.deck as leafmap

    m = leafmap.Map()
    m.add_vector("large_dataset.geojson")

## 5. kepler.gl

Advanced geospatial data visualization.

**Installation:**
    pip install "leafmap[backends]"

**Usage:**
    import leafmap.kepler as leafmap

    m = leafmap.Map()
    m.add_data(gdf, name="My Data")

## 6. maplibre / MapLibre GL JS

Modern vector tile rendering with excellent performance.

**Installation:**
    pip install "leafmap[maplibre]"

**Usage:**
    from leafmap import maplibregl

    m = maplibregl.Map(style="dark-matter")
    m.add_vector("data.geojson")

## Backend Selection

Leafmap automatically chooses the appropriate backend:
- Jupyter Notebook/Lab: ipyleaflet
- Google Colab: ipyleaflet
- Marimo notebooks: folium
- Documentation builds: folium (when USE_MKDOCS is set)

**Force a specific backend:**
    # Use folium
    from leafmap.foliumap import Map

    # Use ipyleaflet
    from leafmap.leafmap import Map

    # Use pydeck
    from leafmap.deck import Map

For more information, visit: https://leafmap.org
"""

    elif uri == "leafmap://examples/ipyleaflet":
        return """Leafmap with ipyleaflet Backend - Code Examples

## Basic Map Creation

```python
import leafmap

# Create a basic map
m = leafmap.Map(center=[40, -100], zoom=4)
m
```

## Adding Basemaps

```python
# Add a single basemap
m = leafmap.Map()
m.add_basemap("OpenTopoMap")

# Or use built-in basemaps
m = leafmap.Map(basemap="HYBRID")  # Satellite + labels

# Available basemaps
leafmap.basemaps.keys()  # List all available basemaps
```

## Adding Vector Data

```python
# From file
m = leafmap.Map()
m.add_vector(
    "path/to/file.geojson",
    layer_name="My Boundaries",
    style={"color": "blue", "fillOpacity": 0.3}
)

# From GeoDataFrame
import geopandas as gpd
gdf = gpd.read_file("data.geojson")
m.add_gdf(gdf, layer_name="Data Layer")

# From URL
url = "https://raw.githubusercontent.com/opengeos/leafmap/master/examples/data/cable_geo.geojson"
m.add_geojson(url, layer_name="Cables")
```

## Adding Raster Data

```python
# Add GeoTIFF
m = leafmap.Map()
m.add_raster(
    "dem.tif",
    layer_name="Elevation",
    colormap="terrain",
    vmin=0,
    vmax=3000
)

# Add Cloud Optimized GeoTIFF (COG)
url = "https://example.com/data.tif"
m.add_cog_layer(url, name="COG Layer")

# Add local tile server
m.add_local_tile("large_raster.tif")
```

## Split-Panel Maps

```python
# Compare two basemaps
m = leafmap.Map(center=[40, -100], zoom=4)
m.split_map(
    left_layer="OpenStreetMap",
    right_layer="Esri.WorldImagery"
)

# Compare raster datasets
m = leafmap.Map()
m.split_map(
    left_layer="before.tif",
    right_layer="after.tif"
)
```

## Drawing and Editing

```python
# Enable drawing tools
m = leafmap.Map()
m.add_basemap("OpenStreetMap")

# Draw shapes interactively, then access them
# (Use the drawing toolbar in the map interface)

# Get drawn features
if hasattr(m, 'draw_features'):
    features = m.draw_features
    print(features)
```

## Layer Control and Legends

```python
# Add multiple layers with control
m = leafmap.Map()
m.add_basemap("OpenStreetMap")
m.add_raster("elevation.tif", layer_name="Elevation")
m.add_vector("boundaries.geojson", layer_name="Boundaries")

# Add custom legend
legend_dict = {
    "Forest": "#228B22",
    "Water": "#4169E1",
    "Urban": "#FF6347"
}
m.add_legend(title="Land Cover", legend_dict=legend_dict)

# Add colorbar for raster
m.add_colorbar(
    vmin=0,
    vmax=100,
    palette="terrain",
    label="Elevation (m)"
)
```

## STAC Catalogs

```python
# Search and visualize STAC data
m = leafmap.Map()

# Microsoft Planetary Computer
m.add_stac_layer(
    url="https://planetarycomputer.microsoft.com/api/stac/v1",
    collection="landsat-c2-l2",
    item="LC08_L2SP_047027_20201204_02_T1",
    bands=["SR_B4", "SR_B3", "SR_B2"],
    name="Landsat 8"
)
```

## Interactive Widgets

```python
# Add layer controls
m = leafmap.Map()
m.add_basemap("OpenStreetMap")
m.add_layer_control()

# Add measure tool
m.add_measure_control()

# Add fullscreen control
m.add_fullscreen_control()

# Add scale bar
m.add_scale_control()
```

## Time Series Animation

```python
# Create animation from raster time series
import glob

files = glob.glob("timeseries/*.tif")
m = leafmap.Map()
m.add_time_slider(
    files,
    layer_name="Time Series",
    date_format="YYYY-MM-DD"
)
```

## Choropleth Maps

```python
import geopandas as gpd

# Load data
gdf = gpd.read_file("counties.geojson")

# Create choropleth
m = leafmap.Map()
m.add_data(
    gdf,
    column="population",
    scheme="Quantiles",
    cmap="YlOrRd",
    legend_title="Population"
)
```

## Heatmaps

```python
# Create heatmap from points
m = leafmap.Map(center=[40, -100], zoom=4)
m.add_heatmap(
    "points.csv",
    latitude="lat",
    longitude="lon",
    value="intensity",
    name="Heatmap"
)
```

## Marker Clusters

```python
# Add marker cluster from CSV
m = leafmap.Map()
m.add_points_from_csv(
    "locations.csv",
    x="longitude",
    y="latitude",
    layer_name="Locations",
    cluster=True
)
```

## Exporting

```python
# Save map as HTML
m.to_html("map.html")

# Take screenshot (requires selenium)
m.to_image("map.png")

# Export drawn features to GeoJSON
m.save_draw_features("drawn_features.geojson")
```

## Advanced: Custom JavaScript

```python
# Execute custom JavaScript
m = leafmap.Map()
m.add_basemap("OpenStreetMap")

# Add custom behavior
js_code = '''
function onMapClick(e) {
    alert("You clicked at " + e.latlng);
}
map.on('click', onMapClick);
'''
m.execute_javascript(js_code)
```

For more examples, visit:
- https://leafmap.org/notebooks/
- https://github.com/opengeos/leafmap/tree/master/examples
"""

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
        Tool(
            name="generate_code",
            description="Generate Python code snippets for common leafmap tasks. Returns ready-to-use "
            "code examples for the specified task with the ipyleaflet or other backends.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The task to generate code for (e.g., 'create_map', 'add_vector', "
                        "'add_raster', 'split_map', 'add_basemap', 'draw_features', 'choropleth', etc.)",
                    },
                    "backend": {
                        "type": "string",
                        "description": "The backend to use (default: 'ipyleaflet'). Options: 'ipyleaflet', "
                        "'folium', 'plotly', 'pydeck', 'kepler', 'maplibre'",
                        "default": "ipyleaflet",
                    },
                    "file_path": {
                        "type": "string",
                        "description": "Optional file path to use in the code example",
                    },
                },
                "required": ["task"],
            },
        ),
        Tool(
            name="csv_to_map_helper",
            description="Generate code to convert CSV/Excel files with coordinates to interactive maps. "
            "Supports various formats including points, heatmaps, and marker clusters.",
            inputSchema={
                "type": "object",
                "properties": {
                    "csv_path": {
                        "type": "string",
                        "description": "Path to the CSV file",
                    },
                    "lat_column": {
                        "type": "string",
                        "description": "Name of the latitude column (default: 'latitude')",
                        "default": "latitude",
                    },
                    "lon_column": {
                        "type": "string",
                        "description": "Name of the longitude column (default: 'longitude')",
                        "default": "longitude",
                    },
                    "map_type": {
                        "type": "string",
                        "description": "Type of map: 'points', 'heatmap', or 'cluster' (default: 'points')",
                        "default": "points",
                    },
                },
                "required": ["csv_path"],
            },
        ),
        Tool(
            name="search_whitebox_tools",
            description="Search through WhiteboxTools' 468+ geoprocessing functions by keyword or category. "
            "Returns tool names, descriptions, and usage examples for geospatial analysis tasks.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search term (e.g., 'slope', 'watershed', 'lidar', 'filter')",
                    },
                    "category": {
                        "type": "string",
                        "description": "Tool category: 'Hydrology', 'Terrain', 'LiDAR', 'Image', 'Math', 'Stream'",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="suggest_colormap",
            description="Recommend appropriate colormaps for different types of geospatial data. "
            "Provides colormap names and usage examples for elevation, temperature, categorical data, etc.",
            inputSchema={
                "type": "object",
                "properties": {
                    "data_type": {
                        "type": "string",
                        "description": "Type of data: 'elevation', 'temperature', 'precipitation', 'vegetation', "
                        "'categorical', 'diverging', 'sequential', 'bathymetry', 'population'",
                    },
                },
                "required": ["data_type"],
            },
        ),
        Tool(
            name="list_data_sources",
            description="List available public geospatial data sources and APIs that work with leafmap. "
            "Includes STAC catalogs, OpenStreetMap, building footprints, elevation data, and more.",
            inputSchema={
                "type": "object",
                "properties": {
                    "data_category": {
                        "type": "string",
                        "description": "Category: 'satellite', 'elevation', 'vector', 'basemaps', 'stac', "
                        "'buildings', 'hydrology', 'land_cover', 'all'",
                        "default": "all",
                    },
                },
                "required": [],
            },
        ),
        Tool(
            name="plan_workflow",
            description="Help plan multi-step geospatial workflows by suggesting a sequence of operations. "
            "Breaks down complex tasks into manageable steps with code examples.",
            inputSchema={
                "type": "object",
                "properties": {
                    "goal": {
                        "type": "string",
                        "description": "The analysis goal (e.g., 'create elevation map from STAC data', "
                        "'analyze watershed boundaries', 'visualize time series satellite imagery')",
                    },
                },
                "required": ["goal"],
            },
        ),
        Tool(
            name="create_notebook",
            description="Create a Jupyter notebook with generated code for a specific geospatial task. "
            "Automatically generates cells with imports, code, markdown explanations, and saves to disk.",
            inputSchema={
                "type": "object",
                "properties": {
                    "goal": {
                        "type": "string",
                        "description": "The analysis goal (e.g., 'create watershed map', 'visualize CSV points')",
                    },
                    "output_path": {
                        "type": "string",
                        "description": "Path where the notebook should be saved (e.g., 'watershed_analysis.ipynb')",
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Optional parameters like file paths, coordinates, etc.",
                    },
                },
                "required": ["goal", "output_path"],
            },
        ),
        Tool(
            name="execute_workflow",
            description="Generate, create, and execute a complete Jupyter notebook for a geospatial workflow. "
            "This tool creates the notebook, runs it, captures outputs, and returns results including any "
            "generated maps, images, or data files. Optionally opens the executed notebook automatically.",
            inputSchema={
                "type": "object",
                "properties": {
                    "goal": {
                        "type": "string",
                        "description": "The analysis goal (e.g., 'create and display watershed', 'make heatmap from CSV')",
                    },
                    "working_directory": {
                        "type": "string",
                        "description": "Directory where notebook and outputs will be saved (default: current directory)",
                        "default": ".",
                    },
                    "parameters": {
                        "type": "object",
                        "description": "Task-specific parameters (file paths, coordinates, options, etc.)",
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Maximum execution time in seconds (default: 300)",
                        "default": 300,
                    },
                    "open_notebook": {
                        "type": "boolean",
                        "description": "Automatically open the executed notebook in browser (default: true)",
                        "default": True,
                    },
                    "output_format": {
                        "type": "string",
                        "description": "Format for viewing: 'html' (browser), 'jupyter' (notebook server), or 'none' (default: 'html')",
                        "default": "html",
                    },
                },
                "required": ["goal"],
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

        elif name == "generate_code":
            task = arguments["task"].lower()
            backend = arguments.get("backend", "ipyleaflet")
            file_path = arguments.get("file_path", "path/to/file")

            code_templates = {
                "create_map": {
                    "ipyleaflet": f"""import leafmap

# Create an interactive map
m = leafmap.Map(center=[40, -100], zoom=4)
m  # Display in Jupyter
""",
                    "folium": f"""import leafmap.foliumap as leafmap

# Create a folium map
m = leafmap.Map(center=[40, -100], zoom=4)
m  # Display in Jupyter or save as HTML
""",
                    "maplibre": f"""from leafmap import maplibregl

# Create a MapLibre map
m = maplibregl.Map(style="dark-matter", center=[-100, 40], zoom=4)
m
""",
                },
                "add_vector": {
                    "ipyleaflet": f"""import leafmap

m = leafmap.Map()
m.add_vector(
    "{file_path}",
    layer_name="Vector Layer",
    style={{"color": "blue", "fillOpacity": 0.3}}
)
m
""",
                    "folium": f"""import leafmap.foliumap as leafmap

m = leafmap.Map()
m.add_vector("{file_path}", layer_name="Vector Layer")
m
""",
                },
                "add_raster": {
                    "ipyleaflet": f"""import leafmap

m = leafmap.Map()
m.add_raster(
    "{file_path}",
    layer_name="Raster Layer",
    colormap="terrain",
    vmin=0,
    vmax=1000
)
m
""",
                    "folium": f"""import leafmap.foliumap as leafmap

m = leafmap.Map()
m.add_raster("{file_path}", layer_name="Raster Layer")
m
""",
                },
                "add_basemap": {
                    "ipyleaflet": f"""import leafmap

m = leafmap.Map()
m.add_basemap("OpenTopoMap")  # Or "HYBRID", "Esri.WorldImagery", etc.
m
""",
                    "folium": f"""import leafmap.foliumap as leafmap

m = leafmap.Map()
m.add_basemap("OpenTopoMap")
m
""",
                },
                "split_map": {
                    "ipyleaflet": f"""import leafmap

m = leafmap.Map(center=[40, -100], zoom=4)
m.split_map(
    left_layer="OpenStreetMap",
    right_layer="Esri.WorldImagery"
)
m
""",
                },
                "choropleth": {
                    "ipyleaflet": f"""import leafmap
import geopandas as gpd

# Load your data
gdf = gpd.read_file("{file_path}")

# Create choropleth map
m = leafmap.Map()
m.add_data(
    gdf,
    column="population",  # Column to visualize
    scheme="Quantiles",   # Classification scheme
    cmap="YlOrRd",        # Colormap
    legend_title="Population"
)
m
""",
                },
                "heatmap": {
                    "ipyleaflet": f"""import leafmap

m = leafmap.Map(center=[40, -100], zoom=4)
m.add_heatmap(
    "{file_path}",  # CSV or GeoJSON with points
    latitude="lat",
    longitude="lon",
    value="intensity",
    name="Heatmap",
    radius=15
)
m
""",
                },
                "draw_features": {
                    "ipyleaflet": f"""import leafmap

m = leafmap.Map()
m.add_basemap("OpenStreetMap")

# Draw features using the drawing toolbar in the map interface
# After drawing, access the features:
# features = m.draw_features

# To save drawn features:
# m.save_draw_features("output.geojson")
m
""",
                },
                "time_series": {
                    "ipyleaflet": f"""import leafmap
import glob

# Get list of time series files
files = glob.glob("timeseries/*.tif")

m = leafmap.Map()
m.add_time_slider(
    files,
    layer_name="Time Series",
    date_format="YYYY-MM-DD"
)
m
""",
                },
                "stac": {
                    "ipyleaflet": f"""import leafmap

m = leafmap.Map()

# Add data from STAC catalog
m.add_stac_layer(
    url="https://planetarycomputer.microsoft.com/api/stac/v1",
    collection="landsat-c2-l2",
    item="LC08_L2SP_047027_20201204_02_T1",
    bands=["SR_B4", "SR_B3", "SR_B2"],
    name="Landsat 8"
)
m
""",
                },
            }

            # Try to find the template
            if task in code_templates and backend in code_templates[task]:
                code = code_templates[task][backend]
            elif task in code_templates and "ipyleaflet" in code_templates[task]:
                # Fallback to ipyleaflet if backend not found
                code = code_templates[task]["ipyleaflet"]
            else:
                # Generate a generic template
                code = f"""import leafmap

# {task.replace('_', ' ').title()}
m = leafmap.Map()
# Add your code here for: {task}
m
"""

            result = {
                "task": task,
                "backend": backend,
                "code": code,
                "instructions": f"Copy and paste this code into a Jupyter notebook or Python script to {task.replace('_', ' ')}.",
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "csv_to_map_helper":
            csv_path = arguments["csv_path"]
            lat_col = arguments.get("lat_column", "latitude")
            lon_col = arguments.get("lon_column", "longitude")
            map_type = arguments.get("map_type", "points")

            code_templates = {
                "points": f"""import leafmap

# Load CSV and create map with points
m = leafmap.Map()
m.add_points_from_xy(
    "{csv_path}",
    x="{lon_col}",
    y="{lat_col}",
    layer_name="Points"
)
m
""",
                "heatmap": f"""import leafmap

# Create heatmap from CSV
m = leafmap.Map()
m.add_heatmap(
    "{csv_path}",
    latitude="{lat_col}",
    longitude="{lon_col}",
    name="Heatmap",
    radius=15
)
m
""",
                "cluster": f"""import leafmap

# Create marker cluster from CSV
m = leafmap.Map()
m.add_points_from_xy(
    "{csv_path}",
    x="{lon_col}",
    y="{lat_col}",
    layer_name="Locations",
    icon_names=["map-marker"],
    spin=True,
    add_marker_cluster=True
)
m
""",
            }

            code = code_templates.get(map_type, code_templates["points"])

            result = {
                "csv_path": csv_path,
                "lat_column": lat_col,
                "lon_column": lon_col,
                "map_type": map_type,
                "code": code,
                "tutorial_reference": "See tutorial #9 (CSV to points) at https://leafmap.org/notebooks/09_csv_to_points",
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "search_whitebox_tools":
            query = arguments.get("query", "").lower()
            category = arguments.get("category", "").lower()

            # Comprehensive whitebox tools database
            whitebox_tools = {
                "Hydrology": [
                    {"name": "BreachDepressions", "description": "Removes depressions in a DEM by breaching"},
                    {"name": "FillDepressions", "description": "Fills all depressions in a DEM"},
                    {"name": "D8FlowAccumulation", "description": "Calculates flow accumulation using D8 algorithm"},
                    {"name": "D8Pointer", "description": "Calculates D8 flow direction"},
                    {"name": "DInfFlowAccumulation", "description": "D-infinity flow accumulation"},
                    {"name": "Watershed", "description": "Identifies watersheds/drainage basins"},
                    {"name": "StreamOrder", "description": "Assigns stream order (Strahler, Horton, Shreve)"},
                    {"name": "ExtractStreams", "description": "Extract stream networks from flow accumulation"},
                ],
                "Terrain": [
                    {"name": "Slope", "description": "Calculates slope from DEM"},
                    {"name": "Aspect", "description": "Calculates aspect (direction) from DEM"},
                    {"name": "Hillshade", "description": "Creates hillshade visualization"},
                    {"name": "Curvature", "description": "Calculates curvature (plan, profile, tangential)"},
                    {"name": "RuggednessIndex", "description": "Terrain ruggedness index"},
                    {"name": "Wetness Index", "description": "Topographic wetness index"},
                    {"name": "ElevationAboveStream", "description": "Height above nearest stream"},
                ],
                "LiDAR": [
                    {"name": "LidarGroundPointFilter", "description": "Filters LiDAR points to ground returns"},
                    {"name": "LidarTophatTransform", "description": "Removes background from LiDAR"},
                    {"name": "LidarIdwInterpolation", "description": "Interpolates LiDAR to raster"},
                    {"name": "LidarTINGridding", "description": "Creates TIN from LiDAR points"},
                    {"name": "ClassifyOverlapPoints", "description": "Identifies overlapping points"},
                ],
                "Image": [
                    {"name": "GaussianFilter", "description": "Gaussian blur filter"},
                    {"name": "MedianFilter", "description": "Median filter for noise removal"},
                    {"name": "EdgeDetection", "description": "Detect edges in raster"},
                    {"name": "HistogramMatching", "description": "Match histogram between images"},
                    {"name": "Mosaic", "description": "Mosaic multiple rasters"},
                ],
                "Math": [
                    {"name": "Add", "description": "Add two rasters or value to raster"},
                    {"name": "Multiply", "description": "Multiply rasters"},
                    {"name": "ZonalStatistics", "description": "Calculate statistics by zone"},
                    {"name": "Reclassify", "description": "Reclassify raster values"},
                ],
            }

            results = []

            # Search by query
            if query:
                for cat, tools in whitebox_tools.items():
                    for tool in tools:
                        if query in tool["name"].lower() or query in tool["description"].lower():
                            results.append({
                                "category": cat,
                                "name": tool["name"],
                                "description": tool["description"],
                            })

            # Filter by category
            elif category:
                matching_cat = None
                for cat in whitebox_tools.keys():
                    if category in cat.lower():
                        matching_cat = cat
                        break

                if matching_cat:
                    for tool in whitebox_tools[matching_cat]:
                        results.append({
                            "category": matching_cat,
                            "name": tool["name"],
                            "description": tool["description"],
                        })
            else:
                # Return categories if no search
                results = [{"category": cat, "tool_count": len(tools)} for cat, tools in whitebox_tools.items()]

            example_code = """import leafmap

# Initialize WhiteboxTools
wbt = leafmap.WhiteboxTools()

# Example: Calculate slope
wbt.slope("dem.tif", "slope.tif")

# See tutorial #8 at: https://leafmap.org/notebooks/08_whitebox
"""

            result = {
                "query": query or "none",
                "category": category or "none",
                "results": results[:20],  # Limit to 20 results
                "total_tools": "468+",
                "example_code": example_code,
                "documentation": "https://www.whiteboxgeo.com/manual/wbt_book/available_tools/index.html",
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "suggest_colormap":
            data_type = arguments["data_type"].lower()

            colormap_recommendations = {
                "elevation": {
                    "recommended": ["terrain", "gist_earth", "Spectral_r"],
                    "description": "Terrain shows natural earth tones, ideal for elevation/topography",
                    "example": """m.add_raster("elevation.tif", colormap="terrain", vmin=0, vmax=3000)""",
                },
                "temperature": {
                    "recommended": ["RdYlBu_r", "coolwarm", "turbo"],
                    "description": "Red-Yellow-Blue (reversed) shows cold (blue) to hot (red)",
                    "example": """m.add_raster("temperature.tif", colormap="RdYlBu_r", vmin=-10, vmax=40)""",
                },
                "precipitation": {
                    "recommended": ["YlGnBu", "Blues", "PuBu"],
                    "description": "Blue gradients represent water/rainfall naturally",
                    "example": """m.add_raster("rainfall.tif", colormap="YlGnBu", vmin=0, vmax=500)""",
                },
                "vegetation": {
                    "recommended": ["Greens", "YlGn", "RdYlGn"],
                    "description": "Green gradients for NDVI, biomass, or vegetation indices",
                    "example": """m.add_raster("ndvi.tif", colormap="Greens", vmin=0, vmax=1)""",
                },
                "categorical": {
                    "recommended": ["tab10", "Set3", "Paired"],
                    "description": "Distinct colors for land cover, soil types, zones",
                    "example": """m.add_raster("landcover.tif", colormap="tab10")""",
                },
                "diverging": {
                    "recommended": ["RdBu_r", "BrBG", "PiYG"],
                    "description": "For data with meaningful center (e.g., change detection)",
                    "example": """m.add_raster("change.tif", colormap="RdBu_r", vmin=-100, vmax=100)""",
                },
                "sequential": {
                    "recommended": ["viridis", "plasma", "inferno"],
                    "description": "Perceptually uniform, colorblind-friendly sequential data",
                    "example": """m.add_raster("population.tif", colormap="viridis")""",
                },
                "bathymetry": {
                    "recommended": ["ocean", "deep", "Blues_r"],
                    "description": "Blue gradients for ocean depth/bathymetry",
                    "example": """m.add_raster("bathymetry.tif", colormap="ocean", vmin=-5000, vmax=0)""",
                },
                "population": {
                    "recommended": ["YlOrRd", "Reds", "hot"],
                    "description": "Yellow to red shows density/intensity",
                    "example": """m.add_raster("population.tif", colormap="YlOrRd", vmin=0, vmax=10000)""",
                },
            }

            recommendation = colormap_recommendations.get(data_type)

            if not recommendation:
                # Provide general guidance
                result = {
                    "data_type": data_type,
                    "error": f"Unknown data type: {data_type}",
                    "available_types": list(colormap_recommendations.keys()),
                    "default_recommendation": "viridis (perceptually uniform, colorblind-friendly)",
                }
            else:
                result = {
                    "data_type": data_type,
                    "recommended_colormaps": recommendation["recommended"],
                    "description": recommendation["description"],
                    "example_code": recommendation["example"],
                    "all_colormaps_url": "https://matplotlib.org/stable/tutorials/colors/colormaps.html",
                    "tutorial_reference": "See tutorial #23 at: https://leafmap.org/notebooks/23_colormaps",
                }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "list_data_sources":
            category = arguments.get("data_category", "all").lower()

            data_sources = {
                "stac": [
                    {
                        "name": "Microsoft Planetary Computer",
                        "url": "https://planetarycomputer.microsoft.com/api/stac/v1",
                        "description": "Petabytes of satellite imagery and environmental data",
                        "tutorial": "#37",
                    },
                    {
                        "name": "Earth Search (AWS)",
                        "url": "https://earth-search.aws.element84.com/v1",
                        "description": "Sentinel-2, Landsat, and more on AWS",
                        "tutorial": "#64, #73",
                    },
                    {
                        "name": "USGS STAC",
                        "url": "https://landsatlook.usgs.gov/stac-server",
                        "description": "Landsat and other USGS data",
                        "tutorial": "#64",
                    },
                ],
                "elevation": [
                    {
                        "name": "National Elevation Dataset (NED)",
                        "source": "USGS",
                        "description": "10m, 30m elevation data for USA",
                        "tutorial": "#56",
                        "code": "leafmap.download_ned(bbox, output='ned.tif')",
                    },
                    {
                        "name": "The National Map",
                        "source": "USGS",
                        "description": "Topographic maps and elevation",
                        "tutorial": "#57",
                    },
                    {
                        "name": "SRTM",
                        "source": "NASA",
                        "description": "Global 30m/90m elevation",
                        "tutorial": "#88",
                    },
                ],
                "satellite": [
                    {
                        "name": "Landsat",
                        "source": "USGS/NASA",
                        "description": "30m multispectral, since 1972",
                        "access": "STAC catalogs",
                    },
                    {
                        "name": "Sentinel-2",
                        "source": "ESA",
                        "description": "10m multispectral, global coverage",
                        "access": "STAC catalogs",
                    },
                    {
                        "name": "MODIS",
                        "source": "NASA",
                        "description": "Daily global coverage, 250m-1km",
                        "access": "NASA Earth Data",
                        "tutorial": "#88",
                    },
                    {
                        "name": "Maxar Open Data",
                        "source": "Maxar",
                        "description": "High-res imagery for disasters",
                        "tutorial": "#67, #69",
                    },
                ],
                "buildings": [
                    {
                        "name": "Microsoft Building Footprints",
                        "source": "Microsoft",
                        "description": "AI-extracted building footprints globally",
                        "tutorial": "#81",
                        "code": "leafmap.download_ms_buildings(location='City')",
                    },
                    {
                        "name": "Google Building Footprints",
                        "source": "Google",
                        "description": "Building footprints for many countries",
                        "tutorial": "#81",
                    },
                    {
                        "name": "Overture Maps Buildings",
                        "source": "Overture Maps",
                        "description": "Global building data",
                        "tutorial": "#97, #102",
                    },
                ],
                "vector": [
                    {
                        "name": "OpenStreetMap",
                        "source": "OSM",
                        "description": "Global vector data - roads, buildings, POIs",
                        "tutorial": "#15",
                        "code": "m.add_osm_from_geocode('City Name')",
                    },
                    {
                        "name": "Natural Earth",
                        "source": "Natural Earth",
                        "description": "Cultural and physical vectors",
                        "url": "https://www.naturalearthdata.com/",
                    },
                ],
                "hydrology": [
                    {
                        "name": "National Hydrography Dataset (NHD)",
                        "source": "USGS",
                        "description": "Stream networks, watersheds for USA",
                        "tutorial": "#98",
                        "code": "leafmap.get_nhd(basin_id)",
                    },
                    {
                        "name": "National Wetlands Inventory (NWI)",
                        "source": "USFWS",
                        "description": "Wetland boundaries for USA",
                        "tutorial": "#99",
                        "code": "leafmap.get_nwi(bbox)",
                    },
                ],
                "land_cover": [
                    {
                        "name": "National Land Cover Database (NLCD)",
                        "source": "USGS",
                        "description": "30m land cover for USA",
                        "tutorial": "#100",
                    },
                    {
                        "name": "Dynamic World",
                        "source": "Google",
                        "description": "Global 10m land cover, near real-time",
                        "access": "Google Earth Engine",
                    },
                    {
                        "name": "ESA WorldCover",
                        "source": "ESA",
                        "description": "Global 10m land cover",
                        "access": "STAC catalogs",
                    },
                ],
            }

            if category == "all":
                result = {
                    "categories": list(data_sources.keys()),
                    "total_sources": sum(len(sources) for sources in data_sources.values()),
                    "usage": "Call this tool again with a specific category to see details",
                }
            else:
                matching_sources = data_sources.get(category, [])
                result = {
                    "category": category,
                    "sources": matching_sources,
                    "count": len(matching_sources),
                }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "plan_workflow":
            goal = arguments["goal"].lower()

            # Workflow templates based on common patterns
            workflow_plans = []

            if "stac" in goal or "satellite" in goal:
                workflow_plans.append({
                    "workflow": "STAC Satellite Imagery Workflow",
                    "steps": [
                        {
                            "step": 1,
                            "action": "Search STAC catalog",
                            "code": """import leafmap
m = leafmap.Map()
# Search catalog interactively or via API
""",
                            "tutorial": "#64, #73"
                        },
                        {
                            "step": 2,
                            "action": "Add STAC item to map",
                            "code": """m.add_stac_layer(
    url="https://planetarycomputer.microsoft.com/api/stac/v1",
    collection="landsat-c2-l2",
    item="ITEM_ID",
    bands=["SR_B4", "SR_B3", "SR_B2"]
)""",
                            "tutorial": "#37"
                        },
                        {
                            "step": 3,
                            "action": "Visualize with appropriate colormap",
                            "code": "# Use colormap suggestions from suggest_colormap tool",
                        }
                    ]
                })

            if "elevation" in goal or "dem" in goal or "terrain" in goal:
                workflow_plans.append({
                    "workflow": "Elevation/Terrain Analysis",
                    "steps": [
                        {
                            "step": 1,
                            "action": "Download elevation data",
                            "code": """import leafmap
leafmap.download_ned(bbox, output='elevation.tif')
""",
                            "tutorial": "#56, #57"
                        },
                        {
                            "step": 2,
                            "action": "Calculate terrain derivatives",
                            "code": """wbt = leafmap.WhiteboxTools()
wbt.slope("elevation.tif", "slope.tif")
wbt.aspect("elevation.tif", "aspect.tif")
wbt.hillshade("elevation.tif", "hillshade.tif")
""",
                            "tutorial": "#8"
                        },
                        {
                            "step": 3,
                            "action": "Visualize results",
                            "code": """m = leafmap.Map()
m.add_raster("slope.tif", colormap="terrain")
""",
                        }
                    ]
                })

            if "time series" in goal or "timeseries" in goal or "animation" in goal:
                workflow_plans.append({
                    "workflow": "Time Series Animation",
                    "steps": [
                        {
                            "step": 1,
                            "action": "Collect time series images",
                            "code": """import glob
files = glob.glob("timeseries/*.tif")
files.sort()  # Ensure chronological order
""",
                            "tutorial": "#72"
                        },
                        {
                            "step": 2,
                            "action": "Create time slider or animation",
                            "code": """m = leafmap.Map()
m.add_time_slider(
    files,
    layer_name="Time Series",
    date_format="YYYY-MM-DD"
)
""",
                            "tutorial": "#22, #79"
                        }
                    ]
                })

            if "csv" in goal or "points" in goal:
                workflow_plans.append({
                    "workflow": "CSV/Point Data Visualization",
                    "steps": [
                        {
                            "step": 1,
                            "action": "Load CSV with coordinates",
                            "code": "# Use csv_to_map_helper tool for code generation",
                            "tutorial": "#9, #34"
                        },
                        {
                            "step": 2,
                            "action": "Choose visualization style",
                            "options": ["Points", "Heatmap", "Marker Cluster"],
                            "tutorial": "#24 (heatmap), #50 (clusters)"
                        }
                    ]
                })

            if "watershed" in goal or "hydrology" in goal:
                workflow_plans.append({
                    "workflow": "Watershed/Hydrology Analysis",
                    "steps": [
                        {
                            "step": 1,
                            "action": "Prepare DEM",
                            "code": """wbt = leafmap.WhiteboxTools()
wbt.breach_depressions("dem.tif", "dem_breached.tif")
wbt.d8_pointer("dem_breached.tif", "d8_pointer.tif")
""",
                            "tutorial": "#8, #55"
                        },
                        {
                            "step": 2,
                            "action": "Calculate flow accumulation",
                            "code": """wbt.d8_flow_accumulation("d8_pointer.tif", "flow_accum.tif")
""",
                        },
                        {
                            "step": 3,
                            "action": "Delineate watersheds",
                            "code": """wbt.watershed("d8_pointer.tif", pour_pts, "watershed.tif")
# Or get from NHD: leafmap.get_nhd(basin_id)
""",
                            "tutorial": "#98"
                        }
                    ]
                })

            if not workflow_plans:
                # Generic workflow
                workflow_plans.append({
                    "workflow": "General Geospatial Analysis",
                    "steps": [
                        {"step": 1, "action": "Create map and add data", "tutorial": "#1"},
                        {"step": 2, "action": "Apply appropriate styling/colormap"},
                        {"step": 3, "action": "Add legends and controls", "tutorial": "#6, #7"},
                        {"step": 4, "action": "Export or publish results", "tutorial": "#19, #28"},
                    ]
                })

            result = {
                "goal": goal,
                "suggested_workflows": workflow_plans,
                "next_steps": [
                    "Use generate_code tool for specific tasks",
                    "Use search_whitebox_tools for analysis functions",
                    "Use suggest_colormap for visualization",
                ],
                "tutorials": "https://leafmap.org/notebooks/",
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "create_notebook":
            goal = arguments["goal"]
            output_path = arguments["output_path"]
            parameters = arguments.get("parameters", {})

            # Generate workflow plan first
            workflow_result = await call_tool("plan_workflow", {"goal": goal})
            workflow_data = json.loads(workflow_result[0].text)

            # Create notebook structure
            notebook = {
                "cells": [],
                "metadata": {
                    "kernelspec": {
                        "display_name": "Python 3",
                        "language": "python",
                        "name": "python3"
                    },
                    "language_info": {
                        "name": "python",
                        "version": "3.11.0"
                    }
                },
                "nbformat": 4,
                "nbformat_minor": 5
            }

            # Add title cell
            notebook["cells"].append({
                "cell_type": "markdown",
                "metadata": {},
                "source": [f"# {goal.title()}\n\n**Generated by Leafmap MCP Server**\n\nThis notebook was automatically generated to accomplish: {goal}"]
            })

            # Add imports cell
            imports = """import leafmap
import geopandas as gpd
import os
import warnings
warnings.filterwarnings('ignore')

print("✓ Imports successful")"""

            notebook["cells"].append({
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [imports]
            })

            # Add workflow steps
            if workflow_data.get("suggested_workflows"):
                for workflow in workflow_data["suggested_workflows"]:
                    # Add workflow title
                    notebook["cells"].append({
                        "cell_type": "markdown",
                        "metadata": {},
                        "source": [f"## {workflow['workflow']}\n"]
                    })

                    # Add each step
                    for step in workflow.get("steps", []):
                        # Step description
                        step_desc = f"### Step {step['step']}: {step['action']}\n"
                        if "tutorial" in step:
                            step_desc += f"\n*Reference: Tutorial {step['tutorial']}*"

                        notebook["cells"].append({
                            "cell_type": "markdown",
                            "metadata": {},
                            "source": [step_desc]
                        })

                        # Step code
                        if "code" in step:
                            notebook["cells"].append({
                                "cell_type": "code",
                                "execution_count": None,
                                "metadata": {},
                                "outputs": [],
                                "source": [step["code"]]
                            })

            # Add final display cell
            notebook["cells"].append({
                "cell_type": "markdown",
                "metadata": {},
                "source": ["## Results\n\nThe interactive map should be displayed above. You can:\n- Zoom and pan\n- Toggle layers\n- Inspect data"]
            })

            # Save notebook
            import os
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

            with open(output_path, 'w') as f:
                json.dump(notebook, f, indent=2)

            result = {
                "status": "success",
                "notebook_path": output_path,
                "cell_count": len(notebook["cells"]),
                "message": f"Jupyter notebook created successfully at {output_path}",
                "next_steps": [
                    f"Open the notebook: jupyter notebook {output_path}",
                    "Or use execute_workflow tool to run it automatically"
                ]
            }

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        elif name == "execute_workflow":
            import os
            import time

            goal = arguments["goal"]
            working_dir = arguments.get("working_directory", ".")
            parameters = arguments.get("parameters", {})
            timeout = arguments.get("timeout", 300)
            open_notebook = arguments.get("open_notebook", True)
            output_format = arguments.get("output_format", "html")

            # Create unique notebook name
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            notebook_name = f"workflow_{timestamp}.ipynb"
            notebook_path = os.path.join(working_dir, notebook_name)

            # Create the notebook
            create_result = await call_tool("create_notebook", {
                "goal": goal,
                "output_path": notebook_path,
                "parameters": parameters
            })

            # Check if notebook was created
            if not os.path.exists(notebook_path):
                return [TextContent(type="text", text=json.dumps({
                    "status": "error",
                    "message": f"Failed to create notebook at {notebook_path}"
                }, indent=2))]

            # Try to execute the notebook
            try:
                # Check if nbconvert/papermill is available
                try:
                    import nbformat
                    from nbconvert.preprocessors import ExecutePreprocessor
                    executor_available = True
                except ImportError:
                    executor_available = False

                if not executor_available:
                    result = {
                        "status": "notebook_created",
                        "notebook_path": notebook_path,
                        "execution_status": "skipped",
                        "message": "Notebook created but not executed (nbconvert not installed)",
                        "install_instructions": "To enable execution: pip install nbconvert jupyter",
                        "manual_run": f"jupyter nbconvert --to notebook --execute {notebook_path}"
                    }
                    return [TextContent(type="text", text=json.dumps(result, indent=2))]

                # Execute the notebook
                with open(notebook_path, 'r') as f:
                    nb = nbformat.read(f, as_version=4)

                ep = ExecutePreprocessor(timeout=timeout, kernel_name='python3')

                # Change to working directory for execution
                original_dir = os.getcwd()
                os.chdir(working_dir)

                try:
                    ep.preprocess(nb, {'metadata': {'path': working_dir}})
                    execution_success = True
                    execution_error = None
                except Exception as e:
                    execution_success = False
                    execution_error = str(e)
                finally:
                    os.chdir(original_dir)

                # Save executed notebook
                executed_path = notebook_path.replace('.ipynb', '_executed.ipynb')
                with open(executed_path, 'w') as f:
                    nbformat.write(nb, f)

                # Extract outputs
                outputs_summary = []
                for i, cell in enumerate(nb.cells):
                    if cell.cell_type == 'code' and cell.get('outputs'):
                        for output in cell.outputs:
                            if output.output_type == 'stream':
                                outputs_summary.append({
                                    "cell": i,
                                    "type": "text",
                                    "content": output.text[:200]  # Truncate long outputs
                                })
                            elif output.output_type == 'error':
                                outputs_summary.append({
                                    "cell": i,
                                    "type": "error",
                                    "error": output.ename,
                                    "message": output.evalue
                                })

                result = {
                    "status": "success" if execution_success else "partial_success",
                    "notebook_path": notebook_path,
                    "executed_notebook_path": executed_path,
                    "execution_status": "completed" if execution_success else "completed_with_errors",
                    "execution_time": f"max {timeout}s",
                    "outputs_count": len(outputs_summary),
                    "outputs_summary": outputs_summary[:10],  # First 10 outputs
                    "message": "Workflow executed successfully!" if execution_success else f"Workflow executed with errors: {execution_error}",
                    "next_steps": [
                        f"View the executed notebook: jupyter notebook {executed_path}",
                        "Check the outputs above for results",
                        "Generated files should be in the working directory"
                    ]
                }

                if not execution_success:
                    result["error_details"] = execution_error

                # Handle automatic notebook opening
                if open_notebook and output_format != "none":
                    import webbrowser
                    import subprocess
                    import sys

                    opened = False
                    opening_method = None

                    try:
                        if output_format == "html":
                            # Convert notebook to HTML
                            from nbconvert import HTMLExporter
                            html_exporter = HTMLExporter()
                            (body, resources) = html_exporter.from_notebook_node(nb)

                            # Save HTML file
                            html_path = executed_path.replace('.ipynb', '.html')
                            with open(html_path, 'w', encoding='utf-8') as f:
                                f.write(body)

                            # Open in browser
                            webbrowser.open('file://' + os.path.abspath(html_path))
                            opened = True
                            opening_method = "browser"
                            result["html_path"] = html_path
                            result["opened"] = True
                            result["opening_method"] = "Opened HTML in default browser"

                        elif output_format == "jupyter":
                            # Try to open in Jupyter
                            try:
                                # Check if jupyter is available
                                subprocess.run(
                                    ["jupyter", "notebook", os.path.abspath(executed_path)],
                                    check=False,
                                    stdout=subprocess.DEVNULL,
                                    stderr=subprocess.DEVNULL,
                                    start_new_session=True
                                )
                                opened = True
                                opening_method = "jupyter"
                                result["opened"] = True
                                result["opening_method"] = "Launched Jupyter notebook server"
                            except (FileNotFoundError, subprocess.CalledProcessError):
                                result["opened"] = False
                                result["opening_method"] = "Failed to launch Jupyter (not installed or not in PATH)"

                    except Exception as e:
                        result["opened"] = False
                        result["opening_error"] = str(e)
                        result["opening_method"] = f"Failed to open notebook: {str(e)}"

                return [TextContent(type="text", text=json.dumps(result, indent=2))]

            except Exception as e:
                result = {
                    "status": "error",
                    "notebook_path": notebook_path,
                    "execution_status": "failed",
                    "error": str(e),
                    "message": f"Failed to execute notebook: {str(e)}",
                    "fallback": f"You can still run the notebook manually: jupyter notebook {notebook_path}"
                }
                return [TextContent(type="text", text=json.dumps(result, indent=2))]

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
