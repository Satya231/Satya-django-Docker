#Then we need to import this app in your proj/proj/__init__.py module.
#  This ensures that the app is loaded when Django starts so that 
# the @shared_task decorator (mentioned later) will use it:


from .celery import app as celery_app


__all__ = ('celery_app',)