document.addEventListener('DOMContentLoaded', () => {
  function filterStatus() {
    const selection = document.querySelector('#filter-status');
    const filter = selection.options[selection.selectedIndex].value;
    document.querySelectorAll('.order-list-row').forEach(function(row){
      if (filter == 'all') {
        row.classList.remove('hide');
      } else if (filter == 'completed') {
        if (row.dataset.completed == "True") row.classList.remove('hide'); else row.classList.add('hide');
      } else if (filter == 'pending') {
        if (row.dataset.completed == "False") row.classList.remove('hide'); else row.classList.add('hide');
      }
    });
  }

  document.querySelector('#filter-status').onchange = filterStatus;

  document.querySelectorAll('.mark-button').forEach(function(button) {
    button.onclick = function() {
      const selection = document.querySelector('#filter-status');
      const filter = selection.options[selection.selectedIndex].value;
      const order_id = button.dataset.order_id;
      const action = button.dataset.action;
      const form = document.querySelector('#admin-form');
      document.querySelector("input[name='order_id']").value = order_id;
      document.querySelector("input[name='action']").value = action;
      document.querySelector("input[name='filter']").value = filter;
      form.submit();
    };
  })

  filterStatus();
})
