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
// строит меню предзаказа
    function build_pred_check(){
        let is_exist_order = look_to_localStorage()
        if(is_exist_order){
            const numberTable = $('.number-table').data('tablename')
            body = '<ul class="ps-0">'
            let full_pred_price = 0.00
            for(let i = 0; i < is_exist_order[numberTable].length; i++){
                body += '<li><ul class="row ps-0">'
                body += '<li class="col-5 pe-1 text-danger">'+is_exist_order[numberTable][i].product_name+'</li>'
                body += '<li class="col-2 pe-0 ps-0">'+is_exist_order[numberTable][i].price+'</li>'
                body += '<li class="col-2 pe-0"><a href="#" class="button_plus_pred_check d-inline-block" data-product_id="'+is_exist_order[numberTable][i].product_id+'" data-price="'+is_exist_order[numberTable][i].price+'"></a></li>'
                body += '<li class="col-1 text-center ps-0 pe-0">'+is_exist_order[numberTable][i].count+'</li>'
                body += '<li class="col-2 ps-0"><a href="#" class="button_minus_pred_check d-inline-block" data-product_id="'+is_exist_order[numberTable][i].product_id+'" data-price="'+is_exist_order[numberTable][i].price+'"></a></li>'
                body += '</ul></li>'
                full_pred_price += (parseFloat(is_exist_order[numberTable][i].price) * is_exist_order[numberTable][i].count)
            }
            body += '</ul>'
            $('.pred_check__body').html(body)
            setFullPrice(full_pred_price)
        }
    };
       // добавляет к финальной стоимости full_pred_price
    function setFullPrice(full_pred_price){
        let price = parseFloat($('#full_price').text())
        price = price + full_pred_price
        $('#full_price').text(price)
    }

    // плюс клик
    function plus_pred_check(){
        $(document).on('click', '.button_plus_pred_check', function(e){
            e.preventDefault()
            tables = localStorage.getItem('tables')
            let count = $(this).parent().next().text()
            if(count <= 8){
                if(tables){
                    parseTable = JSON.parse(tables)
                    const numberTable = $('.number-table').data('tablename')
                    const price = parseFloat($(this).parent().prev().text())

                    const product_id = $(this).data('product_id')
                    for(let i=0; i < parseTable[numberTable].length; i++){
                        if(parseTable[numberTable][i].product_id === product_id){
                            parseTable[numberTable][i].count += 1
                            localStorage.setItem('tables', JSON.stringify(parseTable))
                            $(this).parent().next().text(parseTable[numberTable][i].count)
                            setFullPrice(price)
                            break
                        }
                    }
                }
            }
        })
    };
    // minus pred check
    function minus_pred_check(){
        $(document).on('click', '.button_minus_pred_check', function(e){
            e.preventDefault()
            tables = localStorage.getItem('tables')
            let count = $(this).parent().prev().text()
            if(count >= 0){
                if(tables){
                    parseTable = JSON.parse(tables)
                    const numberTable = $('.number-table').data('tablename')
                    const price = -parseFloat($(this).data('price'))
                    const product_id = $(this).data('product_id')
                    for(let i = 0; i < parseTable[numberTable].length; i++){
                        if(parseTable[numberTable][i].product_id === product_id){
                            parseTable[numberTable][i].count -= 1
                            if(parseTable[numberTable][i].count === 0){
                                parseTable[numberTable].splice(i, 1)
                                localStorage.setItem('tables', JSON.stringify(parseTable))
                                setFullPrice(price)
                                $(this).parent().parent().remove()
                                if(parseTable[numberTable].length === 0){
                                    $('.pred_check').addClass('d-none')
                                }
                                break
                            }
                            localStorage.setItem('tables', JSON.stringify(parseTable))
                            $(this).parent().prev().text(parseTable[numberTable][i].count)
                            setFullPrice(price)
                            break
                        }
                    }
                }
            }
        })
    }

    // кнопка заказ
    function order_go(){
        $(document).on('click', '#order_go', function(){
            table = localStorage.getItem('tables')
            if(table){
                parseTable = JSON.parse(table)
                table_name = Object.keys(parseTable)[0]
                data_list = Object.values(parseTable)[0]
                $.ajax({
                type: 'POST',
                url: '/tables/add_order/',
                data: {
                    csrfmiddlewaretoken: csrf_token, table_name:table_name, data_list:JSON.stringify(data_list)
                },
                dataType: 'json',
                success: function (data){
                    localStorage.clear()
                    location.reload()
                },
                error: function () {
                alert('Произошла ошибка при создании таблицы.');
                }


            })





            }
        })
    }


    build_pred_check()
    plus_pred_check()
    minus_pred_check()
    order_go()


});
