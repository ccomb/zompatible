from zope.app.generations.generations import SchemaManager

ZompatibleSchemaManager = SchemaManager(
    minimum_generation=1,
    generation=1,
    package_name='zompatible.generations'
)

 