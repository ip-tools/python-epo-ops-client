from epo_ops.middlewares.cache.dogpile.helpers import kwarg_range_header_handler


def test_kwarg_range_header_handler():
    assert kwarg_range_header_handler(x=1) == ""
    assert kwarg_range_header_handler(headers={"a": 1}) == ""
    assert kwarg_range_header_handler(headers={"X-OPS-Range": 1}) == (
        "headers.X-OPS-Range=1"
    )
