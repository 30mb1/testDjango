from django.apps import apps
from rest_framework import viewsets
from rest_framework import routers
from .serializers import get_serializer

# TODO rewrite with django-filters
def get_queryset(self):
    # getting request params
    params = self.request.GET.dict()
    # getting queryset
    queryset = self.queryset.all()
    # need sorting?
    sort = params.pop('sort', None)
    # need limit?
    limit = params.pop('limit', None)
    if limit: limit = int(limit)

    params_exist = [i.name for i in self.model._meta.get_fields()]
    # removing irrelevant params
    for key in list(params.keys()):
        if key not in params_exist: params.pop(key)

    queryset = queryset.filter(**params)
    if sort:
        queryset = queryset.order_by(sort)
    queryset = queryset[:limit]
    return queryset

def get_all_views():
    all_models = apps.get_models()
    all_views = []

    for model in all_models:
        serializer = get_serializer(model)
        view = type(
            '{}View'.format(model.__name__),
            (viewsets.ModelViewSet,),
            dict(
                serializer_class=serializer,
                model=model,
                queryset=model.objects.all(),
                get_queryset=get_queryset
            )
        )

        all_views.append(view)
    return all_views


def get_all_urls():
    r = routers.SimpleRouter()
    for view in get_all_views():
        r.register(view.model.__name__.lower(), view)
    return r.urls
