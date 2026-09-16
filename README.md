# Pixabay MCP Server

A Model Context Protocol (MCP) server that provides access to the Pixabay API for searching and retrieving royalty-free images and videos.

## Features

- **Image Search**: Search through millions of royalty-free images
- **Video Search**: Find high-quality stock videos
- **Advanced Filtering**: Filter by category, orientation, color, size, and more
- **Individual Lookup**: Get specific images or videos by ID
- **Multiple Formats**: Access different image sizes and video qualities

## Getting a Pixabay API Key

1. Sign up at [Pixabay](https://pixabay.com/accounts/register/)
2. Go to the [Pixabay API page](https://pixabay.com/api/docs/)
3. Copy your API key

## Installation

### Option 1: Quick install with the Claude Code CLI (recommended)

Register the published server directly with `claude mcp add`:

```bash
claude mcp add pixabay \
  --env PIXABAY_API_KEY=YOUR_API_KEY \
  -- npx -y @hanoak/pixabay-mcp-server
```

This adds the server to Claude Code's MCP configuration and runs it on demand via `npx`, so there's nothing to clone or build locally.

### Option 2: Build from source (this repo)

1. Clone this repository:
   ```bash
   git clone <this-repo-url>
   cd 1
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Build the project:
   ```bash
   npm run build
   ```
4. Set your API key as an environment variable:
   ```bash
   export PIXABAY_API_KEY="your-api-key-here"
   ```
5. Register it with Claude Code, pointing at the built entrypoint:
   ```bash
   claude mcp add pixabay --env PIXABAY_API_KEY="$PIXABAY_API_KEY" -- node "$(pwd)/dist/index.js"
   ```

### Claude Desktop Configuration

Add the server to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "pixabay": {
      "command": "npx",
      "args": ["-y", "@hanoak/pixabay-mcp-server"],
      "env": {
        "PIXABAY_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

Or, to run the version built from this repo, use `"command": "node"` and `"args": ["/path/to/dist/index.js"]` instead.

## Available Tools

### search_images
Search for royalty-free images with various filters:

- `q`: Search term (max 100 characters)
- `lang`: Language code (default: "en")
- `image_type`: "all", "photo", "illustration", "vector"
- `orientation`: "all", "horizontal", "vertical"
- `category`: Category filter (nature, business, etc.)
- `min_width`/`min_height`: Minimum dimensions
- `colors`: Color filter (red, blue, grayscale, etc.)
- `editors_choice`: Editor's Choice awards only
- `safesearch`: Safe for all ages
- `order`: "popular" or "latest"
- `page`: Page number (default: 1)
- `per_page`: Results per page (3-200, default: 20)

### search_videos
Search for royalty-free videos with similar filtering options:

- `q`: Search term
- `video_type`: "all", "film", "animation"
- All other parameters similar to image search

### get_image_by_id
Retrieve a specific image by its Pixabay ID:
- `id`: Pixabay image ID (required)

### get_video_by_id
Retrieve a specific video by its Pixabay ID:
- `id`: Pixabay video ID (required)

## Usage Examples

### Basic Image Search
```
Search for "mountain landscape" photos
```

### Advanced Image Search
```
Search for horizontal nature photos with minimum width 1920px, editors choice only
```

### Video Search
```
Find animation videos about "space exploration"
```

## API Rate Limits

- 100 requests per 60 seconds by default
- Responses must be cached for 24 hours
- Systematic mass downloads are not allowed

## Response Format

The server returns JSON responses with image/video metadata including:
- URLs for different sizes
- Dimensions and file sizes
- View/download/like counts
- User information
- Tags and categories

## Development

### Running in Development Mode
```bash
npm run dev
```

### Building
```bash
npm run build
```

## License

MIT License - see LICENSE file for details

## Disclaimer

This server provides access to Pixabay's API. Please comply with:
- Pixabay's Terms of Service
- Content License requirements
- Attribution requirements when displaying search results
- Rate limiting and caching requirements

Images and videos are subject to Pixabay's Content License. Always check individual image/video licenses before use.
