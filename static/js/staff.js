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
const loader = new Loader()

document.addEventListener("DOMContentLoaded", () => {
    loader.LoaderOn()
    ChangeService.style = 'display: none;';
    addStaffBlock.style = 'display: none;'
    loader.LoaderOff()
});

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

// showChange.addEventListener('click', () => {
//     showChange.classList.toggle('transform')
//     let element = document.querySelector('.block_watched')
//     if (element.style.display == "none") {
//         element.style.display = "block"; //Показываем элемент
//     }
//     else {
//         element.style = "display : none;"
//     };
// })

select_consumables.addEventListener('change', () => {
    if (select_consumables.value == 'ChangeConsumables') {
        ChangeConsumables.style = 'display: block;'
        ChangeService.style = 'display: none;'
        location.reload()
    } else {
        ChangeConsumables.style = 'display: none;'
        ChangeService.style = 'display: block;'
        searchInServices.focus()
    }
})


select_staff.addEventListener('change', () => {
    if (select_staff.value === 'changeStaffBlock') {
        changeStaffBlock.style = 'display: block;'
        addStaffBlock.style = 'display: none;'
        location.reload()
    } else {
        changeStaffBlock.style = 'display: none;'
        fetch('/roles', {
            method: 'GET',
        }).then(response => {
            return response.json()
        })
            .then(res => {
                for (let role of res) {
                    let option = document.createElement('option')
                    option.value = role.name
                    option.text = role.name
                    allRoleInCompany.appendChild(option)
                }
            }).catch((error) => {
                console.error(error)
            })
        addStaffBlock.style = 'display: block;'

        // searchInServices.focus()
    }
})
function saveNewStaff() {
    const form = document.getElementById('addStaffForm');
    const formData = new FormData(form);

    fetch('/staff/create', {
        method: 'POST',
        body: formData,
    })
        .then(response => {
            if (response.ok) {
                getNotifications('Успешно! Сотрудник создан!', 'alert-success')
                // Обработка успешного ответа, например, перенаправление на другую страницу
            } else {
                // Обработка ошибки
                getNotifications('Ошибка! Сотрудник не создан!', 'alert-danger')
                console.error('Произошла ошибка при отправке данных.');
            }
        })
        .catch(error => {
            console.error('Произошла ошибка:', error);
        });
}
// showChange.addEventListener('click', ())

