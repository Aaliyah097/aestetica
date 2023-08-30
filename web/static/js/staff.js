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


function getSalaryCurrentEmloyee(value) {
    
    let name = value.getAttribute('data-name-employee')
    // get_salary_by_staff
    $.ajax(
        {
            type: 'get',
            url: `/staff/salary?staff=${name}`,
            async: true,
            success: function (data) {
                console.log(value)
                // document.getElementById(`open_modal${name}`).click()
                document.getElementById('test').innerHTML = data
                document.getElementById('exampleModalLabel').innerHTML = value.getAttribute('data-name-modal')
            },
            error: function (xhr, errmsg, err) {
                notify('Ошибка!', 'Повторите попытку позднее.');
            }
        }
    )
}

function getBonusCurrentEmloyee(value){
    let name = value.getAttribute('data-name-employee')
    // get_salary_by_staff
    $.ajax(
        {
            type: 'get',
            url: `/bonus-by-staff?staff=${name}`,
            async: true,
            success: function (data) {
                console.log(value)
                // document.getElementById(`open_modal${name}`).click()
                document.getElementById('test').innerHTML = data
                document.getElementById('exampleModalLabel').innerHTML = value.getAttribute('data-name-modal')
            },
            error: function (xhr, errmsg, err) {
                notify('Ошибка!', 'Повторите попытку позднее.');
            }
        }
    )
}


const tabs = document.querySelectorAll('.tabs_eldenhard.nav-link');
const tabContents = document.querySelectorAll('.tab-pane');
console.log(tabs)
tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');

        tabContents.forEach(content => content.classList.remove('active'));
        const targetId = tab.getAttribute('data-bs-target').substr(1);
        const targetContent = document.getElementById(targetId);
        targetContent.classList.add('active');
    });
});

