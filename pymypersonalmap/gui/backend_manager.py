"""
Backend Manager

Manages FastAPI backend running in a separate daemon thread.
Allows the GUI to communicate with the backend via HTTP localhost.
"""

import threading
import time
import requests
import uvicorn
from typing import Optional
import logging


logger = logging.getLogger(__name__)


class BackendManager:
    """
    Manages FastAPI backend in background thread

    The backend runs as a daemon thread, which means it will
    automatically stop when the main application exits.

    Example:
        manager = BackendManager(host="127.0.0.1", port=8000)
        manager.start()
        # ... GUI runs ...
        manager.stop()  # Optional, daemon dies with app
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8000):
        """
        Initialize BackendManager

        Args:
            host: Host to bind backend (default: 127.0.0.1 for security)
            port: Port to bind backend (default: 8000)
        """
        self.host = host
        self.port = port
        self.server_thread: Optional[threading.Thread] = None
        self.is_running = False
        self._server: Optional[uvicorn.Server] = None

    def start(self):
        """
        Start FastAPI backend in daemon thread

        Raises:
            RuntimeError: If backend is already running
            TimeoutError: If backend doesn't start within timeout
        """
        if self.is_running:
            logger.warning("Backend is already running")
            return

        # Import app here to avoid circular imports
        from pymypersonalmap.main import app

        # Configure uvicorn server
        config = uvicorn.Config(
            app,
            host=self.host,
            port=self.port,
            log_level="error",  # Silenzioso per non disturbare GUI
            access_log=False,
        )
        self._server = uvicorn.Server(config)

        # Run server in daemon thread
        def run_server():
            """Thread target function"""
            try:
                self.is_running = True
                logger.info(f"Starting backend at {self.host}:{self.port}")
                self._server.run()
            except Exception as e:
                logger.error(f"Backend error: {e}")
                self.is_running = False

        self.server_thread = threading.Thread(target=run_server, daemon=True)
        self.server_thread.start()

        # Wait for backend to be ready
        self.wait_for_ready(timeout=10)
        logger.info("Backend started successfully")

    def wait_for_ready(self, timeout: int = 10):
        """
        Wait for backend to be ready by polling health endpoint

        Args:
            timeout: Maximum seconds to wait

        Raises:
            TimeoutError: If backend doesn't respond within timeout
        """
        start_time = time.time()
        health_url = f"http://{self.host}:{self.port}/health"

        while time.time() - start_time < timeout:
            try:
                response = requests.get(health_url, timeout=1)
                if response.status_code == 200:
                    logger.info("Backend health check passed")
                    return
            except requests.exceptions.RequestException:
                # Backend not ready yet, wait a bit
                time.sleep(0.2)

        raise TimeoutError(
            f"Backend failed to start within {timeout} seconds. "
            f"Check if port {self.port} is available."
        )

    def stop(self):
        """
        Stop backend server

        Note: Since server runs in daemon thread, this is optional.
        The thread will automatically stop when main app exits.
        """
        if not self.is_running:
            logger.warning("Backend is not running")
            return

        try:
            if self._server:
                self._server.should_exit = True
            self.is_running = False
            logger.info("Backend stopped")
        except Exception as e:
            logger.error(f"Error stopping backend: {e}")

    def is_healthy(self) -> bool:
        """
        Check if backend is healthy

        Returns:
            True if backend responds to health check, False otherwise
        """
        if not self.is_running:
            return False

        try:
            health_url = f"http://{self.host}:{self.port}/health"
            response = requests.get(health_url, timeout=2)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def get_base_url(self) -> str:
        """
        Get base URL for API requests

        Returns:
            Base URL string (e.g., "http://127.0.0.1:8000")
        """
        return f"http://{self.host}:{self.port}"
