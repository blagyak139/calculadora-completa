import pytest
import subprocess
import time
import os
from fastapi.testclient import TestClient
from src.api import app


# ── Capa 2: cliente HTTP sin servidor real ──────────────────────────────────
@pytest.fixture(scope="session")
def cliente_api():
    with TestClient(app) as client:
        yield client


# ── Capa 3: servidor real para Playwright ──────────────────────────────────
@pytest.fixture(scope="session")
def servidor_api():
    proceso = subprocess.Popen(
        ["uvicorn", "src.api:app", "--port", "8000"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(2)
    yield proceso
    proceso.terminate()


@pytest.fixture(scope="function")
def pagina(playwright, servidor_api):
    html_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "src", "index.html")
    )
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto(f"file:///{html_path}")
    yield page
    browser.close()
