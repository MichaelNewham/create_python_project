# Images and Videos Folder

This folder contains images and videos downloaded using the Pexels MCP server.

## Using the Pexels MCP Server

The Pexels MCP server is configured in your `.vscode/mcp.json` file and provides a set of tools for searching and downloading images and videos from Pexels.

### Available Tools

When using GitHub Copilot or Claude with MCP support, you can use these tools:

1. **Search Photos**: `f1e_searchPhotos`
   - Example: `f1e_searchPhotos` with parameters: 
     ```json
     {
       "query": "lions on savannah africa",
       "perPage": 5
     }
     ```

2. **Download Photo**: `f1e_downloadPhoto`
   - Example: `f1e_downloadPhoto` with parameters:
     ```json
     {
       "id": 32151901,
       "size": "large"
     }
     ```
   - Available sizes: 'original', 'large2x', 'large', 'medium', 'small', 'portrait', 'landscape', 'tiny'

3. **Get Photo Info**: `f1e_getPhoto`
   - Example: `f1e_getPhoto` with parameters:
     ```json
     {
       "id": 32151901
     }
     ```

4. **Search Videos**: `f1e_searchVideos`
   - Example: `f1e_searchVideos` with parameters:
     ```json
     {
       "query": "lions on savannah",
       "perPage": 5
     }
     ```

5. **Download Video**: `f1e_downloadVideo`
   - Example: `f1e_downloadVideo` with parameters:
     ```json
     {
       "id": 1234567,
       "quality": "hd"
     }
     ```

### Image Attribution

Always remember to properly attribute Pexels and the photographers:
- Always show a prominent link to Pexels (e.g., "Photos provided by Pexels")
- Always credit photographers (e.g., "Photo by [Photographer] on Pexels")

For more information, see the `attribution.md` file in this folder.
