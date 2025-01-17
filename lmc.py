import readline  # Import readline to handle command history

class LittleManComputer:
    def __init__(self, memory_size=500):
        self.memory = [0] * memory_size  # Initialize memory with zeros
        self.accumulator = 0  # Accumulator to hold results of operations
        self.program_counter = 0  # Program Counter (PC) for instruction tracking

    def input_memory(self, address, value):
        """Manually input a value into a specific memory address."""
        if 0 <= address < len(self.memory):
            self.memory[address] = value
            print(f"-> Block[{address}]: {value}")
        else:
            print(f"Error: Address {address} is out of bounds!")

    def display_memory(self):
        """Display all non-zero memory addresses and their values."""
        print(f"[ACC]: {self.accumulator}")
        print(f"[IDX]: {self.program_counter}")
        print("Memory Address Space:")
        for address in range(len(self.memory)):
            value = self.memory[address]
            if value != 0:
                print(f"[{address}]: {value}")

    def display_help(self):
        print("Little Man Computer Interactive Simulator")
        print("  <address>: <value>  - Manually input value into memory")
        print("  show                - Show address space and value/instruction")
        print("  exit                - Exit the simulator")
        print("LCM Instructions:")
        print("  LDM #n         - ACC <- n")
        print("  LDD <address>  - ACC <- content(address)")
        print("  LDI <address>  - ACC <- content(content(address))")
        print("  LDX <address>  - ACC <- content(address+IX)")
        print("  LDR #n         - IX <- n")
        print("  LDR ACC        - IX <- ACC")
        print("  MOV <register> - IX <- content(ACC)")
        print("  STO <address>  - address <- content(ACC)")
        print("  END            - Return control to OS")
        print("  IN, CMP             - Input and comparison instructions")

    def lmc_ldm(self, instruction):
        operand = instruction.split()[1]
        if operand.startswith("#"):  # Immediate addressing
            self.accumulator = int(operand[1:])
            print(f"-> ACC = {self.accumulator}")
        else:
            print("Invalid instruction!")

    def lmc_ldd(self, instruction):
        parts = instruction.split()

        if len(parts) < 2:  # Check if operand is missing
            print("Error: Missing operand in LDD instruction!")
            return

        operand = parts[1]  # Safe to access now

        if operand.startswith("#"):  # Immediate addressing not allowed
            print("Invalid instruction for LDD: Immediate addressing not allowed!")
        else:
            try:
                address = int(operand)
                if 0 <= address < len(self.memory):  # Ensure the address is valid
                    if self.memory[address] != 0:
                        self.accumulator = self.memory[address]
                    else:
                        self.input_memory(address, 0)  # Set default if needed
                        print("Invalid instruction: Address has no value!")
                    print(f"-> ACC = {self.accumulator}")
                else:
                    print(f"Error: Address {address} out of bounds!")
            except ValueError:
                print(f"Error: Invalid operand '{operand}' for LDD instruction!")


    def lmc_ldi(self, instruction):
        parts = instruction.split()

        if len(parts) < 2:  # Check if operand is missing
            print("Error: Missing operand in LDI instruction!")
            return

        operand = parts[1]  # Safe to access now

        if operand.startswith("#"):  # Immediate addressing not allowed
            print("Invalid instruction for LDI: Immediate addressing not allowed!")
        else:
            try:
                address = int(operand)
                if 0 <= address < len(self.memory):  # Ensure the address is valid
                    if self.memory[address] != 0:
                        indirect_address = self.memory[address]
                        for indirect_address in range(len(self.memory)):
                            value = self.memory[indirect_address]
                            if value != 0:
                                self.accumulator = self.memory[indirect_address]
                    else:
                        self.input_memory(address, 0)  # Set default if needed
                        print("Invalid instruction: Address has no value!")
                    print(f"-> ACC = {self.accumulator}")
                else:
                    print(f"Error: Address {address} out of bounds!")
            except ValueError:
                print(f"Error: Invalid operand '{operand}' for LDI instruction!")

    def lmc_add(self, instruction):
        """Add the value from memory (direct or immediate) to the accumulator."""
        parts = instruction.split()
        operand = parts[1]
        if operand.startswith("#"):  # Immediate addressing
            self.accumulator += int(operand[1:])
        else:  # Direct addressing
            address = int(operand)
            self.accumulator += self.memory[address]
        print(f"-> ACC = {self.accumulator}")

    def lmc_sub(self, instruction):
        """Subtract the value from memory (direct or immediate) from the accumulator."""
        operand = instruction.split()[1]
        if operand.startswith("#"):  # Immediate addressing
            self.accumulator -= int(operand[1:])
        else:  # Direct addressing
            address = int(operand)
            self.accumulator -= self.memory[address]
        print(f"-> ACC = {self.accumulator}")

    def lmc_inc(self, instruction):
        """Increment the accumulator."""
        self.accumulator += 1
        print(f"-> ACC = {self.accumulator}")

    def lmc_dec(self, instruction):
        """Decrement the accumulator."""
        self.accumulator -= 1
        print(f"-> ACC = {self.accumulator}")

    def lmc_in(self, instruction):
        """Input a value and store it in the accumulator."""
        print("-> IN: Input value required to store in ACC")
        self.accumulator = int(input("Enter a value: "))
        print(f"-> ACC = {self.accumulator}")

    def lmc_cmp(self, instruction):
        """Compare the accumulator with a value from memory (direct or immediate)."""
        operand = instruction.split()[1]
        if operand.startswith("#"):  # Immediate addressing
            value = int(operand[1:])
        else:  # Direct addressing
            address = int(operand)
            value = self.memory[address]

        if self.accumulator == value:
            print("-> ACC equals the value")
        elif self.accumulator < value:
            print("-> ACC is less than the value")
        else:
            print("-> ACC is greater than the value")

    def run_instruction(self, instruction):
        """Execute the LMC instruction using the instruction-to-function map."""
        instruction_map = {
            "LDM": self.lmc_ldm,
            "LDD": self.lmc_ldd,
            "LDI": self.lmc_ldi,
            #"LDX": self.lmc_ldx,
            #"LDR": self.lmc_ldr,
            #"MOV": self.lmc_mov,
            #"STO": self.lmc_sto,
            #"END": self.lmc_end,

            "ADD": self.lmc_add,
            "SUB": self.lmc_sub,
            "INC": self.lmc_inc,
            "DEC": self.lmc_dec,
            "IN": self.lmc_in,
            "CMP": self.lmc_cmp,
        }

        # Extract the instruction name (e.g., ADD, SUB, etc.)
        command = instruction.split()[0]

        # Check if the command exists in the instruction map
        if command in instruction_map:
            # Call the corresponding function from the map
            instruction_map[command](instruction)
        else:
            print("Invalid instruction!")

    def input_program(self):
        """Take program input and execute it."""
        print("Enter LMC Instructions (type 'EXIT' to stop):")
        while True:
            instruction = input("$ ").strip().upper()

            if instruction == "EXIT":
                print("Exiting LMC Program.")
                break

            # Run the entered instruction
            self.run_instruction(instruction)


