#!/bin/bash

# Script to download an image from Pexels using curl
# Usage: ./download_pexels_image.sh <download_url> <filename>

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <download_url> <filename>"
    exit 1
fi

DOWNLOAD_URL=$1
FILENAME=$2
OUTPUT_DIR="../imagesandvids"

# Create the output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

echo "Downloading image from $DOWNLOAD_URL..."
curl -s "$DOWNLOAD_URL" -o "$OUTPUT_DIR/$FILENAME"

if [ $? -eq 0 ]; then
    echo "Image successfully downloaded to $OUTPUT_DIR/$FILENAME"
    echo "Don't forget to add proper attribution:"
    echo "- Always show a prominent link to Pexels (e.g., 'Photos provided by Pexels')"
    echo "- Always credit photographers (e.g., 'Photo by [Photographer] on Pexels')"
else
    echo "Error downloading image."
fi
