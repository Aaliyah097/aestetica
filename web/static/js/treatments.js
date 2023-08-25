document.getElementById('form_data').addEventListener('submit', function(event) {
    event.preventDefault()
    getSalary($(this))

})

function getSalary(form){
    $.ajax(
        {
            type: 'get',
            url: `${form.attr('action')}?${form.serialize()}`,
            async: true,
            success: function (data) {
                document.getElementById('table_block').innerHTML = data
            },
            error: function (xhr, errmsg, err) {
                getNotifications()
                notify('Ошибка!', 'Повторите попытку позднее.');
            }
        }
    )
}
