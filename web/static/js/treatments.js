(function () {
    document.querySelector('.table').style = 'display: none'
}())

const generate_button = document.getElementById('generate_button')
const date_start = document.getElementById('date_start')
const filial = document.getElementById('filial')
const table = document.querySelector('.table')
const month_ZP = document.querySelector('#month_ZP')


generate_button.addEventListener('click', () => {
    event.preventDefault()
    if (!date_start.value) {
        getNotifications()
        return
    }
    let current_month = new Date(date_start.value).toLocaleString('default', { month: 'long' })
    month_ZP.innerHTML = `Зарплатная ведомость за ${current_month.charAt(0).toUpperCase() + current_month.slice(1)}`
    document.querySelector('.no_data').style = 'display: none'
    month_ZP.style = 'margin: 0'
    table.style = 'display: block;'
})


