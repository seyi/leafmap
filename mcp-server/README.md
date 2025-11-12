# Leafmap MCP Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that provides tools and resources for geospatial analysis and interactive mapping using [leafmap](https://leafmap.org).

## Overview

This MCP server exposes leafmap's powerful geospatial capabilities through the Model Context Protocol, allowing AI assistants and other MCP clients to:

- View and analyze raster data (GeoTIFFs, COGs, etc.)
- View and analyze vector data (Shapefiles, GeoJSON, GeoPackage, etc.)
- Access geospatial metadata and information
- Convert coordinates between different CRS
- List and access available basemaps
- Access leafmap documentation and resources

## Features

### Tools

The server provides the following tools:

1. **view_raster** - View raster files interactively in a web browser
   - Supports GeoTIFFs, Cloud Optimized GeoTIFFs (COGs), and other raster formats
   - Options for band selection, colormaps, and value ranges
   - Interactive viewer with opacity control and basemap selection

2. **view_vector** - View vector files interactively in a web browser
   - Supports Shapefiles, GeoJSON, GeoPackage, and other vector formats
   - Multiple map styles (dark-matter, positron, voyager, etc.)
   - Interactive features with zooming, panning, and inspection

3. **get_raster_info** - Get metadata about raster files
   - Returns bands, CRS, bounds, resolution, data type, and more
   - Useful for understanding raster properties before visualization

4. **get_vector_info** - Get information about vector files
   - Returns geometry type, CRS, feature count, bounds, and attributes
   - Helps understand vector data structure

5. **list_basemaps** - List all available basemaps in leafmap
   - Returns comprehensive list of basemap providers and tile URLs
   - Includes attribution information

6. **convert_coordinates** - Convert coordinates between CRS
   - Supports conversion between WGS84, Web Mercator, and many others
   - Useful for coordinate transformation tasks

7. **get_crs_info** - Get information about a coordinate reference system
   - Returns CRS name, type, units, area of use, and more
   - Helps understand CRS properties

### Resources

The server provides the following resources:

- **leafmap://docs/overview** - Overview of leafmap features and capabilities
- **leafmap://docs/installation** - Installation guide for leafmap
- **leafmap://docs/quickstart** - Quick start guide with examples
- **leafmap://info/repository** - Repository information (JSON)
- **leafmap://info/basemaps** - Available basemaps (JSON)

## Installation

### Prerequisites

- Python >= 3.10
- leafmap and its dependencies

### Install from source

1. Clone the leafmap repository:
```bash
git clone https://github.com/opengeos/leafmap.git
cd leafmap/mcp-server
```

2. Install the MCP server:
```bash
pip install -e .
```

Or install with all dependencies:
```bash
pip install -e ".[dev]"
```

### Install dependencies separately

If you prefer to install dependencies separately:

```bash
pip install mcp leafmap rasterio geopandas pyproj
```

## Usage

### Running the server standalone

You can run the MCP server directly:

```bash
python server.py
```

The server will start and listen for MCP protocol messages on stdin/stdout.

### Using with Claude Desktop

To use this server with Claude Desktop, add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "leafmap": {
      "command": "python",
      "args": ["/path/to/leafmap/mcp-server/server.py"]
    }
  }
}
```

On macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

### Using with other MCP clients

This server implements the standard MCP protocol and can be used with any MCP-compatible client. Refer to your client's documentation for configuration instructions.

## Example Usage

Once connected to an MCP client, you can use the tools like this:

### View a raster file
```
Can you view the raster file at /path/to/dem.tif using the terrain colormap?
```

### Get information about a vector file
```
What information can you tell me about the shapefile at /path/to/boundaries.shp?
```

### Convert coordinates
```
Convert the coordinates (37.7749, -122.4194) from EPSG:4326 to EPSG:3857
```

### List available basemaps
```
What basemaps are available in leafmap?
```

## Development

### Setting up development environment

Install the package with development dependencies:

```bash
pip install -e ".[dev]"
pip install -r requirements-test.txt
```

Or use the Makefile:

```bash
make install-dev
```

### Running tests

Run all tests:
```bash
pytest
```

Or use the Makefile:
```bash
make test
```

Run tests with verbose output:
```bash
pytest -vv
# or
make test-verbose
```

Run tests with coverage:
```bash
pytest --cov=server --cov-report=term-missing --cov-report=html
# or
make test-coverage
```

### Test structure

The test suite (`test_server.py`) includes:

- **TestResources**: Tests for all resource endpoints
  - Listing resources
  - Reading each resource
  - Error handling for invalid resources

- **TestTools**: Tests for all tool functionality
  - Tool listing and metadata
  - Individual tool tests with various parameters
  - Error handling

- **TestRasterInfo**: Integration tests with actual raster files
  - Creating sample GeoTIFF files
  - Reading metadata
  - Handling missing files

- **TestVectorInfo**: Integration tests with actual vector files
  - Creating sample GeoJSON files
  - Reading metadata
  - Handling missing files

- **TestErrorHandling**: Edge cases and error scenarios
  - Invalid CRS codes
  - Missing parameters
  - Malformed inputs

- **TestIntegration**: Server integration tests
  - Server initialization
  - Tool and resource validation

### Code formatting

Format code with black:
```bash
black server.py test_server.py
# or
make format
```

### Linting

Run linting checks:
```bash
flake8 server.py test_server.py --max-line-length=100
# or
make lint
```

### Type checking

Run type checking:
```bash
mypy server.py --ignore-missing-imports
# or (included in make lint)
make lint
```

### Clean up

Remove generated files:
```bash
make clean
```

## About Leafmap

Leafmap is a Python package for geospatial analysis and interactive mapping in a Jupyter environment. It provides:

- Interactive mapping with multiple backends (ipyleaflet, folium, kepler.gl, pydeck, bokeh)
- Support for vector and raster data visualization
- Integration with WhiteboxTools for advanced geospatial analysis (500+ tools)
- STAC catalog integration
- Time series animations
- Split-panel maps and linked maps
- And much more!

For more information:
- Documentation: https://leafmap.org
- GitHub: https://github.com/opengeos/leafmap
- PyPI: https://pypi.org/project/leafmap

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This MCP server is part of the leafmap project and is released under the MIT License. See the [LICENSE](../LICENSE) file for details.

## Support

- GitHub Issues: https://github.com/opengeos/leafmap/issues
- Discord: https://discord.gg/UgZecTUq5P
- YouTube Channel: https://youtube.com/@giswqs

## Citation

If you use leafmap in your research, please cite:

Wu, Q. (2021). Leafmap: A Python package for interactive mapping and geospatial analysis with minimal coding in a Jupyter environment. *Journal of Open Source Software*, 6(63), 3414. https://doi.org/10.21105/joss.03414
