# Pexels MCP Server Tools Guide

This document provides an overview of the Pexels MCP Server's capabilities through the Model Context Protocol (MCP) in VS Code. Pexels MCP Server allows access to a vast library of professional stock photos and videos, with tools for searching, retrieving, and downloading high-quality visual content.

## Photo Tools

### 1. Search for Photos

**Question:** "Find me some photos of lions on the African savannah."  
**Tool:** `f1e_searchPhotos`  
**Description:** Searches the Pexels library for photos matching your query, with optional filters for orientation, size, and color. Returns metadata including photo IDs, URLs, and attribution information.

```
Natural language: "Find high-quality photos of mountains at sunset"
Tool call: f1e_searchPhotos({"query": "mountains at sunset", "orientation": "landscape", "perPage": 5})
```

### 2. Download a Photo

**Question:** "I'd like to download this lion photo in large size."  
**Tool:** `f1e_downloadPhoto`  
**Description:** Provides a direct download link for a specific photo by ID, with options to choose size. Returns the download URL, suggested filename, and required attribution information.

```
Natural language: "Download this photo with ID 32151901 in large size"
Tool call: f1e_downloadPhoto({"id": 32151901, "size": "large"})
```

### 3. Get Curated Photos

**Question:** "Show me the current curated collection of photos from Pexels."  
**Tool:** `f1e_getCuratedPhotos`  
**Description:** Retrieves Pexels' current curated collection of high-quality photos selected by their team. Results can be paginated for browsing through multiple sets.

```
Natural language: "Show me the latest curated photos from Pexels"
Tool call: f1e_getCuratedPhotos({"perPage": 10})
```

### 4. Get Photo Details

**Question:** "Can you show me all the available information about this specific photo?"  
**Tool:** `f1e_getPhoto`  
**Description:** Retrieves comprehensive metadata about a specific photo, including all available sizes, photographer information, and full attribution details.

```
Natural language: "Get all the details for photo with ID 32151901"
Tool call: f1e_getPhoto({"id": 32151901})
```

## Video Tools

### 1. Search for Videos

**Question:** "Find me some videos of waves crashing on a beach."  
**Tool:** `f1e_searchVideos`  
**Description:** Searches the Pexels library for videos matching your query, with optional filters. Returns metadata including video IDs, URLs, preview images, and attribution information.

```
Natural language: "Find videos of city traffic time lapse"
Tool call: f1e_searchVideos({"query": "city traffic time lapse", "orientation": "landscape", "perPage": 5})
```

### 2. Get Popular Videos

**Question:** "What are the current popular videos on Pexels?"  
**Tool:** `f1e_getPopularVideos`  
**Description:** Retrieves a collection of currently popular videos from Pexels, with optional filters for duration and dimensions. Results can be paginated.

```
Natural language: "Show me popular short videos under 30 seconds"
Tool call: f1e_getPopularVideos({"maxDuration": 30, "perPage": 5})
```

### 3. Get Video Details

**Question:** "Can you show me all the available information about this specific video?"  
**Tool:** `f1e_getVideo`  
**Description:** Retrieves comprehensive metadata about a specific video, including all available quality options, file sizes, duration, and attribution details.

```
Natural language: "Get all details for video with ID 1409899"
Tool call: f1e_getVideo({"id": 1409899})
```

### 4. Download a Video

**Question:** "I'd like to download this ocean wave video in HD quality."  
**Tool:** `f1e_downloadVideo`  
**Description:** Provides a direct download link for a specific video by ID, with options to choose quality (HD or SD). Returns the download URL, suggested filename, and required attribution information.

```
Natural language: "Download video 1409899 in HD quality"
Tool call: f1e_downloadVideo({"id": 1409899, "quality": "hd"})
```

## Collection Tools

### 1. Get Featured Collections

**Question:** "What are the current featured collections on Pexels?"  
**Tool:** `f1e_getFeaturedCollections`  
**Description:** Retrieves Pexels' current featured collections, which are curated sets of photos and videos organized by themes. Results can be paginated.

```
Natural language: "Show me the featured collections on Pexels"
Tool call: f1e_getFeaturedCollections({"perPage": 10})
```

### 2. Get Collection Media

**Question:** "Show me all the photos in the 'Wild Animals' collection."  
**Tool:** `f1e_getCollectionMedia`  
**Description:** Retrieves all media items (photos and/or videos) from a specific collection. Options to filter by media type, sort order, and paginate results.

```
Natural language: "Get all photos from collection with ID 'ftw9l9'"
Tool call: f1e_getCollectionMedia({"id": "ftw9l9", "type": "photos", "perPage": 15})
```

### 3. Set API Key

**Question:** "I need to update my Pexels API key."  
**Tool:** `f1e_setApiKey`  
**Description:** Dynamically updates the Pexels API key used for subsequent requests. Useful if you need to switch between different API keys during a session.

```
Natural language: "Set my Pexels API key to this new value"
Tool call: f1e_setApiKey({"apiKey": "your-api-key-here"})
```

## Usage Examples

### Workflow Example: Finding and Downloading Wildlife Images

1. **Search for specific wildlife photos:**

```
f1e_searchPhotos({"query": "lions hunting savannah", "orientation": "landscape", "perPage": 10})
```

2. **Get details about a specific photo:**

```
f1e_getPhoto({"id": 12345678})
```

3. **Download the selected photo in high resolution:**

```
f1e_downloadPhoto({"id": 12345678, "size": "original"})
```

4. **Browse a related wildlife collection:**

```
f1e_getCollectionMedia({"id": "wildlife-collection-id", "type": "photos", "perPage": 20})
```

## Optimized Workflows for AI Agents

