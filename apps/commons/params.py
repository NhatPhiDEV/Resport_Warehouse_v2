from rest_framework import serializers

# AUTO COMPLETE TEXT
PROC_AUTOCOMPLETE_NAME = "AutoComplete_Text"
PROC_ALLCODE_NAME = "getAllcode"
#1. DEPARTMENTS 
DEPT_SELECT = "DISTINCT dept_code,dept_name"
DEPT_WHERE  = "dept_name != '' AND dept_code != '' ORDER BY dept_name;" 
#2. CUSTOMER 
CUS_SELECT  = "DISTINCT cus_code,cus_name"
CUS_WHERE   = "cus_code != '' AND cus_name != '' ORDER BY cus_name;"
#3. EMPLOYEE
EMP_SELECT  = "DISTINCT emp_code,emp_name"
EMP_WHERE   = "emp_code != '' AND emp_name != '' ORDER BY emp_name;"
#4. WORKSPACE
WS_SELECT = "DISTINCT ws_code"
WS_WHERE = "ws_code != '' ORDER BY ws_code;"
#5. PARAM
class ParamReportsData(serializers.Serializer):
    params = serializers.CharField( required= False)

class FilterParam(serializers.Serializer):
    number_selected = serializers.CharField( required= False)
    string_selected = serializers.CharField( required= False)
    date_filter = serializers.CharField( required= False)
    from_date = serializers.CharField( required= False)
    to_date = serializers.CharField( required= False)
    group_by = serializers.CharField( required= False)
    extras = serializers.CharField( required= False)
    limits = serializers.CharField( required= False)
    desc = serializers.CharField( required= False)