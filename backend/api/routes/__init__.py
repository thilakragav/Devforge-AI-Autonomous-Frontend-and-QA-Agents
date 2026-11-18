from .upload import router as upload_router
from .agent1 import router as agent1_router
from .agent2 import router as agent2_router
from .orchestrator import router as orchestrator_router
from .reports import router as reports_router
from .preview import router as preview_router

__all__ = [
    "upload_router",
    "agent1_router",
    "agent2_router",
    "orchestrator_router",
    "reports_router",
    "preview_router",
]
