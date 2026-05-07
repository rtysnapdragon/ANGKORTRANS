# accounts/rbac/db_manager.py
import os
from django.db import connections
from django.conf import settings


class DynamicDBManager:
    """
    Manages dynamic database connections without relying on settings.py.
    Can be initialized with environment variables or runtime parameters.
    """
    
    _instances = {}
    
    def __new__(cls, db_alias='rbac_db', **kwargs):
        if db_alias not in cls._instances:
            cls._instances[db_alias] = super().__new__(cls)
        return cls._instances[db_alias]
    
    def __init__(self, db_alias='rbac_db', **kwargs):
        if hasattr(self, '_initialized'):
            return
            
        self.db_alias = db_alias
        self.connection_params = self._build_connection_params(**kwargs)
        self._register_connection()
        self._initialized = True
    
    def _build_connection_params(self, **kwargs):
        """Build connection parameters from kwargs or environment variables."""
        engine = kwargs.get('engine', os.getenv('RBAC_DB_ENGINE', 'django.db.backends.postgresql'))
        
        params = {
            'ENGINE': engine,
            'NAME': kwargs.get('name', os.getenv('RBAC_DB_NAME', 'rbac_database')),
            'USER': kwargs.get('user', os.getenv('RBAC_DB_USER', 'rbac_user')),
            'PASSWORD': kwargs.get('password', os.getenv('RBAC_DB_PASSWORD', '')),
            'HOST': kwargs.get('host', os.getenv('RBAC_DB_HOST', 'localhost')),
            'PORT': kwargs.get('port', os.getenv('RBAC_DB_PORT', '5432')),
            'OPTIONS': kwargs.get('options', {}),
            'CONN_MAX_AGE': kwargs.get('conn_max_age', 600),
            'ATOMIC_REQUESTS': kwargs.get('atomic_requests', False),
        }
        
        # Support for SQLite
        if 'sqlite' in engine:
            params.pop('USER', None)
            params.pop('PASSWORD', None)
            params.pop('HOST', None)
            params.pop('PORT', None)
            
        return params
    
    def _register_connection(self):
        """Register the dynamic connection in Django's connection handler."""
        if self.db_alias not in connections.databases:
            connections.databases[self.db_alias] = self.connection_params
    
    def get_connection(self):
        """Get the database connection."""
        return connections[self.db_alias]
    
    def test_connection(self):
        """Test if the connection is working."""
        try:
            conn = self.get_connection()
            conn.cursor()
            return True
        except Exception as e:
            return False, str(e)
    
    @classmethod
    def get_or_create(cls, db_alias='rbac_db', **kwargs):
        """Get existing manager or create new one."""
        return cls(db_alias, **kwargs)