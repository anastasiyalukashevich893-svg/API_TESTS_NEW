class SoftAssert:
    def __init__(self):
        self.errors = []

    def assert_equal(self, actual, expected, message):
        if actual != expected:
            self.errors.append(f"{message}: expected '{expected}', got '{actual}'")

    def assert_all(self):
        if self.errors:
            raise AssertionError("Soft assertions failed:\n  - " + "\n  - ".join(self.errors))
