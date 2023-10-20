window.addEventListener('load', function(){

    $('#ajax_delete_product').on('click', function(e){
        e.preventDefault()
        $('.delete_popup').fadeIn()
    })


    $('#popup_no').on('click', function(e){
        e.preventDefault()
        $('.delete_popup').fadeOut()
    })

    $('#ajax_delete_category').on('click', function(e){
        e.preventDefault()
        $('.delete_popup').fadeIn()
    })


})