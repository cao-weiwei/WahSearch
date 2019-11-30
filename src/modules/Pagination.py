from urllib.parse import urlencode


class Pagination(object):
    """
    Constructor
    """
    def __init__(self, current_page, total_count, base_url, params, per_page_count=20, max_pager_count=1):
        try:
            # convert str into int, if fails, go to the 1st page
            current_page = int(current_page)
        except Exception as e:
            current_page = 1

        if current_page <= 0:
            current_page = 1
        self.current_page = current_page

        # total numbers of documents
        self.total_count = total_count
        # numbers of document shown on per page
        self.per_page_count = per_page_count
        # calculate max pages
        max_page_num, div = divmod(total_count, per_page_count)
        if div:
            max_page_num += 1
        self.max_page_num = max_page_num
        # 页面上默认显示11个页码（当前页在中间）
        self.max_pager_count = max_pager_count
        self.half_max_pager_count = int((max_pager_count - 1) / 2)
        # URL prefix
        self.base_url = base_url
        # request.GET
        import copy
        params = copy.deepcopy(params)
        get_dict = params.to_dict()
        self.params = get_dict

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_count

    @property
    def end(self):
        return self.current_page * self.per_page_count

    def page_html(self):
        """
        get a list of page url
        :return: page list contains url of first page, previous page and next page
        """
        # store urls of first page, previous page and next page
        page_html_list = []
        # first page url
        self.params['page'] = 1
        # first_page = '<li><a href="%s?%s">首页</a></li>' % (self.base_url, urlencode(self.params))
        first_page = "{}?{}".format(self.base_url, urlencode(self.params))
        page_html_list.append(first_page)

        # previous page url
        self.params["page"] = self.current_page - 1
        if self.params["page"] < 1:
            # previous_page = '<li class="disabled"><a href="%s?%s" aria-label="Previous">上一页</span></a></li>' % (
            # self.base_url, urlencode(self.params))
            previous_page = "{}?{}".format(self.base_url, urlencode(self.params))
        else:
            # previous_page = '<li><a href = "%s?%s" aria-label = "Previous" >上一页</span></a></li>' % (self.base_url,
            # urlencode(self.params))
            previous_page = "{}?{}".format(self.base_url, urlencode(self.params))
        page_html_list.append(previous_page)

        # next page url
        self.params["page"] = self.current_page + 1
        if self.params["page"] > self.max_page_num:
            self.params["page"] = self.current_page
            # next_page = '<li class="disabled"><a href = "%s?%s" aria-label = "Next">下一页</span></a></li >' % (
            # self.base_url, urlencode(self.params))
            next_page = "{}?{}".format(self.base_url, urlencode(self.params))
        else:
            # next_page = '<li><a href = "%s?%s" aria-label = "Next">下一页</span></a></li>' % (self.base_url,
            # urlencode(self.params))
            next_page = "{}?{}".format(self.base_url, urlencode(self.params))
        page_html_list.append(next_page)

        return page_html_list

        # return ''.join(page_html_list)
