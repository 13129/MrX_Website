from rest_framework import generics
from rest_framework import status, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.data_tools import models, serializers
from apps.data_tools.models import DataSourceTable
from apps.data_tools.serializers import DataSourceTableSerializer


class DataSourceTablesView(APIView):
    def post(self, request, *args, **kwargs):
        table_data_source = request.data.get('table_data_source', None)
        table_name_en = request.data.get('table_name_en', None)

        if table_data_source and table_name_en:
            print(table_data_source, table_name_en)
            obj = DataSourceTable.objects.filter(table_data_source=table_data_source,
                                                 table_name_en=table_name_en).first()
            # print(obj)
            if obj:
                return Response({'status': '1001', 'msg': '已存在表'})
            else:
                serializer = DataSourceTableSerializer(data=request.data)
                print("验真")
                if serializer.is_valid():
                    serializer.save()
                    return Response({'status': '1000', 'msg': '添加成功'})
                else:
                    return Response({'status': '1002', 'msg': '插入数据不合法'})


class DataSourceTableView(APIView):
    def put(self, request):
        table_data_source = request.data.get('table_data_source', None)
        table_name_en = request.data.get('table_name_en', None)
        if table_data_source and table_name_en:
            obj = DataSourceTable.objects.get(table_data_source=table_data_source,
                                              table_name_en=table_name_en)
            if obj:
                serializer = DataSourceTableSerializer(instance=obj, data=request.data)

                if serializer.is_valid():
                    serializer.save()
                    return Response({'status': 100, 'msg': '修改成功'})
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "参数错误"}, status=status.HTTP_400_BAD_REQUEST)


class DirectoryAPIView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = models.ThemeDirectory.objects.filter(level=0).all()
    serializer_class = serializers.ThemeDirectorySerializer

    def get(self, request, *args, **kwargs):
        parent = request.GET.get('parent', None)
        if id:
            queryset = models.ThemeDirectory.objects.filter(parent=parent).all()
        else:
            queryset = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True, fields=['id', 'name', 'direct_name_table'])
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class TableDataAPIView(mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = models.DataSourceTable.objects.all()
    serializer_class = serializers.DataSourceTableSerializer

    def post(self, request, *args, **kwargs):
        table_code = request.data.get('table_code', None)
        data_filters = request.data.get('data_filters', None)

        if table_code:
            queryset = models.DataSourceTable.objects.filter(table_code=table_code)
            data_source_url = queryset[0].table_data_source.data_source_url
            data_source_type = queryset[0].table_data_source.data_source_type
            table_name_en = queryset[0].table_name_en
            table_fields = models.DataSourceTableField.objects.filter(table_code=table_code, is_list_show=True) \
                .values('column_name_en', 'column_name_cn').order_by('ordinal_position')
            print(table_fields)
            if data_filters:
                for f in data_filters:
                    field = f['field']
                    wildcard = f['wildcard']
                    value = f['value']
            field_name_en = ','.join(list(table_fields.values_list("column_name_en", flat=True)))
            field_name_zh = list(table_fields.values_list("column_name_cn", flat=True))
            from sqlalchemy import create_engine
            import pandas as pd
            engine = create_engine(data_source_url)

            sql = "select {} from {} limit 15".format(field_name_en, table_name_en)
            df = pd.read_sql(sql, con=engine)
            df.columns = field_name_zh
            data = df.to_dict('index')
        return Response({"data": data}, status=status.HTTP_200_OK)
