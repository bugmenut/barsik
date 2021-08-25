from behave import *
from django.test import Client
from django.contrib import auth
from django.contrib.auth.models import User, Group
use_step_matcher("re")


@given("Пользователь admin авторизуется")
def step_impl(context):
    context.user = User.objects.create_superuser(username='admin', password='admin')
#   можно использовать context.test.client, это мне Рамиль подсказал, я сам не додумался
    context.c = Client()
    response = context.c.post('/admin/login/', {'username': 'admin', 'password': 'admin'}, follow=True)
    context.user_client = auth.get_user(context.c)
    assert context.user_client.is_authenticated, "Админ не смог залогиниться"
    assert response.status_code == 200, "Статус код не 200!"


@step("Пользователь admin создаёт группу 'Good Boy Group'")
def step_impl(context):
    context.barsik = 'Good Boy Group'
    response2 = context.c.post('/admin/auth/group/add/', {'name': 'Good Boy Group', '_save': 'Save'}, follow=True)
    assert response2.status_code == 200, "Статус код не 200!"
    context.barsik_dict = {'name': 'Good Boy Group'}
    assert context.barsik_dict in Group.objects.values('name'), "Barsik не в списке групп!"


@then("Группа 'Good Boy Group' оказывается в списке групп")
def step_impl(context):
    assert context.barsik_dict in Group.objects.values('name'), "Barsik не в списке групп!"


@when("Пользователь admin удаляет группу")
def step_impl(context):
    print(Group.objects.get(name=context.barsik).id)
    group_id = Group.objects.get(name=context.barsik).id
    context.url_id = f'/admin/auth/group/{group_id}/delete/'
    response3 = context.c.post(context.url_id,
                               {'post': 'yes'},
                               follow=True)
    assert response3.status_code == 200, "Статус код не 200!"


@then("Группы 'Good Boy Group' больше нет в списке групп")
def step_impl(context):
    assert not Group.objects.filter(name=context.barsik).exists(), "Группа с таким названием всё ещё в списке!"
