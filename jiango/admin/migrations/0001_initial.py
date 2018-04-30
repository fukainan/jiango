# Generated by Django 2.0.4 on 2018-04-21 23:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='名称')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, null=True, verbose_name='用户名')),
                ('datetime', models.DateTimeField(auto_now=True, db_index=True, verbose_name='时间')),
                ('level', models.SmallIntegerField(choices=[(10, '调试'), (20, '信息'), (25, '成功'), (30, '注意'), (40, '错误')], db_index=True, default=25, verbose_name='级别')),
                ('action', models.SmallIntegerField(choices=[(0, '无'), (10, '增加'), (20, '读取'), (30, '更新'), (40, '删除'), (1000, '登陆'), (1001, '退出')], db_index=True, default=0, verbose_name='动作')),
                ('app_label', models.CharField(max_length=100, null=True)),
                ('content', models.TextField(null=True)),
                ('view_name', models.CharField(max_length=100, null=True)),
                ('view_args', models.CharField(max_length=100, null=True)),
                ('view_kwargs', models.CharField(max_length=100, null=True)),
                ('remote_ip', models.GenericIPAddressField(null=True)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('codename', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='权限名')),
            ],
            options={
                'ordering': ('codename',),
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='用户名')),
                ('password_digest', models.CharField(editable=False, max_length=32)),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='有效用户')),
                ('is_superuser', models.BooleanField(db_index=True, default=False, verbose_name='超级用户')),
                ('login_at', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('login_token', models.CharField(db_index=True, editable=False, max_length=32, null=True)),
                ('login_fail_at', models.DateTimeField(db_index=True, editable=False, null=True, verbose_name='最近登陆失败日期')),
                ('login_fails', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='最近登陆失败次数')),
                ('join_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('request_at', models.DateTimeField(db_index=True, editable=False, null=True, verbose_name='最近请求时间')),
                ('groups', models.ManyToManyField(blank=True, help_text='如果为超级用户则已经拥有所有用户组无需选择', to='admin.Group', verbose_name='用户组')),
                ('permissions', models.ManyToManyField(blank=True, help_text='如果为超级用户则已经拥有所有权限无需选择', to='admin.Permission', verbose_name='额外权限')),
            ],
            options={
                'verbose_name': '管理员',
                'ordering': ('-request_at',),
            },
        ),
        migrations.AddField(
            model_name='log',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='admin.User', verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='group',
            name='permissions',
            field=models.ManyToManyField(blank=True, help_text=None, to='admin.Permission', verbose_name='权限'),
        ),
    ]
