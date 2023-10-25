window.addEventListener('load', function(){


// ajax запрос для отображения всех product определёной
// категории при расктытие аккордиона на главной странице,
// добавление элементов в swiper slider
$('.accordion-header').on('click', function(e){
    let category = $(this).attr('data-category')
    let category_block = $(this).next().find('.swiper-wrapper')
    $.ajax({
        url:'/api/v1/product/?category='+ category,
        method: 'get',
        dataType: 'json',
        success: function(response){

            if (response.length > 0) {
              category_block.empty();
                $.each(response, function(index, item) {
                    item_block = `
                        <div class="swiper-slide">
                            <div class="block_inner w-100 row mt-1 mb-1">
                                <div class="col-6 col-sm-6 mx-auto">
                                    <img class="w-100" src="${item.photo}"/>
                                </div>
                                <div class="col-6">${item.title}</div>
                            </div>

                        </div>
                    `




                    category_block.append(item_block)
                })
                var swiper = new Swiper(".mySwiper", {
                      speed: 1200,
                      loop: true,
                      direction: "vertical",
                      pagination: {
                        el: ".swiper-pagination",
                        clickable: true,
                      },
                    });

            }else{
                console.log('нет данных')
            }
        }



    })

})

})
