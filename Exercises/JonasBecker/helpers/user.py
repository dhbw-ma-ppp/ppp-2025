def get_user_input(
    prompt: str = "Enter something: ", type=str, accept: list | None = None
):  # type is some type, returns some type
    while True:
        try:
            user_input = type(input(prompt))

            if isinstance(accept, list):
                if user_input in accept:
                    return user_input
                else:
                    print(f"Invalid input! Please only provide a valid choice.")
                    continue

            return user_input
        except ValueError:
            print(f"Invalid input! Please enter a value of type {type.__name__}.")
