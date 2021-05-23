const stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
const client_secret = $('#id_client_secret').text().slice(1, -1);
const stripe = Stripe(stripe_public_key);
const elements = stripe.elements();

const style = {
    base: {
        color: '#000',
        fontFamily: '"Rokkitt", serif',
        fontSmoothing: 'antialised',
        fontSize: '14px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    inavlid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

const card = elements.create('card', {
    style: style
});
card.mount('#card-element');