DIRECTORY_SELECTORS = {
    # xpath
    'entry': ".//div[@class='cXEmmc B9Uude hFgAsc F6rDnb H7du2 JN6y2c qrLqp']/div",
    'page_num': ".//div[@class='aEb7Ed']",
    'thread_title': ".//span[@class='o1DPKc']",
    'post_url': ".//a[@class='ZLl54']/@href",
    'post_author': ".//span[@class='z0zUgf']",
    'post_date': ".//div[@class='tRlaM']",
    'post_subject': ".//div[@class='WzoK']",
}

THREAD_SELECTORS = {
    'hidden_email': ".//a[@data-email-masked='']",
    'post_author': ".//h3[@class='s1f8zd']",
    'post_date': ".//span[@class='zX2W9c']"
}