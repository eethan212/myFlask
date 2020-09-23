from app.configs.development import DevelopmentConfig
from app.configs.pre_release import PreReleaseConfig
from app.configs.production import ProductionConfig
from app.configs.testing import TestingConfig


conf_map = {
    'default': DevelopmentConfig,
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'pre': PreReleaseConfig,
    'prod': ProductionConfig
}
