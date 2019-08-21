$("#id_begin_date").datetimepicker({
        format: 'yyyy-mm-dd hh:ii',
        language: 'zh-CN',
        autoclose:true,
        startDate:new Date()
    }).on("click",function(){
        $("#id_begin_date").datetimepicker("setEndDate",$("#id_end_date").val())
    });

$("#id_end_date").datetimepicker({
        format: 'yyyy-mm-dd hh:ii',
        language: 'zh-CN',
        autoclose:true,
        startDate:new Date()
    }).on("click",function(){
        $("#id_begin_date").datetimepicker("setEndDate",$("#id_end_date").val())
    });