const loader = document.querySelector('.bgDark')
let originalHeaderText = '';

$(document).ready(function () {
    $('.js-select2').select2({
        placeholder: "Выберите услугу",
        maximumSelectionLength: 2,
        language: "ru"
    });

});

function makeInput(th) {
    originalHeaderText = th.textContent.trim();
    th.style = 'position: relative'
    th.innerHTML = `<input type="text" id="filterInput" placeholder="Поиск" value="" oninput="filterTable()" style="position: absolute; padding-left: 5%; border: none; outline: none; text-decoration: none; top: 0; left: 0; height: 100%; width: 100%; ">`;
    const input = document.getElementById('filterInput');
    input.focus();

    // Добавляем обработчик события клика на весь документ
    document.addEventListener('click', function (event) {
        if (!th.contains(event.target)) { // Если клик был не внутри th
            th.textContent = originalHeaderText;
            th.style = 'background: #E2E3E5'
        }
    });
}

function filterTable() {
    const input = document.getElementById('filterInput');
    const filterValue = input.value.toUpperCase();
    const table = document.querySelector('.table');
    const rows = table.getElementsByTagName('tr');

    for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const td = row.getElementsByTagName('td')[0];
        if (td) {
            const cellText = td.textContent || td.innerText;
            if (cellText.toUpperCase().indexOf(filterValue) > -1) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        }
    }
}


function transfromThisElement(id) {
    console.log(id)
    let element = document.getElementById(id)
    element.classList.toggle('transform');
    setTimeout(() => {
        location.reload()
    }, 500)
}

showChange.addEventListener('click', () => {
    showChange.classList.toggle('transform')
    let element = document.querySelector('.block_watched')
    if (element.style.display == "none") {
        element.style.display = "block"; //Показываем элемент
    }
    else {
        element.style = "display : none;"
    };
})

// showChange.addEventListener('click', ())

function getSalaryCurrentEmloyee(value) {
    let name = value.getAttribute('data-name-employee')
    let name_modal = value.getAttribute('data-name-modal')
    // get_salary_by_staff
    $.ajax(
        {
            type: 'get',
            url: `/staff/salary?staff=${name}`,
            async: true,
            success: function (data) {
                document.getElementById('test').innerHTML = data
                document.querySelector('.save-button').style = 'display: block'
                document.getElementById('exampleModalLabel').innerHTML = name_modal
                document.querySelector('.name_staff').innerText = ""
            },
            error: function (xhr, errmsg, err) {
                notify('Ошибка!', 'Повторите попытку позднее.');
            }
        }
    )
}


function getBonusCurrentEmloyee(value) {
    let name = value.getAttribute('data-name-employee')
    let name_modal = value.getAttribute('data-name-modal')

    if (localStorage.getItem('name')) {
        localStorage.clear()
    }
    localStorage.setItem('name', name)
    $.ajax(
        {
            type: 'get',
            url: `/bonus-by-staff?staff=${name}`,
            async: true,
            success: function (data) {
                console.log(value)
                document.querySelector('.name_staff').innerHTML = 'Сотрудник: ' + localStorage.getItem('name')

                document.querySelector('.save-button').style = 'display: none'
                document.getElementById('test').innerHTML = data
                // console.log(localStorage.getItem('name'))
                document.getElementById('exampleModalLabel').innerHTML = name_modal
            },
            error: function (xhr, errmsg, err) {
                notify('Ошибка!', 'Повторите попытку позднее.');
            }
        }
    )
}

function deleteRow(value) {
    let table = document.querySelector('.table-bonus')
    let id_row = value.getAttribute('data-delete-bonus')
    let row = document.getElementById(id_row)
    fetch(`/bonus/${id_row}/delete/`, {
        method: 'POST'
    }).then(response => {
        if (table && row) {
            table.removeChild(row)
        }
    }).catch(error => {
        notify('Ошибка!', 'Повторите попытку позднее.');
    })
}

