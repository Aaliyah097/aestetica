const loader = document.querySelector('.bgDark')
document.getElementById('form_data').addEventListener('submit', function (event) {
    event.preventDefault()
    getSalary($(this))

})

function getSalary(form) {
    document.getElementById('table_block').innerHTML = ""
    loader.style = 'display: block'
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

                      
                        const img = span.querySelector('img');
                        img.classList.toggle('rotaed');
                       
                       

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
              
                    loader.style = 'display: none'
            
   

            },
            error: function (xhr, errmsg, err) {
                loader.style = 'display: none'
                getNotifications('Ошибка получения данных, повторите попытку позже')
            }
        }
    )
}






function fnExcelReport() {
    var table = document.getElementById('DownloadMainTable')
    // const ws = XLSX.utils.table_to_sheet(data);
    // const wb = XLSX.utils.book_new();
    // XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
    // XLSX.writeFile(wb, 'Зарплатная таблица.xlsx')
    const ws = XLSX.utils.table_to_sheet(table);

    // Создайте книгу Excel и добавьте в нее лист
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Sheet1');
    
    // Создайте ArrayBuffer для хранения данных
    const buf = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });
    
    // Создайте Blob из ArrayBuffer
    const blob = new Blob([buf], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    
    // Создайте ссылку для скачивания
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'exported_table.xlsx';
    document.body.appendChild(a);
    
    // Симулируйте клик по ссылке для скачивания
    a.click();
    
    // Удалите временные элементы
    document.body.removeChild(a);
  }



