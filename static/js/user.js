document.addEventListener('DOMContentLoaded', function() {
    const orderHistory = document.querySelector('.order-history');
    const loadMoreButton = document.getElementById('load-more-orders');
    let loadingMore = false;

    window.addEventListener('scroll', function() {
        const scrollHeight = orderHistory.scrollHeight;
        const scrollTop = window.scrollY;
        const clientHeight = window.innerHeight;
        const scrollBottom = scrollHeight - scrollTop - clientHeight;

        if (scrollBottom < 200 && !loadingMore) {
            loadingMore = true;
            const offset = orderHistory.childElementCount;
            fetchMoreOrders(offset);
        }
    });

    function fetchMoreOrders(offset) {
        fetch(`/load-more-orders?offset=${offset}`)
            .then(response => response.json())
            .then(data => {
                data.forEach(order => {
                    const orderElement = document.createElement('div');
                    orderElement.classList.add('order');
                    orderElement.innerHTML = `
                        <p>${order.product_name}</p>
                        <p>Quantité : ${order.quantity}</p>
                        <p>Prix : ${order.price}</p>
                        <p>Date : ${order.order_date}</p>
                    `;
                    orderHistory.appendChild(orderElement);
                });

                loadingMore = false;
                if (data.length < 8) {
                    loadMoreButton.style.display = 'none';
                }
            })
            .catch(error => {
                console.error('Error fetching more orders:', error);
                loadingMore = false;
            });
    }
});


// opacity order component
document.addEventListener("DOMContentLoaded", function() {
    const orders = document.querySelectorAll('.order');

    orders.forEach((order, index) => {
        const opacity = 1 - (index * 0.1);
        order.style.opacity = opacity;
    });
});