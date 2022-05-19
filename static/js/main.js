$(document).ready(async function () {
    let checkoutCreate = async (url) =>
            await $.ajax(
                {
                    method: 'GET',
                    url,
                }
            ),
        checkoutCreateV2 = async (csrfToken) =>
            await $.ajax(
                {
                    method: 'POST',
                    headers: {'X-CSRFToken': csrfToken},
                    url: ''
                }
            ),
        retrievePayment = async (pi_secret) =>
            await $.ajax(
                {
                    method: 'GET',
                    data: {pi_secret},
                    url: 'check/'
                }
            ),
        cartOrder = async (csrfToken) =>
            await $.ajax({
                method: 'post',
                headers: {'X-CSRFToken': csrfToken},
                url: '/v2/cart/order/'
            }),
        addItemToCart = async (csrfToken, data) =>
            await $.ajax({
                method: 'post',
                headers: {'X-CSRFToken': csrfToken},
                url: '/v2/cart/add/',
                data
            }),
        removeItemFromCart = async (csrfToken, data) =>
            await $.ajax({
                method: 'post',
                headers: {'X-CSRFToken': csrfToken},
                url: '/v2/cart/remove/',
                data
            });

    let stripePk = $('input[name=stripe_pk]').val();

    // v1
    if ($('#checkoutCreateForm').length) {
        let stripe = Stripe(stripePk);

        $('#checkoutCreateForm').submit(async function (e) {
            e.preventDefault();
            let url = $(this).attr('action'),
                response = await checkoutCreate(url);

            if (response.sessionId) {
                await stripe.redirectToCheckout({sessionId: response.sessionId})
            } else {
                alert(response)
            }
        })
    }

    // v2
    let cartPreview = $('#cart_preview');
    if (cartPreview) {
        cartPreview.click(function () {
            $('#cart').addClass('active');
            cartPreview.removeClass('active')
        })
        $('.cart-close').click(function () {
            $('#cart').removeClass('active')
            cartPreview.addClass('active')
        })
    }


    if ($('#itemList').length) {
        $('.items-list__item a').click(async function (e) {
            e.preventDefault();
            let csrfToken = $('input[name=csrfmiddlewaretoken]').val(),
                itemId = $(this).data('item-id'),
                response = await addItemToCart(csrfToken, {itemId});

            if (response.added) {
                let cartItem = $(`#cartList tbody tr[data-item-id=${response.itemId}]`);
                if (cartItem.length) {
                    let tds = cartItem.find('td');
                    $(tds[1]).text(response.itemQuantity);
                    $(tds[2]).text(response.itemAmount + ' USD');
                } else {
                    $('#cartList tbody').prepend(
                        `
                            <tr data-item-id="${ response.itemId }">
                                <td>${response.itemName}</td>
                                <td>${response.itemQuantity}</td>
                                <td>${response.itemAmount} USD</td>
                                <td><a href="${response.itemDeleteUrl}" class="cart-list__item-delete" data-item-id="${response.itemId}">удалить</a></td>
                            </tr>
                        `
                    )
                }

                $('.cart-title p').text(`(${response.cartAmount} USD)`)
            }
        })
    }

    if ($('#cartList').length) {
        $('.cart-list__item-delete').click(async function (e) {
            e.preventDefault();
            let csrfToken = $('input[name=csrfmiddlewaretoken]').val(),
                itemId = $(this).data('item-id'),
                response = await removeItemFromCart(csrfToken, {itemId});

            if (response.removed) {
                let cartItem = $(`#cartList tbody tr[data-item-id=${response.itemId}]`);
                cartItem.remove()
                $('.cart-title p').text(`(${response.cartAmount} USD)`)
            }
        });

        $('button.cart-order').click(async function (e) {
            e.preventDefault();
            let csrfToken = $('input[name=csrfmiddlewaretoken]').val(),
                response = {};
            try {
                response = await cartOrder(csrfToken);
            } catch (e) {
                response = e;
            }

            if (response.orderCreated) {
                window.location.href = `/v2/order/${response.orderId}`
            } else {
                alert('Ошибка при создании заказа!')
            }
        })
    }

    if ($('#checkoutCreateFormV2').length) {
        let stripe = Stripe(stripePk);

        $('#checkoutCreateFormV2').submit(async function (e) {
            e.preventDefault();
            let csrfToken = $('input[name=csrfmiddlewaretoken]').val(),
                response = await checkoutCreateV2(csrfToken);

            if (response.intentSecret) {
                const options = {
                        clientSecret: response.intentSecret,
                        appearance: {
                            theme: 'night',
                            labels: 'floating'
                        }
                    },
                    elements = stripe.elements(options),
                    paymentElement = elements.create('payment');

                paymentElement.mount('#payment-element');

                setTimeout(
                    () => {
                        $('#submit').css('display', 'inline-block')
                    }, 1000
                )

                $('#payment-form').submit(async function (e) {
                    e.preventDefault();
                    console.log(response.confirmPaymentUrl)

                    const error = await stripe.confirmPayment({
                        elements,
                        confirmParams: {
                            return_url: response.confirmPaymentUrl,
                        },
                    });

                    if (error) {
                        const messageContainer = document.querySelector('#error-message');
                        messageContainer.textContent = error.message;
                    } else {
                        // Your customer will be redirected to your `return_url`. For some payment
                        // methods like iDEAL, your customer will be redirected to an intermediate
                        // site first to authorize the payment, then redirected to the `return_url`.
                    }
                })
            }
        });
    }

    if ($('#status').length) {
        let stripe = Stripe(stripePk),
            clientSecret = new URLSearchParams(window.location.search).get(
                'payment_intent'
            ),
            response = await retrievePayment(clientSecret),
            message = $('#message');
            console.log(response);

            switch (response.status) {
                case 'succeeded':
                    message.text('Success! Payment received.');
                    break;

                case 'processing':
                    message.text("Payment processing. We'll update you when payment is received.");
                    break;

                case 'requires_payment_method':
                    message.text('Payment failed. Please try another payment method.');
                    break;

                default:
                    message.text('Something went wrong.');
                    break;
            }
            setTimeout(() => {
                window.location.href = '/v2/item/list/'
            }, 3000)
    }

})

