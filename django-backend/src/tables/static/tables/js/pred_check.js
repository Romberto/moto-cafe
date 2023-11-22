window.addEventListener('load', function(){


// смотрим есть ли для этого стола заказы в localStorage
    function look_to_localStorage(){
        const numberTable = $('.number-table').data('tablename')
        let tableStorage = localStorage.getItem('tables')
        if(tableStorage){
            parseTable = JSON.parse(tableStorage)
            if(parseTable.hasOwnProperty(numberTable) && parseTable[numberTable].length > 0){
                $('.pred_check').removeClass('d-none')
                return parseTable
            }
        }else{
            return false
        }
    }

    function build_pred_check(){
        let is_exist_order = look_to_localStorage()
        if(is_exist_order){
            const numberTable = $('.number-table').data('tablename')
            body = '<ul>'
            for(let i = 0; i < is_exist_order[numberTable].length; i++){
                body += '<li><ul class="row">'
                body += '<li class="col-6">'+is_exist_order[numberTable][i].product_name+'</li>'
                body += '<li class="col-2"></li>'
                body += '<li class="col-2">'+is_exist_order[numberTable][i].count+'</li>'
                body += '<li class="col-2"></li>'
                body += '</ul></li>'
            }
            body += '</ul>'
            $('.pred_check__body').html(body)

        }
    };

    build_pred_check()

});
