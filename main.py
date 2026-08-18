from mcp.server.fastmcp import FastMCP
from services import img_service
from services.file_service import search_files_by_extension
mcp = FastMCP("files-mcp-server")
gh=img_service()

@mcp.tool(description="""
Return search results for images based on a user-provided description.

Use when:

You need to find images related to a specific description or keywords.

You want to search through a directory of images for relevant matches based on descriptive input.

Before processing a batch of images to determine which ones match a certain theme, keyword, or context.

Inputs:

description: A text string containing the description or keywords to search for in the images (e.g., "cat playing with a ball").

folder_path: Path to the directory containing the images to be searched.

timeout_sec: Maximum duration (in seconds) for the image search operation to run.

Returns (ToolResult):

ok=true: data.matched_images contains a list of image paths that match the description or keywords provided.

ok=false: error.code/message and additional details regarding any failures (e.g., invalid path, timeout, or no matching images found).
""")
async def search_images_by_description(description: str, folder_path: str, timeout_sec: int):
    try:
        # Validate folder path
        if not os.path.isdir(folder_path):
            return {"ok": False, "error": {"code": "InvalidPath", "message": f"The folder path '{folder_path}' is not valid."}}

        # Search for images matching the description
        matched_images = gh.find_images_by_description(description, folder_path)

        if not matched_images:
            return {"ok": False, "error": {"code": "NoMatches", "message": "No images found matching the provided description."}}

        return {"ok": True, "data": {"matched_images": matched_images}}

    except Exception as e:
        return {"ok": False, "error": {"code": "SearchError", "message": str(e)}}