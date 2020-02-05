document.addEventListener('DOMContentLoaded', () => {
  const TIMEOUT = 5000;

  function showModal(title, message) {
    const modalInfo = document.querySelector('#modal-info');
    const modalTitle = document.querySelector('#modal-title');
    const modalBody = document.querySelector('#modal-body');
    modalTitle.innerHTML = title;
    modalBody.innerHTML = message;
    modalInfo.style.backgroundColor = 'rgba(0, 0, 0, 0.4)';
    modalInfo.style.display = 'block';
  }

  function closeModal() {
    const modalInfo = document.querySelector('#modal-info');
    modalInfo.style.display = 'none';
  }

  document.querySelector('#close-modal-x').onclick = closeModal;

  document.querySelector('#close-modal-button').onclick = closeModal;

  function updatePizzaToppings(pizzaType) {
    const selection = document.querySelector('#' + pizzaType + '-selection');
    const maxToppings = selection.options[selection.selectedIndex].dataset.toppings_count;
    const button = document.querySelector('#' + pizzaType + '-submit');
    var count = 0;
    document.querySelectorAll('.' + pizzaType + '-topping').forEach(function(topping) {
      if (topping.checked) count++;
    });
    if (count == maxToppings) {
      button.disabled = false;
      button.innerHTML = 'Add to cart';
    } else {
      button.disabled = true;
      if (count > maxToppings) {
        button.innerHTML = 'Please remove ' + (count - maxToppings) + ' topping(s).';
      } else {
        button.innerHTML = 'Please add ' + (maxToppings - count) + ' topping(s).';
      }
    }
  }

  function updatePizzaSelection(pizzaType) {
    const spanToppingsCount = document.querySelector('#' + pizzaType + '-toppings-count');
    const selection = document.querySelector('#' + pizzaType + '-selection');
    const toppingsCount = selection.options[selection.selectedIndex].dataset.toppings_count;
    const price = selection.options[selection.selectedIndex].dataset.price;
    const spanPrice = document.querySelector('#' + pizzaType + '-price');
    if (toppingsCount > 0) {
      spanToppingsCount.innerHTML = 'Please select ' + toppingsCount + ' topping(s).';
      document.querySelectorAll('.' + pizzaType + '-topping').forEach(function(topping) {
        topping.disabled = false;
      })
    } else {
      spanToppingsCount.innerHTML = 'Cheese without toppings.';
      document.querySelectorAll('.' + pizzaType + '-topping').forEach(function(topping) {
        topping.disabled = true;
        topping.checked = false;
      })
    }
    spanPrice.innerHTML = '$' + parseFloat(price).toFixed(2);
    updatePizzaToppings(pizzaType);
  }

  function addPizzaToCart(pizzaType){
    const request = new XMLHttpRequest();
    const selection = document.querySelector('#' + pizzaType + '-selection');
    const menuItemId = selection.options[selection.selectedIndex].value;
    const csrfMiddlewareToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;
    const cart = document.querySelector('#cart-items-count');
    const button = document.querySelector('#' + pizzaType + '-submit');
    let toppingsList = [];
    var abortTimer;
    var oldHTML = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
    button.disabled = true;
    document.querySelectorAll('.' + pizzaType + '-topping').forEach(function(topping) {
      if (topping.checked) toppingsList.push(topping.value);
    });
    request.open('POST', '/add_to_cart/');
    request.onload = () => {
      clearTimeout(abortTimer);
      button.innerHTML = oldHTML;
      button.disabled = false;
      if (request.status == 200) {
        const data = JSON.parse(request.responseText);
        if (data.success) {
          var modalBody = data.message + '<br> * ' + data.item;
          console.log(data);
          cart.innerHTML = data.cart_items_count;
          showModal('Information', modalBody);
        } else {
          console.log(data);
          showModal('Item NOT added to cart!', data.message);
        }
      } else {
        console.log(request);
        let reason = 'Reason: ' + request.status + ' ' + request.statusText;
        showModal('Item NOT added to cart!', reason);
      }
    }
    const data = new FormData();
    data.append('csrfmiddlewaretoken', csrfMiddlewareToken);
    data.append('menu_item_id', menuItemId);
    data.append('toppings_list', toppingsList);
    request.send(data);
    abortTimer = setTimeout( function() {
      request.abort('timeout');
      console.log("timeout");
      button.innerHTML = oldHTML;
      button.disabled = false;
      showModal('Item NOT added to cart!', "Reason: Timeout");
    }, TIMEOUT);
  }

  document.querySelector('#regular-pizza-selection').onchange = () => {
    updatePizzaSelection('regular-pizza');
  }

  document.querySelectorAll('.regular-pizza-topping').forEach(function(topping) {
    topping.onchange = () => {
      updatePizzaToppings('regular-pizza');
    }
  });

  document.querySelector('#regular-pizza-form').onsubmit = () => {
    addPizzaToCart('regular-pizza');
    return false;
  }

  document.querySelector('#sicilian-pizza-selection').onchange = () => {
    updatePizzaSelection('sicilian-pizza');
  }

  document.querySelectorAll('.sicilian-pizza-topping').forEach(function(topping) {
    topping.onchange = () => {
      updatePizzaToppings('sicilian-pizza');
    }
  });

  document.querySelector('#sicilian-pizza-form').onsubmit = () => {
    addPizzaToCart('sicilian-pizza');
    return false;
  }

  function updateSubsSelection() {
    const selection = document.querySelector('#subs-selection');
    var price = selection.options[selection.selectedIndex].dataset.price;
    const spanPrice = document.querySelector('#subs-price');
    price = parseFloat(price);
    document.querySelectorAll('.sub-addition').forEach(function(subAddition) {
      if (subAddition.checked) price += parseFloat(subAddition.dataset.price);
    });
    spanPrice.innerHTML = '$' + parseFloat(price).toFixed(2);
  }

  function addSubToCart(pizzaType){
    const request = new XMLHttpRequest();
    const selection = document.querySelector('#subs-selection');
    const menuItemId = selection.options[selection.selectedIndex].value;
    const csrfMiddlewareToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;
    const cart = document.querySelector('#cart-items-count');
    const button = document.querySelector('#subs-submit');
    let subAdditionsList = [];
    var abortTimer;
    var oldHTML = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
    button.disabled = true;
    document.querySelectorAll('.sub-addition').forEach(function(subAddition) {
      if (subAddition.checked) subAdditionsList.push(subAddition.value);
    });
    request.open('POST', '/add_to_cart/');
    request.onload = () => {
      clearTimeout(abortTimer);
      button.innerHTML = oldHTML;
      button.disabled = false;
      if (request.status == 200) {
        const data = JSON.parse(request.responseText);
        if (data.success) {
          var modalBody = data.message + '<br> * ' + data.item;
          console.log(data);
          cart.innerHTML = data.cart_items_count;
          showModal('Information', modalBody);
        } else {
          console.log(data);
          showModal('Item NOT added to cart!', data.message);
        }
      } else {
        console.log(request);
        let reason = 'Reason: ' + request.status + ' ' + request.statusText;
        showModal('Item NOT added to cart!', reason);
      }
    }
    const data = new FormData();
    data.append('csrfmiddlewaretoken', csrfMiddlewareToken);
    data.append('menu_item_id', menuItemId);
    data.append('sub_additions_list', subAdditionsList);
    request.send(data);
    abortTimer = setTimeout( function() {
      request.abort('timeout');
      console.log("timeout");
      button.innerHTML = oldHTML;
      button.disabled = false;
      showModal('Item NOT added to cart!', "Reason: Timeout");
    }, TIMEOUT);
  }

  document.querySelector('#subs-selection').onchange = updateSubsSelection;

  document.querySelectorAll('.sub-addition').forEach(function(subAddition) {
    subAddition.onchange = updateSubsSelection;
  });

  document.querySelector('#subs-form').onsubmit = () => {
    addSubToCart();
    return false;
  }

  function updateOtherSelection(itemType) {
    const selection = document.querySelector('#' + itemType + '-selection');
    const price = selection.options[selection.selectedIndex].dataset.price;
    const spanPrice = document.querySelector('#' + itemType + '-price');
    spanPrice.innerHTML = '$' + parseFloat(price).toFixed(2);
  }

  function addItemToCart(itemType){
    const request = new XMLHttpRequest();
    const selection = document.querySelector('#' + itemType + '-selection');
    const menuItemId = selection.options[selection.selectedIndex].value;
    const csrfMiddlewareToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;
    const cart = document.querySelector('#cart-items-count');
    const button = document.querySelector('#' + itemType + '-submit');
    var abortTimer;
    var oldHTML = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';
    button.disabled = true;
    request.open('POST', '/add_to_cart/');
    request.onload = () => {
      clearTimeout(abortTimer);
      button.innerHTML = oldHTML;
      button.disabled = false;
      if (request.status == 200) {
        const data = JSON.parse(request.responseText);
        if (data.success) {
          var modalBody = data.message + '<br> * ' + data.item;
          console.log(data);
          cart.innerHTML = data.cart_items_count;
          showModal('Information', modalBody);
        } else {
          console.log(data);
          showModal('Item NOT added to cart!', data.message);
        }
      } else {
        console.log(request);
        let reason = 'Reason: ' + request.status + ' ' + request.statusText;
        showModal('Item NOT added to cart!', reason);
      }
    }
    const data = new FormData();
    data.append('csrfmiddlewaretoken', csrfMiddlewareToken);
    data.append('menu_item_id', menuItemId);
    request.send(data);
    abortTimer = setTimeout( function() {
      request.abort('timeout');
      console.log("timeout");
      button.innerHTML = oldHTML;
      button.disabled = false;
      showModal('Item NOT added to cart!', "Reason: Timeout");
    }, TIMEOUT);
  }

  document.querySelector('#pasta-selection').onchange = () => {
    updateOtherSelection('pasta');
  }

  document.querySelector('#pasta-form').onsubmit = () => {
    addItemToCart('pasta');
    return false;
  }

  document.querySelector('#salad-selection').onchange = () => {
    updateOtherSelection('salad');
  }

  document.querySelector('#salad-form').onsubmit = () => {
    addItemToCart('salad');
    return false;
  }

  document.querySelector('#platter-selection').onchange = () => {
    updateOtherSelection('platter');
  }

  document.querySelector('#platter-form').onsubmit = () => {
    addItemToCart('platter');
    return false;
  }

  //document.querySelector('#regular-pizza-selection').selectedIndex = 0;
  updatePizzaSelection('regular-pizza');
  updatePizzaSelection('sicilian-pizza');
  updateSubsSelection();
  updateOtherSelection('pasta');
  updateOtherSelection('salad');
  updateOtherSelection('platter');
});
