menu = [{'title': 'Home', 'url_name': 'home'},
        {'title': 'All blogs', 'url_name': 'all_blogs'},
        {'title': 'All bloggers', 'url_name': 'all_blogers'}, ]


class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        return context
