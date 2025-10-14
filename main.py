import logging
import os
import sys
from pathlib import Path
import uvicorn

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)

def main():

    environment = os.getenv('ENVIRONMENT', 'development')
    from src.config import load_env_file
    load_env_file(f'.env.{environment}')

    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', '8000'))
    workers = int(os.getenv('WORKERS', '1'))
    reload = os.getenv('RELOAD', 'false').lower() in ('true', '1', 'yes')

    uvicorn.run(
        "src.presentation.app:app",
        host=host,
        port=port,
        workers=workers,
        reload=reload,
        log_config="./config/logging.yaml",
    )


if __name__ == "__main__":
    main()