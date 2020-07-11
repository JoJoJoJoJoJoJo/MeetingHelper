from flask import Flask, request, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

import click


app = Flask(__name__)
bp = Bootstrap()
db = SQLAlchemy()


def create_app():
    from config import Config  # 创建app时加载，避免环境变量未设置
    app.config.from_object(Config)
    bp.init_app(app)
    db.init_app(app)
    from . import views

    #  cli
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Drop all then create.')
    def init(drop=False):
        if drop:
            db.drop_all()
        db.create_all()
        click.echo('DB Initialized.')
    return app
