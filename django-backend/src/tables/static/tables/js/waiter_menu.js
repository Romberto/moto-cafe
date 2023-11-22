window.addEventListener('load', function(){

    // запрос для получения всех категорий
    function get_category(callback){
        $.ajax({
            url:'/api/v1/category/',
            method: 'get',
            dataType: 'json',
            success: function (response){
                callback(response)
            },
            error: function (error) {
                  console.error('Ошибка при получении категорий:', error);
                  callback(null);
                }
        })
    };

    // строим меню
    function build_menu_category(data){
        let li = ""
        $.each(data, function(inf, category){
              li += "<li><button class='btn btn-success mb-2 category-link' type='button' data-category='"+category.id+"'>"+category.title+"</button></li>"
        })
        return li
    };
    // открытие меню
    function menu(){
    $('#js_add_product').on('click', function(){
        $('.menu_waiter').addClass('show')
        let fullPrice = $('#full_price').text()
        let tableNumber = $('.number-table').data('tablename')
        get_category(function (categories) {
            let elements = '<h1 data-table="'+tableNumber+'" id="table-menu">Стол № '+tableNumber+'</h1>'
            elements += build_menu_category(categories)
            $('.menu_category-list').html(elements)
            $('.full_price span').text(fullPrice)
        })
    });
    }

    // получаем перечень продуктов категории
    $(document).on('click', '.category-link', function(){
        let categoryId = $(this).data('category')
        let categoryName = $(this).text()
        let tableNumber = $('#table-menu').data('table')
        tables = localStorage.getItem('tables')
        parseTables = JSON.parse(tables)
        $.ajax({
            url:'/api/v1/product/?category='+ categoryId,
            method: 'get',
            dataType: 'json',
            success: function(response){
                category_page = '<h1 data-table="'+tableNumber+'" id="category-table">Стол №'+tableNumber+'</h1>'
                category_page += '<h3 class="mb-2">'+categoryName+'</h3>'
                category_page += '<div class="menu-block">'
                category_page += '<ul class="menu-list ps-1">'
                category_page += '<button class="btn btn-info mb-3" id="add_pred_check">Добавить к счёту</button>'

                $.each(response, function(index, product){
                    category_page += '<li class="row mb-2">'
                        category_page += '<p class="col-7 mb-1 product_name">'+product.title+'</p>'
                        category_page += '<a href="#" type="button" class="plus_button col-2" data-product="'+product.id+'" data-price="'+product.price+'"></a>'
                        check_product = false
                        if(parseTables){
                            check_product = is_exist_in_localStorage(product.id, parseTables[tableNumber])
                        }
                        if(check_product){
                            category_page += '<p class="col-1 mb-1 count">'+check_product+'</p>'
                        }else{
                            category_page += '<p class="col-1 mb-1 count">0</p>'
                        }
                        category_page += '<a href="#" type="button" class="minus_button col-2" data-product="'+product.id+'"></a>'
                    category_page += '</li>'
                })
                category_page += '</ul>'
                category_page += '</div>'
                $('.menu_waiter').html(
                    category_page
                )
            }
        })
    });

     // закрытие меню
    $('#close_menu').on('click',function(){
        $('.menu_waiter').removeClass('show')
    })
    // фуркция плюс
    function clickPlus(){
        $(document).on('click', '.plus_button', function(e){
            e.preventDefault()
            let count = parseInt($(this).next().text())
            if(parseInt(count) <= 8){
            const tableNumber = $('#category-table').data('table')
            const product_id = $(this).data('product')
            const product_name = $(this).prev().text()
            const price = $(this).data('price')
            let result = plus_in_localStorage(count ,product_id, tableNumber, product_name, price)
            $(this).next().text(result)
            }else{
                e.preventDefault()
            }
        })
    }


    //  функция прибавления элемента в localStorage
    function plus_in_localStorage(count ,product_id, tableNumber, product_name, price){
        let tables = localStorage.getItem('tables')
        let parsedTable = JSON.parse(tables)
        if(parsedTable){ // если в локал сторадж есть записи
            if (parsedTable.hasOwnProperty(tableNumber)){ // если есть запись этого стола
                is_Exist = false
                for(let i = 0; i < parsedTable[tableNumber].length; i++){ // проходим по списку заказанных продуктов

                    if(parsedTable[tableNumber][i].product_id === product_id){  // если в списке продуктов есть продукт с таким id
                        parsedTable[tableNumber][i].count += 1
                        localStorage.setItem('tables', JSON.stringify(parsedTable));
                        is_Exist = true
                        return parsedTable[tableNumber][i].count
                        }
                }
                if(!is_Exist){// если в списке продуктов нет продукта с таким id
                    parsedTable[tableNumber].push({'product_id': product_id, count: 1, 'product_name':product_name, 'price':price})
                    localStorage.setItem('tables', JSON.stringify(parsedTable));
                    return 1
                }
            }else{
                // если в localStorage ещё нет стола стаким именем то мы создаём его
                table = {[String(tableNumber)] :[{'product_id': product_id, count: 1, 'product_name':product_name, 'price':price}]}
                localStorage.setItem('tables', JSON.stringify(table));
                return 1
            }
        }else{
                table = {[String(tableNumber)]:[{'product_id': product_id, count: 1, 'product_name':product_name, 'price':price}]}
                localStorage.setItem('tables', JSON.stringify(table));
                return 1
        }
};

    // проверка на существование элемента с таким id в localStorage
    function is_exist_in_localStorage(id_product, data){
        let foundCount = false
        $.each(data, function(index, value){
            if(value.product_id === id_product){
                foundCount = value.count;
                return foundCount;
            }
        })
        return foundCount
    }

    // функция минус
    function clickMinus(){
        $(document).on('click', '.minus_button', function(e){
            e.preventDefault()
            let count = parseInt($(this).prev().text())
            if(count >= 1){
                const tableNumber = $('#category-table').data('table')
                const product_id = $(this).data('product')
                result = minus_in_localStorage(count ,product_id, tableNumber)
                $(this).prev().text(result)
            }

        })
    };
    //  функция прибавления элемента в localStorage
    function minus_in_localStorage(count, product_id, tableNumber){
        let table = localStorage.getItem('tables')
        let parsedTable = JSON.parse(table)
        if(parsedTable){
            if (parsedTable.hasOwnProperty(tableNumber)){
                for (var i = 0; i < parsedTable[tableNumber].length; i++) {
                    if(parsedTable[tableNumber][i].product_id === product_id){
                        parsedTable[tableNumber][i].count -= 1
                        if(parsedTable[tableNumber][i].count === 0){
                            parsedTable[tableNumber].splice(i, 1)
                            localStorage.setItem('tables', JSON.stringify(parsedTable));
                            return 0
                        }
                        localStorage.setItem('tables', JSON.stringify(parsedTable));
                        return parsedTable[tableNumber][i].count
                        break
                    }
                }
            }
        }else{
            return 0
        }
    };
    function add_to_check(){
        $(document).on('click', '#add_pred_check', function(){
            location.reload();
        });
    };


    menu()
    clickPlus()
    clickMinus()
    add_to_check()
});



