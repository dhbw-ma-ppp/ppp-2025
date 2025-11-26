def test_function(func, *, params=None, kwargs=None, expected) -> bool:
    """Tests a function.

    Tests a function by trying to execute the inline function and feeding it params (passed as params to self).
    Then it will compare it to the expected value and make a print message.

    Parameters
    ----------
    func: Callable[..., Any] # Could be included through internal typing library
        Callback function to test

    params: Optional[Union[list[Any], tuple[Any, ...]]] # Could be included through internal typing library
        optional keyword argument for position params listing to pass to callback function

    kwargs: Optional[dict[str, Any]] = None,  # Could be included through internal typing library
        optional keyword argument for keyword arguments to pass to callback function

    expected: Any # Could be included through internal typing library
        keyword argument for expected value to compare to

    Returns
    -------
    bool
        True for success, False for fail
    """

    params = params or ()
    kwargs = kwargs or {}

    try:
        result = func(*params, **kwargs)
        if result == expected:
            print(
                f"✅ Test succeeded: {func.__name__}(*{params}, **{kwargs}) == {expected}"
            )
            return True
        else:
            print(
                f"❌ Test failed: {func.__name__}(*{params}, **{kwargs}) == {result}, expected: {expected}"
            )
            return False
    except Exception as e:
        print(
            f"❌ Test failed: {func.__name__}(*{params}, **{kwargs}) threw Error: {e}"
        )
        return False
