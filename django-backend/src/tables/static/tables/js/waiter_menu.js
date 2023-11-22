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
        orders = localStorage.getItem('orders')
        parseOrders = JSON.parse(orders)
        $.ajax({
            url:'/api/v1/product/?category='+ categoryId,
            method: 'get',
            dataType: 'json',
            success: function(response){
                category_page = '<h1 data-table="tableNumber" id="category-table">Стол №'+tableNumber+'</h1>'
                category_page += '<h3 class="mb-2">'+categoryName+'</h3>'
                category_page += '<div class="menu-block">'
                category_page += '<ul class="menu-list ps-1">'
                category_page += '<button class="btn btn-info mb-3">Добавить к счёту</button>'

                $.each(response, function(index, product){
                    category_page += '<li class="row mb-2">'
                        category_page += '<p class="col-7 mb-1">'+product.title+'</p>'
                        category_page += '<a href="#" type="button" class="plus_button col-2" data-product="'+product.id+'"></a>'

                        check_product = is_exist_in_localStorage(product.id, parseOrders)

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
            let result = plus_in_localStorage(count ,product_id, tableNumber)
            $(this).next().text(result)
            }else{
                e.preventDefault()
            }
        })
    }
    //  функция прибавления элемента в localStorage
    function plus_in_localStorage(count ,product_id, table){
        let items = localStorage.getItem('orders')
        let parsedItems = JSON.parse(items)
        if(parsedItems){
            let is_Exist = true
            for (var i = 0; i < parsedItems.length; i++) {
              if (parsedItems[i].product_id === product_id) {
                parsedItems[i].count += 1;
                localStorage.setItem('orders', JSON.stringify(parsedItems));
                return parsedItems[i].count;
                is_Exist = false
                break
              }
            }
            if(is_Exist){
                item = {'product_id': product_id, 'count': 1}
                parsedItems.push(item)
                localStorage.setItem('orders', JSON.stringify(parsedItems));
                return 1; // Если словарь найден, выходим из цикла
            }
        }else{
            orders = []

            items = {'product_id': product_id, 'count': 1}
            orders.push(items)
            localStorage.setItem('orders', JSON.stringify(orders));
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
                const product_id = $(this).data('product')
                result = minus_in_localStorage(count ,product_id)
                $(this).prev().text(result)
            }

        })
    };
    //  функция прибавления элемента в localStorage
    function minus_in_localStorage(count, product_id){
        let items = localStorage.getItem('orders')
        let parsedItems = JSON.parse(items)
        if(parsedItems){
            for (var i = 0; i < parsedItems.length; i++) {
                if(parsedItems[i].product_id === product_id){
                    parsedItems[i].count -= 1
                    localStorage.setItem('orders', JSON.stringify(parsedItems));
                    return parsedItems[i].count;
                }
            }
        }else{
            console.log('error minus')
        }
    };



    menu()
    clickPlus()
    clickMinus()
});



