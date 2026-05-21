from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.CharField(
                choices=[('student', 'Ученик'), ('parent', 'Родитель')],
                default='student',
                max_length=20,
                verbose_name='роль',
            ),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='grade',
            field=models.IntegerField(
                blank=True,
                choices=[(8, '8 класс'), (9, '9 класс'), (10, '10 класс'), (11, '11 класс')],
                null=True,
                verbose_name='класс',
            ),
        ),
    ]
