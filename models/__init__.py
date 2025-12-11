"""
__init__.py file for models package
Makes the models directory a Python package
"""

from .classifier import PlasticClassifier, create_classifier_with_keras_model

__all__ = ['PlasticClassifier', 'create_classifier_with_keras_model']
