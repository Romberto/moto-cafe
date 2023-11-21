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
                        <div class="swiper-slide d-block mx-auto row">
                            <div>
                                <div class="d-flex flex-wrap row">
                                    <div class="col-12 col-sm-6 col-md-4 col-xxl-3">
                                        <img src="${item.photo}" class="w-75 mb-1 d-block mx-auto"/>
                                    </div>
                                    <div class="d-flex flex-wrap col-12 col-sm-6 col-md-8 col-xxl-9">
                                        <div class="row mb-1 col-12">
                                           <div class="title position-relative col-8 col-sm-12"><b class="text-info">${item.title}</b></div>
                                           <div class="col-4 col-sm-12 position-relative "><span class="times">${item.times} мин</span></div>
                                        </div>
                                       <div class="w-25 col-12">
                                           <p class="mb-1 ms-3 price position-relative d-inline-block">${item.price}</p>
                                       </div>
                                       <div class="mb-1 col-11 description-large">
                                        <p class="description">${item.description}</p>
                                    </div>
                                    </div>
                                    <div class="mb-1 col-11 description-small">
                                        <p class="description">${item.description}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `
                    category_block.append(item_block)
                })


                var swiper = new Swiper(".mySwiper", {
                    direction: "vertical",
                    speed: 1200,
                    loop: true,
                    spaceBetween: 10,
                    pagination: {
                        el: ".swiper-pagination",
                        clickable: true,
                    },
                //    autoHeight: true, // Включение автоматической высоты
                    });

            }else{
                category_block.empty();
                item_block = `
                    <div class="swiper-slide d-block mx-auto row">
                        <h3>Здесь пока пусто.</h3>
                    </div>
                `

                category_block.append(item_block)

            }
        }



    })

})

})
