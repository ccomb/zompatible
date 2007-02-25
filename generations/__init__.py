from zope.app.generations.generations import SchemaManager

ZompatibleSchemaManager = SchemaManager(
    minimum_generation=2,
    generation=2,
    package_name='zompatible.generations'
)

 