from django.db import connection
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from apps.commons.params import * 
class ReportsViewSet(viewsets.ViewSet): 
    @action(methods=['get'], detail=False, url_path='get-fields')
    def get_fields(self,request):
        """ function load filed

        Returns:
            result: list fields (type json)
        """
        with connection.cursor() as cursor:
            cursor.callproc(PROC_ALLCODE_NAME)
            result = renderData(cursor)
            return Response(result,status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=FilterParam)  
    @action(methods=['post'], detail=False, url_path='filter')
    def get_data_filter(self,request):   
        """ filter data
        Args:
            number_select (str): (ex: opt_budget,opt_expect_revenue)                    
            ==> belong to currency
            string_select (str): (ex: ws_code,emp_name,dept_name,opt_bid_open_date)     
            ==> filed select
            date_filter (str): (ex: opt_bid_open_date)                                  
            ==> type date using filter
            from_date (str): (ex: 2019/01/01)                                           
            ==> date start filter
            to_date (str):(ex: 2022/12/21)                                              
            ==> date end filter 
            group_by (str): YEAR                                                        
            ==> type group (DAY or MONTH or YEAR ....)
            extras (str): (ex: cus_code IN('CUS..2021.0040','KT259','CUS..2021.0014'))  
            ==> using filter cus_node = CUS..2021.0040 or KT259 or CUS..2021.0014
            limits (str): 4                                                             
            ==> top (4)
            desc (str): DESC or ASC                                                     
            ==> using get top min or max
        Returns:
            result(json): 
        """

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
        """ get departments  
        Returns:
            result: list departments type json
        """
        result = dictFetchall(DEPT_SELECT,DEPT_WHERE)
        return Response(result,status=status.HTTP_200_OK)
    @action(methods=['get'], detail=False, url_path='customer')
    def get_customer(self,request):
        """ get customer  
        Returns:
            result: list customer type json
        """
        result = dictFetchall(CUS_SELECT,CUS_WHERE)
        return Response(result,status=status.HTTP_200_OK)
    @action(methods=['get'], detail=False, url_path='employee')
    def get_employee(self,request):
        """ get employee  
        Returns:
            result: list employee type json
        """
        result = dictFetchall(EMP_SELECT,EMP_WHERE)
        return Response(result,status=status.HTTP_200_OK)
    @action(methods=['get'], detail=False, url_path='workspace')
    def get_workspace(self,request):
        """ get workspace  
        Returns:
            result: list workspace type json
        """
        result = dictFetchall(WS_SELECT,WS_WHERE)
        return Response(result,status=status.HTTP_200_OK)
    @swagger_auto_schema(request_body=ParamReportsData)  
    @action(methods=['post'], detail=False, url_path='data-custom')
    def get_custom(self,request):
        """ get custom

        Args:
            params (str): ex: ws_code,emp_name,dept_name,opt_bid_open_date

        Returns:
            result(json): list data (ws_code,emp_name,dept_name,opt_bid_open_date)
        """
        if not (params := request.data.get('params')):
            return Response("No data",status=status.HTTP_403_FORBIDDEN)         
        value_selected = f'DISTINCT {format_date(params)}'
        result = dictFetchall(value_selected,'1=1')
        return Response(result,status=status.HTTP_200_OK)
# Format string select
def format_str(string_select,date_filter):
    """ format string select

    Args:
        string_select (str): type string select (ex: ws_code,emp_name,dept_name,opt_bid_open_date,opt_bid_close_date)
        date_filter (str): type date filter (ex: opt_bid_open_date)

    Returns:
        result: ws_code,emp_name,dept_name,opt_bid_close_date
    """
    if string_select != 'NULL':
        return ''.join(f'{item},' for item in string_select.split(',') if item != date_filter)
    else:
        return ''
# Format number select
def format_num(number_select,group_by):
    """ format number select

    Args:
        number_select (str): _description_
        group_by (str): _description_

    Returns:
        ex: ,Sum(opt_budget) as opt_budget
    """
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
    """format date dd/MM/yyyy

    Args:
        params (str): ex: ws_code,emp_name,dept_name,opt_bid_open_date

    Returns:
        date_convert: ex: ws_code,emp_name,dept_name,IFNULL(DATE_FORMAT(opt_bid_open_date,'%d/%m/%Y'),'') AS opt_bid_open_date
    """
    result = []
    temp = params.split(",")
    for item in temp:
        if item in ['opt_bid_open_date','opt_bid_close_date','scon_date_locked','scon_sign_date','scon_posting_date']:
            item = f"IFNULL(DATE_FORMAT({item},'%d/%m/%Y'),'') AS {item}"
        result.append(item)
    return ''.join(f'{value}, ' for value in result).rstrip(", ")

def format_group_by(group_by,date_filter):
    """ function format group by
    Args:
        group_by (str): type group by (ex: YEAR, MONTH, DAY, ...)
        date_filter (str): type date filter (ex: opt_bid_open_date, opt_bid_close_date)

    Returns:
        group by: ex: GROUP BY YEAR(opt_bid_open_date)
    """
    if (group_by == 'NULL'):
        return ''
    elif group_by in ['DAY', 'MONTH', 'YEAR']:
        return f'GROUP BY {group_by}({date_filter})'
    else:
        return f'GROUP BY {group_by}'

def format_date_filter_follow_group_by(group_by,date_filter):
    """ function format date follow group by

    Args:
        group_by (str): type group by (ex: YEAR)
        date_filter (str): type date filter (ex: opt_bid_open_date)

    Returns:
        date_result: ex: YEAR(opt_bid_open_date) as opt_bid_open_date_year
    """
    if group_by != 'NULL' and group_by in ['DAY', 'MONTH', 'YEAR'] and group_by == 'DAY' or group_by not in ['DAY', 'MONTH', 'YEAR']:
        return f" IFNULL(DATE_FORMAT({date_filter},'%d/%m/%Y'),'') AS {date_filter}"
    elif group_by != 'NULL' and group_by == 'MONTH':
        return f' MONTH({date_filter}) AS {date_filter}_month, YEAR({date_filter}) AS {date_filter}_year'
    elif group_by != 'NULL':
        return f' YEAR({date_filter}) as {date_filter}_year'
    else:
        return f' {date_filter}'

def dictFetchall(params, conditions):
    """ function fetchall data (using procedure)

    Args:
        params (str): object to get 
        conditions (str): condition get

    Returns:
        result(json): list data params
    """
    with connection.cursor() as cursor:
        cursor.callproc(PROC_AUTOCOMPLETE_NAME,[params,conditions])
        result = renderData(cursor)     
    return result

def renderData(cursor):
    """ function convert tuple to json
    Returns:
        result(json)
    """
    columns = cursor.description
    result = [] 
    for value in cursor.fetchall():        
        tmp = {columns[index][0]: column for index, column in enumerate(value)}
        result.append(tmp)      
    return result
    

 