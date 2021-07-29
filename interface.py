import os


class Nest:
    """Rhodos Nest fixture interface"""

    def __init__(self):
        """Setup function"""
        self.path = os.path.dirname(__file__)
        failed = os.system("cd " + self.path)
        if failed:
            raise PathError(self.path)

    def reset(self, package_name: str = "") -> None:
        """
        Reset the Rhodos mounted in the nest

        :param package_name: Uniflash package used to execute the reset command (optional)
        :return: None
        """
        if not package_name and self.get_packages():
            package_name = self.get_packages()[0]
        if not self.get_packages():
            raise CommandError("There must be a flash package in the uniflash-packages folder")
        if os.system(f"cd {self.path}/uniflash-packages/{package_name}"):
            raise PathError(f"{self.path}/uniflash-packages/{package_name}")
        command = f"cd {self.path}/uniflash-packages/{package_name} && dslite.bat --config=user_files/configs" \
                  f"/cc1312r1f3.ccxml --post-flash-device-cmd PinReset "
        failed = os.system(command)
        if failed:
            raise CommandError(command)

    def flash(self, package_name: str) -> None:
        """
        Flash the build included in the uniflash package to the rhodos mounted in the nest

        :param package_name: Uniflash package to flash to the sensor
        :return: None
        """
        if os.system(f"cd {self.path}/uniflash-packages/{package_name}"):
            raise PathError(f"{self.path}/uniflash-packages/{package_name}")
        command = f"cd {self.path}/uniflash-packages/{package_name} && dslite"
        failed = os.system(command)
        if failed:
            raise CommandError(command)

    def get_packages(self) -> list:
        """
        Returns the list of Uniflash package names included in the uniflash-packages folder

        :return: list
        """
        return os.listdir(f"{self.path}/uniflash-packages")


class PathError(Exception):
    """
    Error for catching invalid path inputs
    """
    def __init__(self, *args):
        if args:
            self.path = args[0]
        else:
            self.path = None

    def __str__(self):
        if self.path:
            return "The path {0} does not exist".format(self.path)
        else:
            return


class CommandError(Exception):
    """
    Error for failed commands given to the command line
    """
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return "An error occured when running this command: {0}".format(self.message)
        else:
            return "An error occured when running this command"
