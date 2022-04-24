from requests_html import HTMLSession


class Package:
    def __init__(self, package_name, latest_version, description):
        self.package_name = package_name
        self.latest_version = latest_version
        self.description = description


def search_package(package_name):
    try:
        if package_name is None:
            return []

        s = HTMLSession()
        r = s.get(f'https://pub.dev/packages?q={package_name}')
        packages_items = r.html.find('.packages-item')
        items = []

        for package in packages_items:
            name = package.find('.packages-title', first=True).text
            items.append(Package(package_name=name, latest_version='',
                                 description=''))
        return items

    except Exception as e:
        print(e)
