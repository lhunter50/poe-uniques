from django.db import migrations

def assert_no_null_poe_ninja_id(apps, schema_editor):
    UniqueItem = apps.get_model("catalog", "UniqueItem")
    missing = UniqueItem.objects.filter(poe_ninja_id__isnull=True).count()
    if missing:
        raise RuntimeError(
            f"{missing} UniqueItem rows have NULL poe_ninja_id. "
            "Re-run importer or fix the rows before making poe_ninja_id non-null."
        )

class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0012_alter_uniqueitem_poe_ninja_id"),
    ]

    operations = [
        migrations.RunPython(assert_no_null_poe_ninja_id, migrations.RunPython.noop),
    ]
