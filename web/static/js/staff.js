const loader = document.querySelector('.bgDark')
let originalHeaderText = '';



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



refreshData.addEventListener('click', () => {
    refreshData.classList.toggle('transform');
    setTimeout(() => {
        location.reload()
    }, 500)

})
refreshDataBonus.addEventListener('click', () => {
    refreshDataBonus.classList.toggle('transform');
    setTimeout(() => {
        location.reload()
    }, 500)

})

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
                // document.getElementById(`open_modal${name}`).click()
                console.log(name)
                document.getElementById('test').innerHTML = data
                // console.log(name)
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
    let data_bonus = document.getElementById('on_date').value
    let value_bonus = document.getElementById('amount').value
    let name = localStorage.getItem('name')

    if (!data_bonus || !value_bonus) {
        getNotifications('Ошибка! Необходимо заполнить все поля (Дата и сумма)')
        return
    }
    let form = new FormData()
    form.append('staff', name)
    form.append('amount', value_bonus)
    form.append('on_date', data_bonus)
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





























// const tabs = document.querySelectorAll('.tabs_eldenhard.nav-link');
// const tabContents = document.querySelectorAll('.tab-pane');
// console.log(tabs)
// tabs.forEach(tab => {
//     tab.addEventListener('click', () => {
//         tabs.forEach(t => t.classList.remove('active'));
//         tab.classList.add('active');

//         tabContents.forEach(content => content.classList.remove('active'));
//         const targetId = tab.getAttribute('data-bs-target').substr(1);
//         const targetContent = document.getElementById(targetId);
//         targetContent.classList.add('active');
//     });
// });

