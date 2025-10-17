def test_function(func, *, params=None, kwargs=None, expected):
    params = params or ()
    kwargs = kwargs or {}

    try:
        result = func(*params, **kwargs)
        if result == expected:
            print(
                f"✅ Test succeeded: {func.__name__}(*{params}, **{kwargs}) == {expected}"
            )
        else:
            print(
                f"❌ Test failed: {func.__name__}(*{params}, **{kwargs}) == {result}, expected: {expected}"
            )
    except Exception as e:
        print(
            f"❌ Test failed: {func.__name__}(*{params}, **{kwargs}) threw Error: {e}"
        )
