class Loader {
    constructor(loader) {
        this.loader = document.querySelector('.bgDark')
    }
    LoaderOn() {
        this.loader.style = 'display: block'
    }
    LoaderOff() {
        this.loader.style = 'display: none'

    }
}
let all_reclamation = [];
let confirmation = document.getElementById('confiramtion_reclamation');
let newConsumables = {}

document.getElementById('form_data').addEventListener('submit', function (event) {
    event.preventDefault()
    getSalary($(this))

})


function ExportSalary() {
    let table = document.getElementById('DownloadMainTable');
    if (!table) {
        getNotifications('Сформируйте таблицу перед экспортом')
        return
    }
    let loader = new Loader()
    loader.LoaderOn()
    $.ajax(
        {
            type: 'post',
            url: '/salary/export',
            async: true,
            data: JSON.stringify({
                'table': table.outerHTML,
                'date_begin': document.getElementById('date_start').value,
                'date_end': document.getElementById("date_end").value,
                'filial': document.getElementById("filial").value
            }),
            contentType: 'application/json',
            success: function (data) {
                loader.LoaderOff()
            },
            error: function (xhr, errmsg, err) {
                loader.LoaderOff()
                getNotifications('Ошибка получения данных, повторите попытку позже')
            }
        }
    )
}

let changed_consumables

function getSalary(form) {
    document.getElementById('table_block').innerHTML = ""
    let loader = new Loader()
    loader.LoaderOn()
    $.ajax(
        {
            type: 'post',
            url: `${form.attr('action')}?${form.serialize()}`,
            async: true,
            contentType: 'application/json',
            data: JSON.stringify({
                'complaints': all_reclamation,
                changed_consumables
            }),
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

                loader.LoaderOff()

            },
            error: function (xhr, errmsg, err) {
                loader.LoaderOff()
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

sync_button.addEventListener('click', async (event) => {
    event.preventDefault();
    let loader = new Loader();
    loader.LoaderOn();

    try {
        let result = await fetch('/sync/services');
        loader.LoaderOff();

        if (result.status === 200) {
            getNotifications(`Успешно! Данные синхронизированы.`, 'alert-success');
        } else if (result.status === 404) {
            // Обработка 404 ошибки
            getNotifications(`Ошибка! Данные не найдены`, 'alert-danger');
        } else {
            // Обработка других статусов
            getNotifications(`Ошибка! Данные не синхронизированы. Статус: ${result.status}`, 'alert-danger');
        }
    } catch (error) {
        console.error(error, "zzzz");
        loader.LoaderOff();
        getNotifications(`Ошибка! Данные не синхронизированы. ${error}`, 'alert-danger');
    }
});

function Reclamation(el) {
    if (el.checked) {
        el.closest('td').children[1].style.display = 'block';
        all_reclamation.push(el.getAttribute('data-markdown-number'));
    } else {
        el.closest('td').children[1].style.display = 'none';
        const index = all_reclamation.indexOf(el.getAttribute('data-markdown-number'));
        if (index !== -1) {
            all_reclamation.splice(index, 1);
        }
    }
    all_reclamation.length > 0 ? confirmation.style.display = 'block' : confirmation.style.display = 'none';
    console.log(all_reclamation);
}
function getReclamation() {
    confirmation.style.display = 'none'
    generate_button.click()
    all_reclamation = []
}






async function ChangePriceConsumablesCost(el) {
    if (el.key === 'Enter') {
        const prevalue = el.target.dataset.prevalue;
        const consumables = el.target.dataset.consumables;
        const currentValue = el.target.value;

        el.target.style = "background: lightgreen; text-align: center; width: 100% !important; height: 100% !important; position: absolute; top: 0; right: 0; border: none;";

        if (currentValue == 0 || currentValue == "") {
            el.target.style = "background: white; text-align: center; width: 100% !important; height: 100% !important; position: absolute; top: 0; right: 0; border: none;";
        }
              // Оборачиваем весь блок в Promise для использования await
//         // await new Promise(resolve => {
//         //     setTimeout(() => {
//         //         el.target.style = "background: white; text-align: center; width: 100% !important; height: 100% !important; position: absolute; top: 0; right: 0; border: none;";
//         //         resolve(); // Резолвим Promise после завершения setTimeout
//         //     }, 850);
//         // });

        changed_consumables = {
            cost: Number(prevalue),
            cost_new: Number(currentValue)
        };

        newConsumables[consumables] = changed_consumables;

        let notifNewConsumables = document.getElementById('confiramtion_new_consumables');
        notifNewConsumables.style = 'display: block';

        changed_consumables = {};
    }
}

function getTableWithNewCost() {
    changed_consumables = newConsumables
    let notifNewConsumables = document.getElementById('confiramtion_new_consumables');
    notifNewConsumables.style = 'display: none';
    generate_button.click()
}

function closeModal() {
    let notifNewConsumables = document.getElementById('confiramtion_new_consumables');
    notifNewConsumables.style = 'display: none';

    // Обновление стилей и значений в полях
    for (const consumableNumber in newConsumables) {
        const consumable = newConsumables[consumableNumber];
        const inputElement = document.querySelector(`[data-consumables="${consumableNumber}"]`);
        if (inputElement) {
            inputElement.style = "background: white; text-align: center; width: 100% !important; height: 100% !important; position: absolute; top: 0; right: 0; border: none;";
            inputElement.value = consumable.cost; // Установка значения обратно
        }
    }
}


