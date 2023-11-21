window.addEventListener('load', function(){
    $('#open-check').on('click', function(e){
        e.preventDefault();

        let number = $('#open-check').data('table');
        console.log(number)
            $.ajax({
            type: 'POST',
            url: '/tables/create_table/',
            data: {
                csrfmiddlewaretoken: csrf_token, number:number
            },
            dataType: 'json',
            success: function (data) {
                if(data.error){
                    alert('ошибка: ' + data.error);
                }else{
                    alert('счет открыт');
                    location.reload()
                }
            },
            error: function () {
                alert('Произошла ошибка при создании таблицы.');
            }
        });
    });




})