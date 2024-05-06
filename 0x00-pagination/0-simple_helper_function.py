#!/usr/bin/env python3


def index_range(page, page_size):
    """
    Calculate the start and end index for pagination.

    :param page: int, the current page number (1-indexed)
    :param page_size: int, the number of items per page
    :return: tuple (start_index, end_index)
    """
    start_index = (page - 1) * page_size
    end_index = page * page_size
    return (start_index, end_index)
