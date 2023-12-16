import os
import os.path as op

from flask import send_from_directory, redirect
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla.fields import QuerySelectField
from flask_admin.menu import MenuLink
from flask_wtf import FlaskForm
from wtforms import SelectField

from app import app
from app import db
from flask_admin.form import Select2Field, Select2Widget
from flask_admin import Admin, AdminIndexView, expose, BaseView
from db.aestetica.tables import (Filial, Salary, Staff, Role, Department, SalaryGrid,
    Service, Consumables, Bonus, Payouts, Traffic
)



class StaffView(ModelView):
    column_list = ['name', 'role', 'is_new', ]
    column_labels = {
        'name': 'Имя',
        'role': 'Должность',
        'is_new': 'Новый'
    }
    form_columns = ['name', 'role', 'is_new', ]
    form_overrides = {
        'role': SelectField
    }
    column_filters = ['name', 'role', 'is_new', ]
    column_editable_list = ['name', 'is_new', ]
    column_default_sort = 'name'
    column_searchable_list = ['name', ]
    can_export = True
    export_types = ['csv', 'json', 'xlsx']
    column_sortable_list = ['name', 'is_new', 'role']
    create_modal = True
    edit_modal = True
    page_size = 100
    form_args = {
        'role': {
            'label': 'Должность',
            'choices': lambda: [(role.name, role.name) for role in db.session.query(Role).all()],
            'widget': Select2Widget()
        }
    }


class RoleView(ModelView):
    column_list = ['name', ]
    column_labels = {
        'name': 'Наименование'
    }
    form_columns = ['name', ]
    can_edit = False
    column_searchable_list = ['name', ]
    can_export = True
    export_types = ['csv', 'json', 'xlsx']
    column_sortable_list = ['name', ]
    create_modal = True
    page_size = 100


class FilialView(ModelView):
    column_list = ['name', 'db_address', 'db_port', 'db_name', 'db_user', 'db_password', ]
    create_modal = True
    edit_modal = True
    can_export = True
    page_size = 100
    export_types = ['csv', 'json', 'xlsx']
    form_columns = ['name', 'db_address', 'db_port', 'db_name', 'db_user', 'db_password', ]
    column_editable_list = ['name', 'db_address', 'db_port', 'db_name', 'db_user', 'db_password', ]


class DepartmentView(ModelView):
    column_list = ['name', ]
    column_labels = {
        'name': 'Наименование'
    }
    form_columns = ['name', ]
    can_edit = False
    column_searchable_list = ['name', ]
    can_export = True
    export_types = ['csv', 'json', 'xlsx']
    column_sortable_list = ['name', ]
    create_modal = True
    page_size = 100


class SalaryView(ModelView):
    column_list = ['id', 'staff', 'department', 'fix', 'filial', ]
    column_labels = {
        'id': 'id',
        'staff': 'Сотрудник',
        'department': "Департамент",
        "fix": 'Оклад',
        'filial': 'Филиал'
    }
    form_columns = ['staff', 'department', 'fix', 'filial', ]
    form_overrides = {
        'staff': SelectField,
        'department': SelectField,
        'filial': SelectField
    }
    column_filters = ['filial', 'staff', 'department']
    column_default_sort = 'staff'
    can_export = True
    can_create = False
    can_delete = False
    export_types = ['csv', 'json', 'xlsx']
    column_sortable_list = ['id', 'staff', 'department', 'fix', 'filial', ]
    edit_modal = True
    page_size = 100
    form_args = {
        'staff': {
            'label': 'Сотрудник',
            'choices': lambda: [(staff.name, staff.name) for staff in db.session.query(Staff).all()],
            'widget': Select2Widget()
        },
        'department': {
            'label': "Департамент",
            'choices': lambda: [(department.name, department.name) for department in db.session.query(Department).all()],
            'widget': Select2Widget()
        },
        'filial': {
            'label': "Филиал",
            'choices': lambda: [(filial.name, filial.name) for filial in
                                db.session.query(Filial).all()],
            'widget': Select2Widget()
        }
    }


class SalaryGridView(ModelView):
    column_list = ['id', 'salary', 'limit', 'percent', ]


class ServiceView(ModelView):
    column_list = ['code', 'name', 'is_submit', ]
    column_labels = {
        'name': 'Наименование',
        'code': 'Код',
        'is_submit': 'Сдача работы'
    }
    form_columns = ['name', 'code', 'is_submit', ]

    column_filters = ['name', 'code', 'is_submit', ]
    column_editable_list = ['name', 'is_submit', ]
    column_default_sort = 'code'
    column_searchable_list = ['name', 'code']
    can_export = True
    export_types = ['csv', 'json', 'xlsx']
    column_sortable_list = ['name', 'code', 'is_submit']
    create_modal = True
    edit_modal = True
    page_size = 100


