from flask import Flask, jsonify
from marshmallow import ValidationError

from services.ugc.ugc_config import Config, TestConfig
from services.ugc.models import db
from services.ugc.common.exceptions import UGCException
from services.ugc.blueprints import reviews_bp, comments_bp, moderation_bp


def register_error_handlers(app):
    @app.errorhandler(UGCException)
    def handle_ugc_exception(exc):
        return jsonify({
            'error': {
                'code': exc.code,
                'detail': exc.message,
            },
        }), exc.status_code

    @app.errorhandler(ValidationError)
    def handle_validation_error(exc):
        return jsonify({
            'error': {
                'code': 'validation_error',
                'detail': 'Ошибка валидации',
                'fields': exc.messages,
            },
        }), 422

    @app.errorhandler(Exception)
    def handle_unexpected_error(exc):
        if app.config.get('TESTING'):
            raise exc
        return jsonify({
            'error': {
                'code': 'internal_error',
                'detail': 'Внутренняя ошибка сервера',
            },
        }), 500


def register_blueprints(app):
    app.register_blueprint(reviews_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(moderation_bp)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    register_blueprints(app)
    register_error_handlers(app)

    @app.route('/health')
    def health():
        return jsonify({'status': 'ok'}), 200

    return app


def create_test_app():
    return create_app(TestConfig)
