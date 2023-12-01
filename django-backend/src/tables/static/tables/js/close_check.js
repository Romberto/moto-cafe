window.addEventListener('load', function(){

// смотрим есть ли в открытом столе какие нибудь заказы
    function look_empty_check(){
        let full_price = $('#full_price').text()
        if(full_price === '0'){
            return true
        }else{
            return false
        }
    }


// обработка нажатия на кнопку закрыть стол
    function click_close_check(){
        $('#js_close_check').on('click', function(){
            if(look_empty_check()){
                ajax_close_empty_check()
            }else{
                ajax_close_full_check()
            }
        });
    }

    function ajax_close_empty_check(){
        let number_table = $('.number-table').data('tablename')
        $.ajax({
            url:'/tables/ajax_close_empty_check/',
            data: {'table': number_table},
            method: 'get',
            dataType: 'json',
            success: function(response){
                location.reload()
            }
        })
    };

    function ajax_close_full_check(){
        let number_table = $('.number-table').data('tablename')

        $.ajax({
            url:'/tables/ajax_close_full_check/',
            data: {
                    csrfmiddlewaretoken: csrf_token, table:number_table
                },
            method: 'post',
            dataType: 'json',
            success: function(response){
                location.reload()
            }
        })
    }

    click_close_check()
});