class ConsumablesView(ModelView):
    column_list = ['id', 'service', 'staff', 'cost', 'cost_new', ]
    column_labels = {
        'id': 'id',
        'service': 'Услуга',
        'staff': 'Сотрудник',
        "cost": "Старая цена",
        "cost_new": "Новая цена"
    }
    form_columns = ['service', 'staff', 'cost', 'cost_new', ]
    column_filters = ['staff', 'service', ]
    column_editable_list = ['cost', 'cost_new', ]
    column_default_sort = 'service'
    column_searchable_list = ['service', 'staff']
    can_export = True
    export_types = ['csv', 'json', 'xlsx']
    column_sortable_list = ['service', 'staff', 'cost', 'cost_new', ]
    create_modal = True
    edit_modal = True
    page_size = 100


class BonusView(ModelView):
    column_list = ['id', 'date_begin', 'date_end', 'staff', 'amount', 'comment', ]
    column_labels = {
        'id': 'id',
        'date_begin': 'Дата начала периода',
        'date_end': 'Дата конца периода',
        'staff': 'Сотрудник',
        'amount': 'Сумма',
        'comment': 'Комментарий'
    }
    form_columns = ['date_begin', 'date_end', 'staff', 'amount', 'comment', ]
    form_overrides = {
        'staff': SelectField
    }
    column_filters = ['date_begin', 'date_end', 'staff', 'comment']
    column_editable_list = ['date_begin', 'date_end', 'comment', 'amount']
    column_default_sort = 'date_begin'
    column_searchable_list = ['staff', 'comment']
    can_export = True
    export_types = ['csv', 'json', 'xlsx']
    column_sortable_list = ['date_begin', 'date_end', 'staff', ]
    create_modal = True
    edit_modal = True
    page_size = 100
    form_args = {
        'staff': {
            'label': 'Сотрудник',
            'choices': lambda: [(staff.name, staff.name) for staff in db.session.query(Staff).all()],
            'widget': Select2Widget()
        }
    }


class PayoutsView(ModelView):
    column_list = ['id', 'staff', 'on_date', 'amount', ]
    column_labels = {
        'id': 'id',
        'on_date': 'Дата',
        'staff': 'Сотрудник',
        'amount': 'Сумма',
    }
    form_columns = ['staff', 'on_date', 'amount', ]
    form_overrides = {
        'staff': SelectField
    }
    column_filters = ['staff', 'on_date', 'amount', ]
    column_editable_list = ['on_date', 'amount', ]
    column_default_sort = 'on_date'
    column_searchable_list = ['staff', ]
    can_export = True
    export_types = ['csv', 'json', 'xlsx']
    column_sortable_list = ['on_date', 'staff', ]
    create_modal = True
    edit_modal = True
    page_size = 100
    form_args = {
        'staff': {
            'label': 'Сотрудник',
            'choices': lambda: [(staff.name, staff.name) for staff in db.session.query(Staff).all()],
            'widget': Select2Widget()
        }
    }


class TrafficView(ModelView):
    column_list = ['id', 'staff', 'on_date', 'amount', ]
    column_labels = {
        'id': 'id',
        'on_date': 'Дата',
        'staff': 'Сотрудник',
        'amount': 'Сумма',
    }
    form_columns = ['staff', 'on_date', 'amount', ]
    form_overrides = {
        'staff': SelectField
    }
    column_filters = ['staff', 'on_date', 'amount', ]
    column_editable_list = ['on_date', 'amount', ]
    column_default_sort = 'on_date'
    column_searchable_list = ['staff', ]
    can_export = True
    export_types = ['csv', 'json', 'xlsx']
    column_sortable_list = ['on_date', 'staff', ]
    create_modal = True
    edit_modal = True
    page_size = 100
    form_args = {
        'staff': {
            'label': 'Сотрудник',
            'choices': lambda: [(staff.name, staff.name) for staff in db.session.query(Staff).all()],
            'widget': Select2Widget()
        }
    }


class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('custom_admin_index.html')

    def get_url(self, endpoint, **kwargs):
        return '/'


class CustomFileAdmin(FileAdmin):
    column_labels = {
        'name': 'Название',
        'size': 'Размер',
        'date': 'Дата',
    }

    can_delete_dirs = False
    can_rename = False


admin = Admin(app, name='', template_mode='bootstrap4', index_view=MyHomeView(name='Главная'))

path = op.join(op.dirname(__file__), 'static')
admin.add_view(CustomFileAdmin(path, '/static', name='Файлы', url='files'))

# admin.add_view(StaffView(Staff, db.session, name='Сотрудники'))
# admin.add_view(RoleView(Role, db.session, name='Должности'))
# admin.add_view(FilialView(Filial, db.session, name='Филиалы'))
# admin.add_view(DepartmentView(Department, db.session, name='Департаменты'))
# admin.add_view(SalaryView(Salary, db.session, name='Зарплаты'))
# admin.add_view(SalaryGridView(SalaryGrid, db.session, name='Зарплатные сетки'))
# admin.add_view(ServiceView(Service, db.session, name='Услуги'))
# admin.add_view(ConsumablesView(Consumables, db.session, name='Расходники'))
# admin.add_view(BonusView(Bonus, db.session, name='Надбавки'))
# admin.add_view(PayoutsView(Payouts, db.session, name='Выплаты окладов'))
# admin.add_view(TrafficView(Traffic, db.session, name='Привлеченные суммы'))
