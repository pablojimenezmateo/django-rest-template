import time
from celery import shared_task
from celery.utils.log import get_task_logger
from contextlib import contextmanager
from django.core.cache import cache

logger = get_task_logger(__name__)

LOCK_EXPIRE = 60 * 20  # Lock expires in 20 minutes


@contextmanager
def memcache_lock(lock_id):
    timeout_at = time.monotonic() + LOCK_EXPIRE - 3
    # cache.add fails if the key already exists
    acquired = cache.add(lock_id, "locked", LOCK_EXPIRE)
    try:
        yield acquired
    finally:
        # memcache delete is very slow, but we have to use it to take
        # advantage of using add() for atomic locking
        if time.monotonic() < timeout_at and acquired:
            # don't release the lock if we exceeded the timeout
            # to lessen the chance of releasing an expired lock
            # owned by someone else
            # also don't release the lock if we didn't acquire it
            cache.delete(lock_id)


@shared_task
def create_lock(lock_id):
    return cache.add(lock_id, "locked", LOCK_EXPIRE)


@shared_task
def remove_lock(lock_id):
    logger.info("Removing lock")
    cache.delete(lock_id)
    logger.info("Lock removed")
