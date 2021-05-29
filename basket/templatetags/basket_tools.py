from django import template

register = template.Library()


@register.filter(name='subtotal_calc')
# Function to calculate the subtotal for the basket and checkout
def subtotal_calc(price, quantity):
    return price * quantity
