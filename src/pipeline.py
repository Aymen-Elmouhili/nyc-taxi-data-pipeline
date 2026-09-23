import logging

from src.config.logging_config import setup_logging
from src.load.load_data import load_raw_data
from src.transform.transform_data import transform_data


setup_logging()

logger = logging.getLogger(__name__)


def run_pipeline():
    logger.info("=== START PIPELINE ===")

    try:
        logger.info("[1/2] Starting raw data loading...")
        load_raw_data()
        logger.info("[1/2] Raw data loading completed successfully.")

    except Exception:
        logger.exception("[1/2] Raw data loading failed.")
        raise

    try:
        logger.info("[2/2] Starting data transformation...")
        transform_data()
        logger.info("[2/2] Data transformation completed successfully.")

    except Exception:
        logger.exception("[2/2] Data transformation failed.")
        raise

    logger.info("=== PIPELINE COMPLETED SUCCESSFULLY ===")


if __name__ == "__main__":
    run_pipeline()