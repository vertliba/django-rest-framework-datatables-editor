import re

from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet


class EditorModelMixin(object):
    pass


class DatatablesEditorModelViewSet(EditorModelMixin, ModelViewSet):

    @staticmethod
    def get_post_date(post):
        def read_date(data_in, data_out, rest_of_line):
            field_name = data_in[0]
            if not isinstance(data_out.get(field_name), dict):
                new_data_point = {}
                data_out[field_name] = new_data_point
            else:
                new_data_point = data_out[field_name]
            if len(data_in) == 2:
                new_data_point[data_in[1]] = rest_of_line
            else:
                read_date(data_in[1:], new_data_point, rest_of_line)

        data = {}
        for (line, value) in post.items():
            if line.startswith('data'):
                line_data = re.findall(r"\[([^\[\]]*)\]", line)
                read_date(line_data, data, value)
        return data

    @action(detail=False, url_name='editor', methods=['post'])
    def editor(self, request):
        post = request.POST
        act = post['action']
        data = self.get_post_date(post)

        return_data = []
        if act == 'edit' or act == 'remove' or act == 'create':
            for elem_id, changes in data.items():
                if act == 'create':
                    serializer = self.serializer_class(
                        data=changes,
                        context={'request': request}
                    )
                    if not serializer.is_valid():  # pragma: no cover
                        raise ValidationError(serializer.errors)
                    serializer.save()
                    return_data.append(serializer.data)
                    continue

                elem = get_object_or_404(self.queryset, pk=elem_id)
                if act == 'edit':
                    serializer = self.serializer_class(
                        instance=elem, data=changes,
                        partial=True, context={'request': request}
                    )
                    if not serializer.is_valid():  # pragma: no cover
                        raise ValidationError(serializer.errors)
                    serializer.save()
                    return_data.append(serializer.data)
                elif act == 'remove':
                    elem.delete()

        return JsonResponse({'data': return_data})
