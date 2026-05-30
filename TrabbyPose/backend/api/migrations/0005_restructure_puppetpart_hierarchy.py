# Generated migration: Restructure PuppetPart to hierarchical model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_puppetpart_options_puppetpart_category_and_more'),
    ]

    operations = [
        # Add new fields first
        migrations.AddField(
            model_name='puppetpart',
            name='subcategory',
            field=models.CharField(default='uncategorized', help_text='Subcategory within the category (e.g., \'Face\', \'Eyes\', \'Left Upper Arm\')', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='puppetpart',
            name='order',
            field=models.PositiveIntegerField(default=0, help_text='Display order within subcategory'),
        ),
        
        # Change category choices to use display values
        migrations.AlterField(
            model_name='puppetpart',
            name='category',
            field=models.CharField(
                choices=[('Head', 'Head'), ('Limbs', 'Limbs'), ('Torso', 'Torso'), ('Accessories', 'Accessories')],
                help_text='Main category (Head, Limbs, Torso, Accessories)',
                max_length=20
            ),
        ),
        
        # Remove part_type field
        migrations.RemoveField(
            model_name='puppetpart',
            name='part_type',
        ),
        
        # Update model options: ordering, unique_together, and indexes
        migrations.AlterModelOptions(
            name='puppetpart',
            options={
                'ordering': ['category', 'subcategory', 'order', 'name'],
                'verbose_name': 'Puppet Part',
                'verbose_name_plural': 'Puppet Parts'
            },
        ),
        
        migrations.AlterUniqueTogether(
            name='puppetpart',
            unique_together={('category', 'subcategory', 'name')},
        ),
        
        migrations.AddIndex(
            model_name='puppetpart',
            index=models.Index(fields=['category', 'subcategory'], name='api_puppet_p_categor_idx'),
        ),
    ]
