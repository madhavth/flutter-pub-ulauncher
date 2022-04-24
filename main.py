""" Main Module """

import logging

from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.CopyToClipboardAction import CopyToClipboardAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.event import KeywordQueryEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem

from Flutterhelper import search_package

logger = logging.getLogger(__name__)

FLUTTER_PUB_PROVIDERS = sorted([

])


class QFXExtension(Extension):
    """ Main Extension Class  """

    def __init__(self):
        """ Initializes the extension """
        super(QFXExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        # self.subscribe(ItemEnterEvent, ItemEnterEventListener())

    def search_params(self, query):
        results = search_package(query)
        if len(results) == 0:
            output = f'No packages found by name {query}' if query else 'Enter a package name'
            return RenderResultListAction([
                ExtensionResultItem(
                    icon='images/icon.png',
                    name=output,
                    highlightable=False,
                    on_enter=HideWindowAction()
                )
            ])

        items = []
        for result in results[:20]:
            items.append(
                ExtensionResultItem(
                    icon='images/icon.png',
                    name=result.package_name,
                    on_enter=CopyToClipboardAction(result.package_name)))


# def list_providers(self, query):
#
#     providers = FLUTTER_PUB_PROVIDERS
#     if query:
#         providers = [
#             provider for provider in providers if query.lower() in provider
#         ]
#
#     items = []
#
#     if len(providers) == 0:
#         return RenderResultListAction([
#             ExtensionResultItem(
#                 icon='images/icon.png',
#                 name="No provider found matching your criteria",
#                 highlightable=False,
#                 on_enter=HideWindowAction())
#         ])
#
#     for provider in providers[:20]:
#         items.append(
#             ExtensionSmallResultItem(
#                 icon='images/icon.png',
#                 name=provider.replace("_", " ").title(),
#                 on_enter=ExtensionCustomAction(provider,
#                                                keep_app_open=True)))
#
#     return RenderResultListAction(items)


class KeywordQueryEventListener(EventListener):
    """ Listener that handles the user input """

    def on_event(self, event, extension):
        """ Handles the event """
        return extension.search_params(event.get_argument())


# class ItemEnterEventListener(EventListener):
#     """ Listener that handles the click on an item """
#
#     def on_event(self, event, extension):
#         """ Handles the event """
#         selected_provider = event.get_data()
#
#         items = []
#
#         movies = get_movies(selected_provider)
#
#         for movie in movies:
#             items.append(
#                 ExtensionResultItem(
#                     icon='images/icon.png',
#                     name=movie.movie_name,
#                     highlightable=False,
#                     on_enter=OpenUrlAction(movie.youtube_url),
#                     on_alt_enter=OpenUrlAction(movie.book_url),
#                     description=movie.description,
#                 )
#             )
#
#         return RenderResultListAction(items)


if __name__ == '__main__':
    QFXExtension().run()
