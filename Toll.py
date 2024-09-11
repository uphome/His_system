from flask import Blueprint, render_template, redirect, url_for

# 创建一个蓝图对象
toll_bp = Blueprint('toll_bp', __name__)


@toll_bp.route('/Toll')
def Toll():
    return 'Toll'


@toll_bp.route('/Doctor')
def Doctor():
    return 'Doctor!'


@toll_bp.route('/Inspection')
def Inspection():
    return 'Inspection!'


@toll_bp.route('/Pharmacy')
def Pharmacy():
    return 'Pharmacy!'


@toll_bp.route('/superuser')
def superuser():
    return 'System superuser!'