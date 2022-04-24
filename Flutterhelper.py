from requests_html import HTMLSession


class Package:
    def __init__(self, package_name, description, more_title='', latest_version='', clipboard_text=''):
        self.package_name = package_name
        self.description = description
        self.more_title = more_title
        self.url = f'https://pub.dev/packages/{package_name}'
        self.latest_version = latest_version
        self.clipboard_text = clipboard_text


def search_package(package_name):
    try:
        if package_name is None:
            return []

        s = HTMLSession()
        r = s.get(f'https://pub.dev/packages?q={package_name}')
        packages_items = r.html.find('.packages-item')
        items = []

        for package in packages_items:
            name = package.find('.packages-title a', first=True).text
            descriptions = package.find('.packages-metadata-block', first=True)
            likes = safe_text_parse('.packages-score-like', package)
            pub_points = safe_text_parse('.packages-score-health', package)
            popularity = safe_text_parse('.packages-score-popularity', package)

            likes_text = f' {likes} 👍' if likes else ''
            pub_points_text = f' {pub_points} 💪' if pub_points else ''
            popularity_text = f' {popularity} 🔥' if popularity else ''

            latest_version = safe_text_parse('.packages-metadata-block a:nth-child(1)', package)

            # more_title = likes_text + pub_points_text + popularity_text

            items.append(Package(
                package_name=name,
                clipboard_text=get_clipboard(name, latest_version), description=descriptions,
                more_title='',
            ))
        return items

    except Exception as e:
        print(e)


def get_clipboard(name, latest_version):
    if latest_version:
        return f"{name}:^{latest_version}"
    else:
        return f"{name}:"


def safe_text_parse(selector, s):
    try:
        return s.find(selector, first=True).text
    except Exception:
        return ''
