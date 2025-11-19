def get_user_input(
    prompt: str = "Enter something: ", type=str
):  # type is some type, returns some type
    while True:
        try:
            user_input = input(prompt)
            return type(user_input)
        except ValueError:
            print(f"Invalid input! Please enter a value of type {type.__name__}.")
