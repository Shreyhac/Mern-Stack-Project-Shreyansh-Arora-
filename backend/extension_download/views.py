import os
import zipfile
import tempfile
from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import subprocess
import shutil
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET"])
def download_extension(request):
    """
    Download the extension as a zip file for manual installation.
    """
    try:
        extension_path = Path(__file__).parent.parent.parent / "extension"
        
        if not extension_path.exists():
            logger.error(f"Extension path not found: {extension_path}")
            raise Http404("Extension not found")
        
        logger.info(f"Extension path found: {extension_path}")
        
        dist_path = extension_path / ".output" / "chrome-mv3"
        if dist_path.exists():
            logger.info("Using existing build")
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                zip_path = temp_path / "web-to-mcp-extension.zip"
                
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(dist_path):
                        for file in files:
                            file_path = Path(root) / file
                            arc_path = file_path.relative_to(dist_path)
                            zipf.write(file_path, arc_path)
                
                with open(zip_path, 'rb') as f:
                    response = HttpResponse(f.read(), content_type='application/zip')
                    response['Content-Disposition'] = 'attachment; filename="web-to-mcp-extension.zip"'
                    response['Content-Length'] = str(zip_path.stat().st_size)
                    return response
        else:
            logger.info("Building extension from source")
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                build_path = temp_path / "extension"
                
                shutil.copytree(extension_path, build_path)
                
                original_cwd = os.getcwd()
                try:
                    os.chdir(build_path)
                    
                    logger.info("Installing npm dependencies")
                    result = subprocess.run(["npm", "install"], 
                                          capture_output=True, text=True, timeout=300)
                    if result.returncode != 0:
                        logger.error(f"npm install failed: {result.stderr}")
                        raise Exception(f"npm install failed: {result.stderr}")
                    
                    logger.info("Building extension")
                    result = subprocess.run(["npm", "run", "build"], 
                                          capture_output=True, text=True, timeout=300)
                    if result.returncode != 0:
                        logger.error(f"npm run build failed: {result.stderr}")
                        raise Exception(f"npm run build failed: {result.stderr}")
                    
                    zip_path = temp_path / "web-to-mcp-extension.zip"
                    
                    output_path = build_path / ".output" / "chrome-mv3"
                    if output_path.exists():
                        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                            for root, dirs, files in os.walk(output_path):
                                for file in files:
                                    file_path = Path(root) / file
                                    arc_path = file_path.relative_to(output_path)
                                    zipf.write(file_path, arc_path)
                    else:
                        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                            for root, dirs, files in os.walk(build_path):
                                for file in files:
                                    if not file.startswith('.') and not file.endswith('.log'):
                                        file_path = Path(root) / file
                                        arc_path = file_path.relative_to(build_path)
                                        zipf.write(file_path, arc_path)
                    
                    with open(zip_path, 'rb') as f:
                        response = HttpResponse(f.read(), content_type='application/zip')
                        response['Content-Disposition'] = 'attachment; filename="web-to-mcp-extension.zip"'
                        response['Content-Length'] = str(zip_path.stat().st_size)
                        return response
                        
                finally:
                    os.chdir(original_cwd)
                    
    except Exception as e:
        logger.error(f"Extension download failed: {str(e)}")
        return JsonResponse({
            "error": "Extension download failed",
            "message": "Please try the Chrome Web Store option instead",
            "details": str(e)
        }, status=500)