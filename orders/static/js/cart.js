document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('#cart');
  const dataTag = document.querySelector("input[name='remove_item']");
  document.querySelectorAll('.remove-button').forEach(function(button) {
    button.onclick = function () {
      console.log(this.dataset.cart_item_id);
      dataTag.value = this.dataset.cart_item_id;
      form.submit();
    }
  })
});
