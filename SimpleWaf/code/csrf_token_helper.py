from bs4 import BeautifulSoup


def inject_token_to_html(html: str, xsrf_token_tag: str) -> str:
    """
    the function injects a xsrf_token tag into a html from
    (it will inject it to each form in the html code)
    :param html: the html code as str
    :param xsrf_token_tag: the tag to inject as str
    (should be hidden, with a known name, the value should be unpredictable)
    :return: the html with the tag injected as str
    """
    soup = BeautifulSoup(html, "html.parser")

    for form in soup.find_all("form"):
        form.insert(0, BeautifulSoup(xsrf_token_tag, "html.parser").input)

    return str(soup)
