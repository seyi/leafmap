# Leafmap MCP Server - Testing Guide

This guide explains how to test the Leafmap MCP server on your local machine.

## Prerequisites

```bash
# Install the MCP server
cd /home/user/leafmap/mcp-server
pip install -e .

# Install optional dependencies for full functionality
pip install nbformat nbconvert jupyter
```

## Testing Options

### Option 1: Quick Standalone Testing (Recommended for Development)

Run the provided test scripts to verify functionality:

```bash
# Test basic tools
python test_local.py

# Test notebook generation and execution
python test_notebook_workflow.py

# Run full test suite
pytest test_server.py -v
```

### Option 2: Test with Claude Desktop (Full MCP Experience)

1. **Install Claude Desktop** from https://claude.ai/download

2. **Configure the MCP Server**:

   **On macOS:**
   ```bash
   # Edit Claude Desktop config
   code ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

   **On Linux:**
   ```bash
   # Edit Claude Desktop config
   code ~/.config/Claude/claude_desktop_config.json
   ```

   **On Windows:**
   ```
   Edit: %APPDATA%\Claude\claude_desktop_config.json
   ```

3. **Add this configuration**:
   ```json
   {
     "mcpServers": {
       "leafmap": {
         "command": "python",
         "args": ["-m", "mcp_server_leafmap"],
         "cwd": "/home/user/leafmap/mcp-server"
       }
     }
   }
   ```

4. **Restart Claude Desktop**

5. **Test the integration**:
   - Open Claude Desktop
   - Look for the 🔌 icon indicating MCP servers are connected
   - Try asking: "List available leafmap basemaps"
   - Try asking: "Create a notebook that displays a map of New York City"
   - Try asking: "Execute a workflow to create a watershed analysis"

### Option 3: Test via MCP Inspector (Debugging)

The MCP Inspector is a debugging tool for MCP servers:

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Run the inspector
mcp-inspector python -m mcp_server_leafmap
```

This opens a web interface where you can:
- View all available tools and resources
- Call tools interactively
- Inspect responses
- Debug server behavior

## Available Tools to Test

### Basic Tools (7)
1. **list_basemaps** - List 153+ available basemaps
2. **convert_coordinates** - Convert between coordinate systems
3. **get_crs_info** - Get CRS information
4. **view_raster** - Generate code to view raster data
5. **view_vector** - Generate code to view vector data
6. **get_raster_info** - Get raster metadata
7. **get_vector_info** - Get vector metadata

### Code Generation Tool (1)
8. **generate_code** - Generate leafmap code snippets

### Workflow Tools (5)
9. **csv_to_map_helper** - Convert CSV with coordinates to maps
10. **search_whitebox_tools** - Search 468+ geoprocessing tools
11. **suggest_colormap** - Recommend colormaps for data types
12. **list_data_sources** - Browse 30+ public data sources
13. **plan_workflow** - Plan multi-step workflows

### Notebook Automation Tools (2)
14. **create_notebook** - Generate Jupyter notebooks
15. **execute_workflow** - Create, execute, and open notebooks automatically

## Example Test Scenarios

### Test 1: Basic Coordinate Conversion
```python
import asyncio
from server import call_tool

async def test():
    result = await call_tool("convert_coordinates", {
        "x": -122.4194,
        "y": 37.7749,
        "from_crs": "EPSG:4326",
        "to_crs": "EPSG:3857"
    })
    print(result[0].text)

asyncio.run(test())
```

### Test 2: Search Geospatial Tools
```python
import asyncio
from server import call_tool

async def test():
    result = await call_tool("search_whitebox_tools", {
        "query": "watershed"
    })
    print(result[0].text)

asyncio.run(test())
```

### Test 3: Create and Execute Notebook
```python
import asyncio
from server import call_tool

async def test():
    # This will create, execute, and open a notebook in your browser
    result = await call_tool("execute_workflow", {
        "goal": "Create a map showing earthquake locations in California",
        "working_directory": "/tmp",
        "open_notebook": True,  # Opens in browser automatically
        "output_format": "html"  # Options: 'html', 'jupyter', 'none'
    })
    print(result[0].text)

asyncio.run(test())
```

### Test 4: Generate Code Snippet
```python
import asyncio
from server import call_tool

async def test():
    result = await call_tool("generate_code", {
        "task": "Load a shapefile and display it with custom styling",
        "backend": "ipyleaflet"
    })
    print(result[0].text)

asyncio.run(test())
```

## Testing the Automatic Notebook Opening Feature

The `execute_workflow` tool now supports automatic opening:

```python
# Test HTML opening (default)
result = await call_tool("execute_workflow", {
    "goal": "Create a simple map",
    "open_notebook": True,      # Auto-open (default)
    "output_format": "html"     # Opens HTML in browser (default)
})

# Test Jupyter server opening
result = await call_tool("execute_workflow", {
    "goal": "Create a simple map",
    "open_notebook": True,
    "output_format": "jupyter"  # Launches Jupyter server
})

# Test without opening
result = await call_tool("execute_workflow", {
    "goal": "Create a simple map",
    "open_notebook": False,
    "output_format": "none"
})
```

## Available Resources to Test

Test reading documentation resources:

```python
from server import read_resource

# Read overview
content = await read_resource("leafmap://docs/overview")

# Read installation guide
content = await read_resource("leafmap://docs/installation")

# Read backend guide
content = await read_resource("leafmap://docs/backends")

# Read examples
content = await read_resource("leafmap://examples/ipyleaflet")
```

## Troubleshooting

### Issue: "Module not found: mcp_server_leafmap"
**Solution:** Make sure you installed the package:
```bash
cd /home/user/leafmap/mcp-server
pip install -e .
```

### Issue: "Notebook execution skipped (nbconvert not installed)"
**Solution:** Install execution dependencies:
```bash
pip install nbformat nbconvert jupyter
```

### Issue: "Browser doesn't open automatically"
**Solution:** Check that:
- `open_notebook=True` is set
- `output_format="html"` or `"jupyter"`
- Python `webbrowser` module works: `python -m webbrowser https://google.com`

### Issue: Claude Desktop doesn't see the server
**Solution:**
1. Check the config file path is correct
2. Verify JSON syntax is valid
3. Restart Claude Desktop
4. Check logs: `~/Library/Logs/Claude/` (macOS)

## Performance Testing

Run the full test suite with coverage:

```bash
cd /home/user/leafmap/mcp-server
pytest test_server.py -v --cov=server --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## Next Steps

After testing locally:

1. **Use with Claude Desktop** - Ask Claude to help with geospatial tasks
2. **Create custom workflows** - Build notebooks for your specific needs
3. **Extend the server** - Add new tools or resources
4. **Share with others** - Publish your MCP server configuration

## Support

- Report issues: https://github.com/anthropics/claude-code/issues
- MCP documentation: https://modelcontextprotocol.io
- Leafmap docs: https://leafmap.org

---

**Happy Testing! 🗺️**
