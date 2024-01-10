window.addEventListener('load', function(){
    $('.edit_product').on('click', function(e){
        e.preventDefault()
        let order = $(this).data('orderid')
        let count = $(this).data('count')
        let product_title = $(this).text()
        $('.edit-product').text(product_title)
        $('.product-quantity').text(count)
        $('.close-btn').attr('data-orderid', order)
        let block = document.querySelector('.edit_quality_product')
        block.classList.remove('hide')
    })

    $('.edit-plus').on('click', function(e){
        let count = parseInt($('.product-quantity').text())
        count++
        $('.product-quantity').text(count)
    })

    $('.edit-minus').on('click', function(e){
        let count = parseInt($('.product-quantity').text())
        count--
        if(count > 0){
            $('.product-quantity').text(count)
        }
        else if(count === 0){
            let count = $('.product-quantity').text()
            let orderId = $('.close-btn').data('orderid')
            api_product_plus(orderId, 0)
            let block = document.querySelector('.edit_quality_product')
            block.classList.add('hide')
        }
    })

    $('.close-btn').on('click', function(e){
        let count = $('.product-quantity').text()
        let orderId = $(this).data('orderid')

        api_product_plus(orderId, count)
        let block = document.querySelector('.edit_quality_product')
        block.classList.add('hide')
    })

    function api_product_plus(order, count){
        $.ajax({
            url:'/tables/ajax_edit_product/',
            data: {'order': order, 'count': count},
            method: 'get',
            dataType: 'json',
            success: function(response){
                if(response.success){
                    location.reload()
                }
            }
        })
    }


});


