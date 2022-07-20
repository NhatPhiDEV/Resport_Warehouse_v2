from django.db import connection
from rest_framework import viewsets,generics,status
from rest_framework.response import Response
from rest_framework.decorators import action
class ReportsViewSet(viewsets.ViewSet): 
    @action(methods=['get'], detail=False, url_path='get-fields')
    def get_fields(self,request):
        cursor = connection.cursor()
        try:
            sql = 'SELECT key_code,value_code,table_name FROM allcode WHERE is_active = 1'
            cursor.execute(sql)
            result = dictFetchall(cursor)
            return Response(result,status=status.HTTP_200_OK)
        finally:
            cursor.close()

def dictFetchall(cursor):
    columns = cursor.description
    result = [] 
    for value in cursor.fetchall():        
        tmp = {columns[index][0]: column for index, column in enumerate(value)}
        result.append(tmp)      

    return result
