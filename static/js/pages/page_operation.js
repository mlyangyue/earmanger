/**
 * Created by wangranming on 2017/6/9.
 */
function page_operation(page,total_page) {
        $("[name='page_elem']").removeClass('active');
        $("#page_"+page).addClass('active');
        $("[name='page_elem']").css("display",'none');
        for (var i=page ; i>0&&i>=page-2;i--){
            $("#page_"+i).css('display','');
        }
        for (var j=page; j<=total_page&&j<=page+2;j++){
            $("#page_"+j).css('display','');
        }

        var next_page = page + 1;
        var pre_page  = page - 1;
        if (next_page > total_page
        
        ){
            next_page = page;
        }
        if (pre_page < 1){
            pre_page = page;
        }
        $("#page_before").attr('onclick',"page_data("+pre_page+")");
        $("#page_next").attr('onclick',"page_data("+next_page+")");
    }