### Single-Command Photo Download with Attribution

For maximum efficiency, AI agents can combine Pexels tool calls with a single terminal command to handle the entire search-download-attribution process:

#### Complete Photo Workflow (3 Steps)

1. **Search and identify photos:**

```
# First find suitable photos
result = f1e_searchPhotos({"query": "specific subject keywords", "perPage": 5})
# Select photo ID from the results
photo_id = result.photos[0].id  # Choose the first or most relevant photo
```

2. **Get download link and attribution info:**

```
# Get download link and attribution
download_info = f1e_downloadPhoto({"id": photo_id, "size": "medium"})
```

3. **Download image and create attribution in one terminal command:**

```
# Execute a single terminal command to download and create attribution
cmd = f"""
cd /path/to/project/imagesandvids && \\
curl -s "{download_info.download_link}" -o "filename.jpeg" && \\
cat > "filename_attribution.md" << 'EOL'
# Photo Attribution

## {photo_title}
- **Filename**: filename.jpeg
- **Photo ID**: {photo_id}
- **Photographer**: {download_info.attribution}
- **Source**: Pexels
- **Description**: {photo_description}

## Pexels License Information
Pexels provides free stock photos and videos that you can use for any project.
- All photos and videos on Pexels are free to use.
- Attribution is not required, but appreciated.
- You can modify the photos and videos from Pexels.
- You can use them for free for commercial and noncommercial purposes.

For full license terms, please visit: https://www.pexels.com/license/
EOL"""

run_in_terminal({"command": cmd, "explanation": "Downloading photo and creating attribution file", "isBackground": false})
```

#### Multiple Photos with Single Attribution (4 Steps)

1. **Search for photos:**

```
results = f1e_searchPhotos({"query": "search terms", "perPage": 3})
```

2. **Get download links for each photo:**

```
download_links = []
attribution_info = []
for i, photo in enumerate(results.photos):
    dl_info = f1e_downloadPhoto({"id": photo.id, "size": "medium"})
    download_links.append(dl_info.download_link)
    attribution_info.append({
        "id": photo.id,
        "photographer": dl_info.attribution,
        "description": photo.alt
    })
```

3. **Construct filenames:**

```
filenames = [f"{i+1}_subject.jpeg" for i in range(len(download_links))]
```

4. **Download all photos and create a single attribution file:**

```
cmd = f"""
cd /path/to/project/imagesandvids && \\
"""

# Add download commands for each photo
for i, (link, filename) in enumerate(zip(download_links, filenames)):
    cmd += f'curl -s "{link}" -o "{filename}" && \\\n'

# Add attribution file creation
cmd += f"""
cat > "all_photos_attribution.md" << 'EOL'
# Photos Attribution

"""

# Add each photo's attribution info
for i, (filename, info) in enumerate(zip(filenames, attribution_info)):
    cmd += f"""
## Photo {i+1}: {filename}
- **Photo ID**: {info["id"]}
- **Photographer**: {info["photographer"]}
- **Description**: {info["description"]}

"""

# Add license information
cmd += """
## Pexels License Information
- All photos from Pexels are free to use commercially and non-commercially
- Attribution is appreciated but not required
- For full license details: https://www.pexels.com/license/
EOL"""

run_in_terminal({"command": cmd, "explanation": "Downloading multiple photos with combined attribution", "isBackground": false})
```

## File Structure Guidelines

To maintain a clean and organized workspace:

1. **Place all downloaded images directly in the main `imagesandvids` folder** - Do not create or use subfolders for organizing images.

2. **Use consistent naming patterns** - Name files clearly with descriptive terms like `combat_fighter_jet.jpeg`.

3. **Keep attribution files alongside images** - Name attribution files to match their images, e.g., `combat_fighter_jet_attribution.md`.

4. **Use a single attribution file for related sets** - When downloading multiple related images (like a series), create a combined attribution file (e.g., `dublin_photos_attribution.md`).

This flat organization structure makes it easier to find and reference images within the project.

## Attribution Requirements

When using content from Pexels, you must follow these attribution guidelines:

- Always include a visible credit to Pexels (e.g., "Photos provided by Pexels")
- Always credit photographers (e.g., "Photo by John Doe on Pexels")

The download tools provide the proper attribution information with each download link.

## Tips for Effective Use

1. **Use descriptive queries** - Instead of generic terms like "nature," use more specific phrases like "misty forest at dawn" for better results.

2. **Leverage filters** - Use orientation, size, and color filters to narrow down results to exactly what you need.

3. **Check attribution** - Always save the attribution information provided with each download to properly credit Pexels and photographers.

4. **Browse collections** - Featured collections offer curated sets of related visuals that can be perfect for cohesive project needs.

5. **Consider resolution needs** - Only download the resolution you need; "large" is sufficient for most web uses, while "original" provides the highest quality for print or editing.

6. **Download to the main images folder** - Always download images directly to the main `/imagesandvids` folder rather than to subfolders to maintain a flat, organized structure.

7. **Optimize with single commands** - When downloading photos, combine the curl command with file creation in a single terminal command to minimize steps.

8. **Use heredocs for attribution** - Use shell heredocs (`<< 'EOL'`) to create attribution files in a single terminal command alongside downloads.

8. **Standardize filenames** - Use consistent naming patterns like `1_subject.jpeg` when downloading multiple related images.

9. **Combine attribution for sets** - When downloading multiple related images, create a single attribution file with sections for each image rather than separate files.

10. **Direct downloading** - Remember that downloading requires using the terminal with curl, not just the Pexels API tools. The Pexels tools provide the links, while curl does the actual downloading.

---

**Last Updated:** 2025-05-19
