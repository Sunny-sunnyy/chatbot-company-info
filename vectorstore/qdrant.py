from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import logging 

from core.settings_loader import load_settings

settings = load_settings()
logger = logging.getLogger("vector_database")

QDRANT_CONFIG = settings["vector_database"]
COLLECTION_NAME = QDRANT_CONFIG["collection_name"]
VECTOR_SIZE = QDRANT_CONFIG["vector_size"]
DISTANCE = QDRANT_CONFIG.get("distance", "cosine")
TIMEOUT = QDRANT_CONFIG.get("timeout", 30)

_client: QdrantClient | None = None

def get_qdrant_client() -> QdrantClient:
    global _client
    if _client is not None:
        return _client
    
    try:
        # Neu ket noi qua URL
        if QDRANT_CONFIG.get("url"):
            logger.info("Connect via URL")
            _client = QdrantClient(
                url=QDRANT_CONFIG["url"],
                api_key=QDRANT_CONFIG.get("api_key"),
                timeout=TIMEOUT
            )
        else:
            logger.info(f"Connect via: {QDRANT_CONFIG.get('host')}: {QDRANT_CONFIG.get('port')}")
            
            _client = QdrantClient(
                host=QDRANT_CONFIG.get("host"),
                port=QDRANT_CONFIG.get("port"),
                api_key=QDRANT_CONFIG.get("api_key"),
                timeout=TIMEOUT
            )
        
        # Test connection
        _client.get_collections()
        logger.info("Successfully connected to Qdrant")
        return _client
    
    except Exception as exc:
        logger.error(f"Failed to connect to Qdrant: {exc}")
        raise ConnectionError(f"Cannot connect to Qdrant database: {exc}") from exc

def ensure_collection(client: QdrantClient):
    existing_collection = [collection.name for collection in client.get_collections().collections]
    
    if COLLECTION_NAME in existing_collection:
        logger.info(f"Collection '{COLLECTION_NAME}' already exists.")
        return
    
    logger.info(f"Creating collection '{COLLECTION_NAME}'...")
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance[DISTANCE.upper()]
        )
    )
    logger.info(f"Collection '{COLLECTION_NAME}' created successfully.")
    
