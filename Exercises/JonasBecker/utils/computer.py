from enum import Enum
from .user import get_user_input


class Opcode(Enum):
    ADD: int = 1
    MULTIPLY: int = 2
    INPUT: int = 3
    OUTPUT: int = 4
    JUMP_IF_TRUE: int = 5
    JUMP_IF_FALSE: int = 6
    LESS_THAN: int = 7
    EQUALS: int = 8
    ADJUST_REL_BASE: int = 9
    HALT: int = 99

    @property
    def param_count(self) -> int:
        return {
            Opcode.ADD: 3,
            Opcode.MULTIPLY: 3,
            Opcode.INPUT: 1,
            Opcode.OUTPUT: 1,
            Opcode.JUMP_IF_TRUE: 2,
            Opcode.JUMP_IF_FALSE: 2,
            Opcode.LESS_THAN: 3,
            Opcode.EQUALS: 3,
            Opcode.ADJUST_REL_BASE: 1,
            Opcode.HALT: 0,
        }[self]


def calculate_number_through_memory_list(
    memory_integer_list: list[int],
    inputs: list[int] | None = None,
    input_callback: callable | None = None,
    output_callback: callable | None = None,
    output_since_stacked_callback: callable | None = None,
    output_delta_stacked_callback: callable | None = None,
    unbind_lists: bool = True,
    _opcode_index: int = 0,
    _output: list[int] | None = None,
    _relative_base: int = 0,
) -> list[int]:

    if inputs is None:
        inputs = []
    if _output is None:
        _output = []
    if unbind_lists:
        memory_integer_list = memory_integer_list.copy()
        inputs = inputs.copy()

    last_output_len: int = 0

    # ---------- Infinite memory ----------
    def mem_get(addr: int) -> int:
        if addr < 0:
            raise RuntimeError(f"Negative memory address accessed: {addr}")
        if addr >= len(memory_integer_list):
            memory_integer_list.extend([0] * (addr + 1 - len(memory_integer_list)))
        return memory_integer_list[addr]

    def mem_set(addr: int, value: int) -> None:
        if addr < 0:
            raise RuntimeError(f"Negative memory address written: {addr}")
        if addr >= len(memory_integer_list):
            memory_integer_list.extend([0] * (addr + 1 - len(memory_integer_list)))
        memory_integer_list[addr] = value

    def read_param(n: int, modes: list[int], idx: int) -> int:
        mode: int = modes[n - 1] if n <= len(modes) else 0
        raw: int = mem_get(idx + n)
        if mode == 0:
            return mem_get(raw)
        elif mode == 1:
            return raw
        elif mode == 2:
            return mem_get(_relative_base + raw)
        else:
            raise RuntimeError(f"Unknown mode: {mode}")

    def get_write_addr(n: int, modes: list[int], idx: int) -> int:
        mode: int = modes[n - 1] if n <= len(modes) else 0
        raw: int = mem_get(idx + n)
        if mode == 0:
            return raw
        elif mode == 2:
            return _relative_base + raw
        else:
            raise RuntimeError(f"Invalid write mode: {mode}")

    # ---------- stack callbacks ----------
    def trigger_stack_callbacks():
        nonlocal last_output_len
        if output_since_stacked_callback:
            output_since_stacked_callback(_output)
        if output_delta_stacked_callback:
            output_delta_stacked_callback(_output[last_output_len:])
            last_output_len = len(_output)

    # ---------------------------
    # MAIN EXECUTION LOOP
    # ---------------------------
    while True:
        opcode_raw: int = mem_get(_opcode_index)
        opcode_code: int = opcode_raw % 100

        try:
            actual_opcode: Opcode = Opcode(opcode_code)
        except ValueError:
            raise RuntimeError(f"No valid opcode: {opcode_code}")

        modes: list[int] = [int(d) for d in str(opcode_raw // 100)[::-1]]
        next_ip: int = _opcode_index + 1 + actual_opcode.param_count

        match actual_opcode:

            case Opcode.HALT:
                if _output:
                    trigger_stack_callbacks()
                    return _output
                else:
                    return [mem_get(0)]

            case Opcode.ADD:
                mem_set(
                    get_write_addr(3, modes, _opcode_index),
                    read_param(1, modes, _opcode_index)
                    + read_param(2, modes, _opcode_index),
                )

            case Opcode.MULTIPLY:
                mem_set(
                    get_write_addr(3, modes, _opcode_index),
                    read_param(1, modes, _opcode_index)
                    * read_param(2, modes, _opcode_index),
                )

            case Opcode.INPUT:
                trigger_stack_callbacks()
                val: int
                if inputs:
                    val = inputs.pop(0)
                elif input_callback:
                    val = input_callback()
                else:
                    val = get_user_input("Please enter an integer: ", type=int)
                mem_set(get_write_addr(1, modes, _opcode_index), val)

            case Opcode.OUTPUT:
                val: int = read_param(1, modes, _opcode_index)
                _output.append(val)

                if output_callback:
                    output_callback(val)

            case Opcode.JUMP_IF_TRUE:
                if read_param(1, modes, _opcode_index) != 0:
                    next_ip = read_param(2, modes, _opcode_index)

            case Opcode.JUMP_IF_FALSE:
                if read_param(1, modes, _opcode_index) == 0:
                    next_ip = read_param(2, modes, _opcode_index)

            case Opcode.LESS_THAN:
                mem_set(
                    get_write_addr(3, modes, _opcode_index),
                    (
                        1
                        if read_param(1, modes, _opcode_index)
                        < read_param(2, modes, _opcode_index)
                        else 0
                    ),
                )

            case Opcode.EQUALS:
                mem_set(
                    get_write_addr(3, modes, _opcode_index),
                    (
                        1
                        if read_param(1, modes, _opcode_index)
                        == read_param(2, modes, _opcode_index)
                        else 0
                    ),
                )

            case Opcode.ADJUST_REL_BASE:
                _relative_base += read_param(1, modes, _opcode_index)

        _opcode_index = next_ip


if __name__ == "__main__":

    def failed(operation: str) -> str:
        return f"❌ test for {operation} failed"

    memory_list = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
    assert calculate_number_through_memory_list(memory_list, [8]) == [1], failed(
        "8 == 8"
    )
    assert calculate_number_through_memory_list(memory_list, [9]) == [0], failed(
        "9 == 8"
    )

    memory_list = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
    assert calculate_number_through_memory_list(memory_list, [7]) == [1], failed(
        "7 < 8"
    )
    assert calculate_number_through_memory_list(memory_list, [8]) == [0], failed(
        "8 < 8"
    )

    memory_list = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]
    assert calculate_number_through_memory_list(memory_list, [-5]) == [1], failed(
        "-5 != 0"
    )
    assert calculate_number_through_memory_list(memory_list, [0]) == [0], failed(
        "0 != 0"
    )

    print("✅ All tests passed! :]")
