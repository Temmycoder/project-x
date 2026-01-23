const products = [{
  image: 'img/acer.jpg',
  name: 'Acer Nitro V Gaming Laptop | Intel Core i5-13420H Processor',
  // rating: {
  //   stars: 4,
  //   count: 146
  // },
  priceCents: 13000
}, {
  image: 'img/watch.jpg',
  name: 'LAVAREDO Mens Digital Watch',
  // rating: {
  //   stars: 4,
  //   count: 84
  // },
  priceCents: 1850
}, {
  image: 'img/bottle.jpg',
  name: 'Insulated Water Bottle with Straw Lid',
  // rating: {
  //   stars: 3.5,
  //   count: 59
  // },
  priceCents: 1000
}];

let productsHTML = '';
products.forEach((product) => {
  productsHTML += `
  <div class="col-md-4">
    <div class="product-card">
      <div class="product-img">
        <img src="${product.image}" class="img-fluid">
      </div>
      <div class="product-text">
        <p class="card-text">${product.name}
        <h4 class="">$${(product.priceCents / 100).toFixed(2)}</h4></p>
        <div class="buynow">
          <button href="cart.html" class="buy btn btn-dark add-to-cart" data-product-name="${product.name}">Add to cart</button>
        </div>
      </div>
    </div>
  </div>`
});

document.querySelector('.product-grid').innerHTML = productsHTML;

document.querySelectorAll('.add-to-cart')
  .forEach((button) => {
    button.addEventListener('click', () => {
      const productName = button.dataset.productName;

      let matchingItem;

      cart.forEach((item) => {
        if(productName === item.productName){
          matchingItem = item;
        }
      });

      if(matchingItem){
        matchingItem.quantity += 1
      }else{
        cart.push({productName: productName, quantity: 1})
      }
      console.log(cart);
    });
  });