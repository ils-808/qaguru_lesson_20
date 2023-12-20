from selene import browser, have
from allure import step
from utils.api_handler import add_to_cart

def run_browser_with_cookie(cookies):
    browser.open('/')
    browser.driver.add_cookie({'name': 'Nop.customer', 'value': cookies})

def go_to_cart():
    browser.element('.ico-cart').click()

def assert_name_and_qauntity_in_cart(name, quantity):
    with step('go to cart and check product'):
        go_to_cart()
        browser.element('.product-name').should(have.text(name))
        browser.element('.qty-input').should(have.attribute('value').value_containing(quantity))

def test_add_one_book_successfully(api_url):
    item_to_add = '/addproducttocart/catalog/13/1/1'

    resp = add_to_cart(api_url + item_to_add)
    assert resp.status_code == 200
    cookies = resp.cookies.get('Nop.customer')

    run_browser_with_cookie(cookies)
    assert_name_and_qauntity_in_cart('Computing and Internet', '1')

def test_add_four_pc_successfully(api_url):
    item_to_add = '/addproducttocart/details/72/1'
    data = {
        'product_attribute_72_5_18': 53,
        'product_attribute_72_6_19': 54,
        'product_attribute_72_3_20': 57,
        'addtocart_72.EnteredQuantity': 10
    }

    resp = add_to_cart(api_url + item_to_add, data)
    assert resp.status_code == 200
    cookies = resp.cookies.get('Nop.customer')

    run_browser_with_cookie(cookies)
    assert_name_and_qauntity_in_cart('Build your own cheap computer', '10')

def test_add_different_items(api_url):
    book_to_add = '/addproducttocart/catalog/13/1/1'
    laptop_to_add = '/addproducttocart/catalog/31/1/1'

    resp = add_to_cart(api_url + book_to_add)
    assert resp.status_code == 200
    cookies = resp.cookies.get('Nop.customer')
    add_to_cart(api_url + laptop_to_add, cookies={'Nop.customer': cookies})

    run_browser_with_cookie(cookies)

    go_to_cart()
    browser.all('.cart-item-row').should(have.size(2))