function createBonus(value) {
    // console.log(bonuses)
    // getNotifications('Успешно');
    event.preventDefault()
    let data_bonus = document.getElementById('date_begin').value
    let data_bonus_end = document.getElementById('date_end').value
    let value_bonus = document.getElementById('amount').value
    let name = localStorage.getItem('name')

    if (!data_bonus || !value_bonus) {
        getNotifications('Ошибка! Необходимо заполнить все поля (Дата и сумма)')
        return
    }
    let form = new FormData()
    form.append('staff', name)
    form.append('amount', value_bonus)
    form.append('date_begin', data_bonus)
    form.append('date_end', data_bonus_end)
    fetch(`/bonus`, {
        method: 'POST',
        body: form
    }).then(response => {
        if (response.status != 200) {
            getNotifications('Ошибка создания премии. Повторите попытку позже! Или проверьте не создана ли уже премия на Вашу дату.')
            return
        }
        $('#exampleModal').modal('hide')
        getNotifications('Успешно! Премия создана', 'alert-success')
        setTimeout(() => { location.reload() }, 1500)
    }).catch(error => {

    })
}



function CreateSalaryCurrentEmployee() {
    loader.style = 'display: block'
    console.log(loader)
    setTimeout(() => {
        // Получение элементов для текущей вкладки
        const tabContent = document.querySelector('.tab-pane.active');
        const fixValueInput = tabContent.querySelector('.fix-value');
        const percentInputs = tabContent.querySelectorAll('.grid-percent');
        const limitInputs = tabContent.querySelectorAll('.grid-limit');
        const gridIds = tabContent.querySelectorAll('.grid-id');
        const tabCurrentId = tabContent.querySelector('.salary_id').innerText

        // Получение значений из полей и вывод в консоль
        const fixValue = fixValueInput.value;

        const gridData = [];

        percentInputs.forEach((percentInput, index) => {
            const percent = percentInput.value;
            const limit = limitInputs[index].value;
            const id = gridIds[index].textContent; // Получение текстового содержимого элемента
            gridData.push({
                id: Number(id),
                percent: parseFloat(percent),
                limit: parseFloat(limit)
            });
        });

        const data = {
            'fix': parseFloat(fixValue),
            'grid': gridData
        };

        fetch(`/salary/update/${tabCurrentId}`, {
            method: 'POST',
            headers: {

                "Content-Type": 'application/json'
            },
            body: JSON.stringify(data),
        }).then(response => {
            loader.style = 'display: none'
            if (response.status == 200) {
                getNotifications('Успешно! Данные изменены', 'alert-success')
            }

        }).catch((error) => {
            loader.style = 'display: none'

        })
    }, 1000)

}

document.getElementById('saveConsumables').addEventListener('submit', function (e) {
    e.preventDefault();
    const form = e.target;

    const formData = new FormData(form);
    // if(formData.get('staff') == 'null'){
    //     formData.set('staff', null)
    // }
    fetch('/consumables/create', {
        method: 'POST',
        body: formData,
    })
        .then(response => {
            console.log(response)
            if (response.status == 200) {
                getNotifications(`Успешно! Данные по услуге сохранены`, 'alert-success')
                document.getElementById('costPriceAddSebe').value = ""
                setTimeout(() => {
                    location.reload()
                }, 1000)


            } else {
                getNotifications('Ошибка! Проверьте введенные данные или попроуйте позже', 'alert-danger')
            }
        })
        .catch(error => {
            console.error('Произошла ошибка:', error);
        });
});

function handleEditClick(pk) {

    const newValue = document.getElementById(`costInput_${pk}`).value;
    let formData = new FormData()
    formData.append('cost', newValue)

    fetch(`/consumables/${pk}/update`, {
        method: 'POST',
        body: formData
    }).then(response => {
        getNotifications('Успешно! Данные обновлены.', 'alert-success')
    }).catch(error => {
        getNotifications('Ошибка! Данные не обновлены.', 'alert-danger')
    })
    // ChangeCostMaterials(serviceCode, technicianName, newValue, pk);
}

function deleteThisRow(id) {
    fetch(`/consumables/${id}/delete`, {
        method: 'POST',
    }).then(response => {
        location.reload()
        // getNotifications('Успешно! Данные удалены.', 'alert-success')
    }).catch(error => {
        // getNotifications('Ошибка! Данные не удалены.', 'alert-danger')
    })
}










