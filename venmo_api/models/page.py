class Page(list):

    def __init__(self):
        super().__init__()
        self.method = None
        self.kwargs = {}
        self.current_offset = -1
        self.next_kwargs = None

    def set_method(self, method, kwargs, current_offset=-1, next_kwargs=None):
        """
        set the method and kwargs for paging. current_offset is provided for routes that require offset.
        :param method:
        :param kwargs:
        :param current_offset:
        :param next_kwargs: <dict> [optional] cursor kwargs for the next page, taken from the API's
                            pagination.next link. An empty dict means there is no next page.
        :return:
        """
        self.method = method
        self.kwargs = kwargs
        self.current_offset = current_offset
        self.next_kwargs = next_kwargs
        return self

    def get_next_page(self):
        """
        Get the next page of data. Returns empty Page if none exists
        :return:
        """
        if not self.method:
            return Page()

        # Cursor-paged routes: the API tells us where the next page starts (or that there isn't one)
        if self.next_kwargs is not None:
            if not self.next_kwargs:
                return Page()
            return self.method(**{**self.kwargs, **self.next_kwargs})

        if not self.kwargs or len(self) == 0:
            return Page()

        # use offset or before_id for paging, depending on the route
        if self.current_offset > -1:
            self.kwargs['offset'] = self.current_offset + len(self)
        else:
            self.kwargs['before_id'] = self[-1].id

        return self.method(**self.kwargs)
