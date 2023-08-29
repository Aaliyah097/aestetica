document.getElementById('form_data').addEventListener('submit', function (event) {
    event.preventDefault()
    getSalary($(this))

})

function getSalary(form) {

    $.ajax(
        {
            type: 'get',
            url: `${form.attr('action')}?${form.serialize()}`,
            async: true,
            success: function (data) {

                document.querySelector('.nodata').style = 'display: none'
                document.getElementById('table_block').innerHTML = data
                const toggleSpans = document.querySelectorAll('.toggle-span');

                toggleSpans.forEach(span => {
                    span.addEventListener('click', function () {
                        const closestRow = this.closest('tr');
                        const name = this.getAttribute('data-name-employee');
                        const rows = document.querySelectorAll(`[data-name-employee-no-show="${name}"]`);
                        
                        closestRow.classList.toggle('current_doc');
                        closestRow.classList.toggle('z-index2') 
                        rows.forEach(row => {
                            row.classList.toggle('no_show');
                        });
                    });
                });
            },
            error: function (xhr, errmsg, err) {
                notify('Ошибка!', 'Повторите попытку позднее.');
            }
        }
    )
}






