from loguru import logger

import os, requests

def notify_node_unlocked(user_id: int, node_id: int, node_title: str) -> None:
    base_url = os.environ.get("NOTIFICATIONS_BASE_URL", "http://notifications:8002")

    try:
        requests.post(
            f"{base_url}/api/v1/notifications/node-unlocked",
            json={"user_id": user_id, "node_id": node_id, "node_title": node_title},
            timeout=2,
        )
    except Exception as e:
        logger.warning(f"notify_node_unlocked failed: {e}")

    return None