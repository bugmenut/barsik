from behave import *
from django.test import Client
from django.contrib import auth
from django.contrib.auth.models import User


@given("Приложение запущено")
def step_impl(context):
    pass


@when("Перехожу по адресу /admin/")
def step_impl(context):
    c = Client()
    response = c.get('/admin/', follow=True)
    context.status_code = response.status_code


@then("Приложение работает как положено, получаю статус код 200")
def step_impl(context):
    assert context.status_code == 200, 'Статус не 200'


@given("Существует авторизуемый пользователь username: admin password: admin")
def step_impl(context):
    context.user = User.objects.create_superuser(username='admin', password='admin')


@when("Перехожу по адресу /admin/login/ и ввожу корректные логин и пароль")
def step_impl(context):
    c = Client()
    response = c.post('/admin/login/', {'username': 'admin', 'password': 'admin'}, follow=True)
    context.user_client = auth.get_user(c)
    context.status_code = response.status_code


@then("Успешная авторизация, статус пользователя аутентифицированный")
def step_impl(context):
    assert context.user_client.is_authenticated, "Не удалось залогиниться как админ"
    assert context.status_code == 200, "Статус не 200"


@given("Имеем таблицу с некорректными username и/или password")
def step_impl(context):
    pass


@when("Перехожу по адресу /admin/login/ и ввожу некорректные данные из таблицы")
def step_impl(context):
    context.non_auth_login = False
    c = Client()
    for row in context.table:
        response = c.post('/admin/login/', {'username': row['username'], 'password': row['password']}, follow=True)
        context.user = auth.get_user(c)
        context.status_code = response.status_code
        if context.user.is_authenticated:
            context.non_auth_login = True
        assert not context.user.is_authenticated, "Удалось залогиниться с неверными данными!"
        assert context.status_code == 200, "Статус не 200"


@then("Авторизация не происходит ни в одном из случаев в таблице")
def step_impl(context):
    assert not context.non_auth_login, "Удалось залогиниться с неверными данными!"