function getSalaryCurrentEmloyee(value) {
    let name = value.getAttribute('data-name-employee')
    let name_modal = value.getAttribute('data-name-modal')
    document.getElementById('archiveData').innerHTML = "";
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

async function deleteCurrentEmloyee(value) {
    let res = confirm(`Вы уверены что хотите удалить \nсотрудника - ${value}`, "")
    if (res) {
        await fetch(`/staff/delete?staff=${value}`, {
            method: 'POST',
        })
            .then(res => {
                getNotifications('Успешно! Сотрудник удален!', 'alert-success')
            })
            .catch((err) => {
                getNotifications('Ошибка! Сотрудник не удален!', 'alert-danger')
            })
        await setTimeout(() => location.reload(), 1000)

    }

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
                document.getElementById('archiveData').innerHTML = "";
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

async function getArchiveDataForPerson(value) {

    let name = value.getAttribute('data-name-employee')
    let name_modal = value.getAttribute('data-name-modal')
    let role = value.getAttribute('data-role-employee')
    let data

    let url = `/payouts?staff=${name}`
    if(role == 'Продажник') url = `/traffic?staff=${name}`

    await fetch(url)
        .then(response => { return response.json() })
        .then(res => {
            data = res


            document.getElementById('test').innerHTML = ""; // Очистим содержимое
            document.getElementById('archiveData').innerHTML = "";
            document.getElementById('archiveData').innerHTML = `<p>Сотрудник: ${name}</p>`;

            // Создаем контейнер для таблицы с margin-top: 2%
            const tableContainer = document.createElement("div");
            tableContainer.style.marginTop = "2%";
            tableContainer.appendChild(createDataTable(data, name, role));

            document.getElementById('archiveData').appendChild(tableContainer);

            document.querySelector('.save-button').style = 'display: block';
            document.getElementById('exampleModalLabel').innerHTML = name_modal;
            document.querySelector('.name_staff').innerText = "";
            document.querySelector('.btn.btn-success.save-button').style = 'display: none;'
        });
}

function createDataTable(data, name, role) {
    const section = document.createElement('section');
    const buttonAdd = document.createElement('button');
    const buttonSave = document.createElement('button');
    
    buttonAdd.classList.add('btn', 'btn-dark');
    buttonAdd.innerText = 'Добавить';
    buttonAdd.style.marginTop = '2%'
    buttonSave.classList.add('btn', 'btn-success');
    buttonSave.style.display = 'none'; // Изначально скрываем кнопку сохранения
    buttonSave.innerText = 'Сохранить';
    buttonSave.style.marginTop = '2%'
    const tableContainer = document.createElement('div');
    tableContainer.style.maxHeight = '50vh';
    tableContainer.style.overflow = 'auto';

    const table = document.createElement("table");
    table.classList.add('table', 'table-bordered');
    table.border = "1";

    // Создать заголовок таблицы
    const thead = document.createElement("thead");
    const headerRow = document.createElement("tr");
    headerRow.classList.add('sticks')
    headerRow.innerHTML = "<th>Сумма</th><th>Дата</th><th>Имя</th><th>Роль</th><th>Действия</th>";
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Создать тело таблицы и добавить данные
    const tbody = document.createElement("tbody");
    data.forEach((item) => {
        const row = document.createElement("tr");
        row.innerHTML = `<td>${item.amount}</td>
        <td>${item?.on_date.split('-').reverse().join(".")}</td>
        <td>${item.staff.name}</td>
        <td>${item.staff.role.name}</td>
        <td>
            <button data-idx='${item.id}' data-role='${role}' class="btn btn-danger" onclick=deleteRowArchive(this)>Удалить</button>
        </td>`;
        tbody.appendChild(row);
    });

    table.appendChild(tbody);
    tableContainer.appendChild(table);
    section.appendChild(tableContainer);
    section.appendChild(buttonAdd);
    section.appendChild(buttonSave);
    
    let newRowAdded = false; // Флаг, который указывает, была ли уже добавлена новая строка

    buttonAdd.addEventListener('click', () => {
        if (!newRowAdded) {
            addNewRow(table, data, name, role);
            buttonAdd.style.display = 'none';
            buttonSave.style.display = 'block';
            newRowAdded = true;
        }
    });
    
    buttonSave.addEventListener('click', () => {
        saveNewRow(table, name, role);
        buttonAdd.style.display = 'block';
        buttonSave.style.display = 'none';
        newRowAdded = false;
    });

    return section;
}

function addNewRow(table, data, name, role) {

    const tbody = table.querySelector('tbody');
    const newRow = document.createElement('tr');
    if(role == 'Продажник_оклад') role = 'Продажник'
    newRow.innerHTML = `
        <td style="position: relative"><input type='text' style="width: 100%"></td>
        <td style="position: relative"><input type='date' style="width: 100%"></td>
        <td>${name}</td>
        <td>${role}</td>
    `;

    tbody.appendChild(newRow);
}

function saveNewRow(table, name, role) {

    const tbody = table.querySelector('tbody');
    const newRow = tbody.lastElementChild;
    
    // Получите значения из инпутов в новой строке
    const amount = newRow.querySelector('input[type="text"]').value;
    const date = newRow.querySelector('input[type="date"]').value;
    const staff_name = newRow.cells[2].innerText
    console.log(staff_name)
    let data = {
        'amount': amount,
        'on_date': date,
        'staff': staff_name
    }
    let url = `/payouts/create`
    if(role == 'Продажник') url = `/traffic/create`
     

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    }).then(res => {
        if(res.status == 200){
            getNotifications('Успешно! Данные добавлены', 'alert-success')
            $('#exampleModal').modal('hide')
        }else {
            getNotifications('Ошибка! Вы не заполнили все поля!')
            $('#exampleModal').modal('hide') 
        }

    }).catch((err) => {
        console.error(err)
    })
  
}
// Удаление записи по окладу
function deleteRowArchive(value) {
    let idx = value.getAttribute('data-idx')
    let role = value.getAttribute('data-role')
    let url = `/payouts/${idx}/delete`
    if(role == 'Продажник') url = `/traffic/${idx}/delete`
     let res = confirm('Вы уверены, что хотите удалить запись?', "")

    if (res) {
        fetch(url, {
            method: 'POST'
        })
        .then(res => {
            if (res.ok) {
                getNotifications('Успешно! Данные о выплате удалены', 'alert-success');
                // Находим строку (родительский элемент кнопки "Удалить") и удаляем ее из DOM
                // Находим первый РОДИТЕЛЬ строки
                const row = document.querySelector(`button[data-idx="${idx}"]`).closest('tr');
                row.remove();
            } else {
                getNotifications('Ошибка! Данные не удалены', 'alert-danger');
            }
        })
        .catch((error) => {
            console.error(error);
            getNotifications('Ошибка! Данные не удалены', 'alert-danger');
        });
    }
}




