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
    def get_data_filter(self,request):   # sourcery skip: assign-if-exp, remove-redundant-if
        # Get values in request
        number_select = request.data.get('number_selected')
        string_select = request.data.get('string_selected')
        date_filter = request.data.get('date_filter')
        from_date = request.data.get('from_date')
        to_date = request.data.get('to_date')
        group_by = request.data.get('group_by')
        extras =  request.data.get('extras')
        limits = request.data.get('limits')
        desc = request.data.get('desc')
        # covert result
        if group_by == 'NULL':
            group_by_result = ''
        group_by_result = format_group_by(group_by=group_by,date_filter=date_filter)
        date_result = format_date_filter_follow_group_by(group_by=group_by,date_filter=date_filter)
        string_select_result  = f'{format_date(format_str(string_select,date_filter))},'
        number_selected_result = format_num(number_select=number_select,group_by=group_by)
        order_by_result = format_top(limits=limits,desc=desc,number_select=number_select,date_filter=date_filter)
        # SELECT query
        
        if group_by in ['dept_code','emp_code','cus_code'] :
            selected = f'DISTINCT {group_by}, {string_select_result}{date_result}{number_selected_result}'
        else:
            selected = f'DISTINCT {string_select_result}{date_result}{number_selected_result}'
        # WHERE query
        conditions = f"{extras} AND {date_filter} BETWEEN DATE('{from_date}') AND DATE('{to_date}') {group_by_result}{order_by_result}"
        # Format result and Render json
        print(selected)
        print(conditions)
        result = dictFetchall(selected,conditions)
        return Response(result,status=status.HTTP_200_OK)        
# Get data viewSet
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
        value_selected = f'DISTINCT {format_date(params)}'
        result = dictFetchall(value_selected,'1=1')
        return Response(result,status=status.HTTP_200_OK)
# Format string select
def format_str(string_select,date_filter):
    if string_select != 'NULL':
        return ''.join(f'{item},' for item in string_select.split(',') if item != date_filter)
    else:
        return ''
# Format number select
def format_num(number_select,group_by):
    temp = number_select.split(",")
    result_temp = ''.join(f', Sum({value}) AS {value} ' for value in temp)
    # check number selected
    if number_select == 'NULL':
        return ''
    elif group_by != 'NULL':
        return result_temp
    else:
        return f'{number_select}'
# Format top
def format_top(limits,desc,number_select,date_filter):
    if limits != 'NULL' and desc in['DESC','ASC']  and number_select != 'NULL':
        return f' ORDER BY {number_select} {desc} LIMIT {limits};'
    elif limits != 'NULL' and desc in ['DESC','ASC']:
        return f' ORDER BY DATE({date_filter}) {desc} LIMIT {limits};'
    else:
        return ''
# Convert date dd/MM/yyyy
def format_date(params):
    result = []
    temp = params.split(",")
    for item in temp:
        if item in ['opt_bid_open_date','opt_bid_close_date','scon_date_locked','scon_sign_date','scon_posting_date']:
            item = f"IFNULL(DATE_FORMAT({item},'%d/%m/%Y'),'') AS {item}"
        result.append(item)
    return ''.join(f'{value}, ' for value in result).rstrip(", ")

def format_group_by(group_by,date_filter):
    if (group_by == 'NULL'):
        return ''
    elif group_by in ['DAY', 'MONTH', 'YEAR']:
        return f'GROUP BY {group_by}({date_filter})'
    else:
        return f'GROUP BY {group_by}'

def format_date_filter_follow_group_by(group_by,date_filter):
    if group_by != 'NULL' and group_by in ['DAY', 'MONTH', 'YEAR'] and group_by == 'DAY' or group_by not in ['DAY', 'MONTH', 'YEAR']:
        return f" IFNULL(DATE_FORMAT({date_filter},'%d/%m/%Y'),'') AS {date_filter}"
    elif group_by != 'NULL' and group_by == 'MONTH':
        return f' MONTH({date_filter}) AS {date_filter}_month, YEAR({date_filter}) AS {date_filter}_year'
    elif group_by != 'NULL':
        return f' YEAR({date_filter}) as {date_filter}_year'
    else:
        return f' {date_filter}'

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


 