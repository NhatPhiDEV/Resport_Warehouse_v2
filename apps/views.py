from django.db import connection
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from apps.commons.params import * 
class ReportsViewSet(viewsets.ViewSet): 
    @action(methods=['get'], detail=False, url_path='get-fields')
    def get_fields(self,request):
        with connection.cursor() as cursor:
            sql = 'SELECT key_code,value_code,table_name FROM allcode WHERE is_active = 1'
            cursor.execute(sql)
            result = renderData(cursor)
            return Response(result,status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=FilterParam)  
    @action(methods=['post'], detail=False, url_path='filter')
    def get_workspace(self,request):  # sourcery skip: remove-redundant-if
        # Get values in request
        number_select = request.data.get('number_selected')
        string_select = request.data.get('string_selected')
        date_filter = request.data.get('date_filter')
        from_date = request.data.get('from_date')
        to_date = request.data.get('to_date')
        group_by = request.data.get('group_by')
        extras =  request.data.get('extras')
        # covert result
        group_by_result = ''
        date_result = ''
        number_selected_result = ''
        # Check condition group by
        if(group_by == 'NULL'):
            group_by_result = ''
            date_result = f',{date_filter}'
        elif(group_by == 'DAY' or group_by == 'MONTH' or group_by == 'YEAR'):
            # Convert date follow group_by
            match group_by:
                case 'DAY':
                    date_result = f',DATE({date_filter}) AS DATE'
                case 'MONTH':
                    date_result = f',MONTH({date_filter}) AS MONTH, YEAR({date_filter}) AS YEAR'
                case '':
                    date_result = f',YEAR({date_filter}) as YEAR'
            group_by_result = f'GROUP BY {group_by}({date_filter})'
        else:
            group_by_result = f'GROUP BY {group_by}'
            date_result = f',DATE({date_filter}) AS DATE'
        # handle selected
        temp = number_select.split(",")
        result_temp = ''.join(f'Sum({value}) AS {value}, ' for value in temp)
        # check conditions sum
        if group_by_result != '':
            number_selected_result = result_temp
        else:
            number_selected_result = f'{number_select},'
        # SELECT query
        selected = f'{number_selected_result}{string_select}{date_result}'
        # WHERE query
        conditions = f"{extras} AND {date_filter} BETWEEN DATE('{from_date}') AND DATE('{to_date}') {group_by_result} ORDER BY {date_filter};"
        # Format result and Render json
        result = dictFetchall(selected,conditions)
        return Response(result,status=status.HTTP_200_OK)

class GetDataViewSet(viewsets.ViewSet):
    @action(methods=['get'], detail=False, url_path='departments')
    def get_departments(self,request):
        result = dictFetchall(DEPT_SELECT,DEPT_WHERE)
        return Response(result,status=status.HTTP_200_OK)
    @action(methods=['get'], detail=False, url_path='customer')
    def get_customer(self,request):
        result = dictFetchall(CUS_SELECT,CUS_WHERE)
        return Response(result,status=status.HTTP_200_OK)
    @action(methods=['get'], detail=False, url_path='employee')
    def get_employee(self,request):
        result = dictFetchall(EMP_SELECT,EMP_WHERE)
        return Response(result,status=status.HTTP_200_OK)
    @action(methods=['get'], detail=False, url_path='workspace')
    def get_workspace(self,request):
        result = dictFetchall(WS_SELECT,WS_WHERE)
        return Response(result,status=status.HTTP_200_OK)
    @swagger_auto_schema(request_body=ParamReportsData)  
    @action(methods=['post'], detail=False, url_path='data-custom')
    def get_custom(self,request):
        if not (params := request.data.get('params')):
            return Response("No data",status=status.HTTP_403_FORBIDDEN)
        result = dictFetchall(params,'1=1')
        return Response(result,status=status.HTTP_200_OK)
          
def dictFetchall(params, conditions):
    with connection.cursor() as cursor:
        cursor.callproc(PROC_AUTOCOMPLETE_NAME,[params,conditions])
        result = renderData(cursor)     
    return result

def renderData(cursor):
    columns = cursor.description
    result = [] 
    for value in cursor.fetchall():        
        tmp = {columns[index][0]: column for index, column in enumerate(value)}
        result.append(tmp)      
    return result


