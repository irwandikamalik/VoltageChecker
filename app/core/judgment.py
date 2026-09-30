class Judgment:

    def check_voltage(
        self,
        voltage,
        lower,
        upper
    ):

        return lower <= voltage <= upper


    def check_current(
        self,
        current,
        lower,
        upper
    ):

        return lower <= current <= upper


    def check(
        self,
        voltage,
        current,
        voltage_lower,
        voltage_upper,
        current_lower,
        current_upper
    ):

        voltage_ok = self.check_voltage(
            voltage,
            voltage_lower,
            voltage_upper
        )

        current_ok = self.check_current(
            current,
            current_lower,
            current_upper
        )

        if voltage_ok and current_ok:

            return "OK"

        return "NG"