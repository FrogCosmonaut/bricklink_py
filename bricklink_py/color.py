from .utils import BaseResource

from dataclasses import dataclass


@dataclass
class Color:
    color_id: int
    color_name: str
    color_code: str
    color_type: str

    def __post_init__(self):
        self.color_code = self.color_code.upper()

    def __str__(self):
        """String representation of the color."""
        return f"Color {self.color_name} ({self.color_id}) ({self.color_type}) - #{self.color_code}"

    def __repr__(self) -> str:
        """Detailed representation of the color."""
        return (
            f"Color(id={self.color_id}, name={self.color_name}, "
            f"color_type={self.color_type}, color_code={self.color_code})"
        )


class ColorManager(BaseResource):

    def get_color_list(self):
        """Retrieves a list of the colors defined within BrickLink catalog.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = "colors"
        colors = self._request("get", uri)
        return [Color(**c) for c in colors]

    def get_color(self, color_id: int):
        """Retrieves information about a specific color.

        Arguments:
            color_id -- The ID of the color to get.

        Returns:
            requests.Response: The response object returned from the request.
        """
        uri = f"colors/{color_id}"
        color = self._request("get", uri)
        return Color(**color)