def run_lmc_interactively():
    lmc = LittleManComputer()

    # Enable command history
    history_file = ".lmc_history"  # You can specify a file to store the history
    try:
        readline.read_history_file(history_file)
    except FileNotFoundError:
        pass  # No history file yet, that's fine

    while True:
        try:
            command = input("$ ").strip()

            # Handle empty Enter presses (same as Ctrl+C)
            if command == "":
                continue  # Ignore the empty input and continue the loop

            if command.lower() == "exit":
                print("Exiting the simulator.")
                break

            if command.lower() == "show":
                # Show the non-zero memory addresses and their values
                lmc.display_memory()
                continue

            if command.lower() == "help":
                lmc.display_help()
                continue

            # Handle memory input
            if ':' in command:
                try:
                    address, value = command.split(':')
                    address = int(address.strip())
                    value = value.strip()
                    # Check if the value is an instruction (like IN, CMP, etc.)
                    if value in ['IN', 'CMP'] or value.startswith('CMP'):
                        lmc.input_memory(address, value)
                    else:
                        lmc.input_memory(address, int(value))  # Non-instruction values (numbers)
                except ValueError:
                    print("Error: Please enter valid integers for address and value.")
                continue

            # Otherwise treat it as an instruction and run it
            lmc.run_instruction(command)

            # Save command to history after running it
            #readline.write_history_file(history_file)

        except KeyboardInterrupt:
            print("\n(Ctrl+C) Press 'EXIT' to quit or continue entering commands...")
            continue  # Ignore the exception and continue the loop

if __name__ == "__main__":
    run_lmc_interactively()
