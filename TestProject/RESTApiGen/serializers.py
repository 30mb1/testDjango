from rest_framework import serializers



def get_serializer(model):
    meta_class = type('Meta', (object,), dict(model=model, fields='__all__'))
    serializer = type(
        '{}Serializer'.format(model.__name__),
        (serializers.ModelSerializer,),
        dict(Meta=meta_class)
    )
    return serializer