// function Reclamation(el){
//     console.log(el)
// }


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
    let comment = document.getElementById('comment').value
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
    form.append('comment', comment)
    fetch(`/bonus`, {
        method: 'POST',
        body: form
    }).then(response => {
        if (response.status !== 200) {
            response.text().then(function (text) {
                getNotifications('Ошибка присваивания надбавки. ' + text)
            })
        }
        $('#exampleModal').modal('hide')
        getNotifications('Успешно! Премия создана', 'alert-success')
        // setTimeout(() => { location.reload() }, 1500)
    }).catch((error) => {

    })
}



function CreateSalaryCurrentEmployee() {

    const activeFilialTab = document.querySelector('.nav-link.active');

    if (activeFilialTab) {
        // Получение текущей активной вкладки внутри филиала
        const tabId = activeFilialTab.getAttribute('href').substr(1); // Убираем символ #

        if (tabId) {
            const activeTab = document.getElementById(tabId);

            if (activeTab) {
                // Получение ID активного департамента
                const activeDepartmentTab = activeTab.querySelector('.nav-link.active');
                const departmentId = activeDepartmentTab.getAttribute('data-current-id');

                if (departmentId) {
                    // departmentId содержит ID активного департамента в активном филиале
                    console.log("ID активного департамента:", departmentId);

                    // Найти элементы для ввода percent, limit и fix внутри активного департамента таба
                    const percentInputs = activeTab.querySelectorAll(`#${activeDepartmentTab.getAttribute('href').substr(1)} .salary_input.grid-percent`);
                    const limitInputs = activeTab.querySelectorAll(`#${activeDepartmentTab.getAttribute('href').substr(1)} .salary_input.grid-limit`);
                    const fixValueInput = activeTab.querySelector(`#${activeDepartmentTab.getAttribute('href').substr(1)} .salary_input.fix-value`);
                    const gridIdElements = activeTab.querySelectorAll(`#${activeDepartmentTab.getAttribute('href').substr(1)} .grid-id`);

                    // Получить значение для fix
                    const fix = parseFloat(fixValueInput.value);

                    // Создать массив данных для percent, limit и id
                    const gridData = [];

                    percentInputs.forEach((percentInput, index) => {
                        const percent = parseFloat(percentInput.value);
                        const limit = parseFloat(limitInputs[index].value);
                        const id = gridIdElements[index].getAttribute('data-grid-id');

                        gridData.push({
                            id: Number(id),
                            percent,
                            limit
                        });
                    });

                    // Создать структуру данных
                    const data = {
                        fix: fix,
                        grid: gridData
                    };
                    fetch(`/salary/update/${departmentId}`, {
                        method: 'POST',
                        headers: {
                            "Content-Type": 'application/json'
                        },
                        body: JSON.stringify(data),
                    }).then(response => {
                        loader.LoaderOff()
                        if (response.status == 200) {
                            getNotifications('Успешно! Данные изменены', 'alert-success');
                        }
                    }).catch((error) => {
                        loader.LoaderOff()
                    });
                    // console.log("Данные fix и grid:", data, departmentId);
                }
            }
        }
    }

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
    const OldCost = document.getElementById(`costInput_${pk}`).value;
    const NewCost = document.getElementById(`costInputNew_${pk}`).value;
    let formData = new FormData()
    formData.append('cost', OldCost)
    formData.append('cost_new', NewCost)

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


function ChangeIsSubmit(checkbox) {

    const cargoCode = checkbox.getAttribute('data-cargo-code');
    const cargoName = checkbox.getAttribute('data-cargo-name');
    const newValue = checkbox.checked; // Получаем новое значение чекбокса

    fetch('/services/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            code: cargoCode,
            name: cargoName,
            is_submit: newValue,
        }),
    })
        .then(response => {
            if (response.ok) {
                checkbox.parentNode.classList.add('success')
                setTimeout(() => checkbox.parentNode.classList.remove('success'), 850)

                console.log(`Значение чекбокса для ${cargoName} (код ${cargoCode}) успешно обновлено.`);
            } else {
                checkbox.parentNode.classList.add('error')
                setTimeout(() => checkbox.parentNode.classList.remove('error'), 850)
                console.error(`Ошибка при обновлении значения чекбокса для ${cargoName} (код ${cargoCode}).`);
            }
        })
        .catch((error) => {
            console.error(`Произошла ошибка: ${error}`);
        });
}


function ChangeDiscountByStaff(checkbox) {

    const Name = checkbox.getAttribute('data-name-staff');
    const isNew = checkbox.getAttribute('data-name-isNew')
    const newValue = checkbox.checked; // Получаем новое значение чекбокса
   
    fetch(`/staff/update?staff=${Name}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            is_new: Boolean(isNew),
            reduce_discount: newValue,
        }),
    })
        .then(response => {
            if (response.ok) {
                checkbox.parentNode.classList.add('success')
                setTimeout(() => checkbox.parentNode.classList.remove('success'), 850)

                console.log(`Значение чекбокса для ${cargoName} (код ${cargoCode}) успешно обновлено.`);
            } else {
                checkbox.parentNode.classList.add('error')
                setTimeout(() => checkbox.parentNode.classList.remove('error'), 850)
                console.error(`Ошибка при обновлении значения чекбокса для ${cargoName} (код ${cargoCode}).`);
            }
        })
        .catch((error) => {
            console.error(`Произошла ошибка: ${error}`);
        });
}



function searchServices(input) {
    const searchText = input.value.toLowerCase(); // Получаем текст из поля ввода и приводим его к нижнему регистру
    const table = document.getElementById("TableService"); // Получаем таблицу

    // Получаем все строки таблицы, начиная со второй строки (первая строка содержит заголовки)
    const rows = table.querySelectorAll("tr:not(:first-child)");

    // Перебираем строки таблицы и скрываем те, которые не содержат текст поиска
    rows.forEach((row) => {
        const nameCell = row.querySelector("td:nth-child(2)"); // Получаем ячейку с наименованием
        const name = nameCell.textContent.toLowerCase(); // Получаем текст из ячейки и приводим его к нижнему регистру

        // Проверяем, содержит ли текст ячейки текст поиска
        if (name.includes(searchText)) {
            row.style.display = ""; // Если содержит, то строка видима
        } else {
            row.style.display = "none"; // Если не содержит, то строка скрыта
        }
    });
}
function saveNameOperation(event, element) {
    if (event.key === 'Enter') {
        console.log()
        const cargoCode = element.getAttribute('data-cargo-code');
        const cargoIsSubmit = element.getAttribute('data-cargo-issubmit') == 'True' ? true : false

        fetch('/services/update', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: event.target.value,
                code: cargoCode,
                is_submit: cargoIsSubmit
            }),
        })
            .then(response => {
                if (response.ok) {
                    element.classList.add('success')
                    setTimeout(() => element.classList.remove('success'), 850)
                    getNotifications('Успешно! Наименование изменено', 'alert-success')

                } else {
                    element.classList.add('error')
                    setTimeout(() => element.classList.remove('error'), 850)
                    getNotifications('Ошибка! Не удалось изменить имя услуги', 'alert-danger')

                }
            })
            .catch((error) => {
                console.error(`Произошла ошибка: ${error}`);
            });

    }
}





