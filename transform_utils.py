#
# def local_to_physical_coordinates(element: SpatialElement, coordinate_system_name: str, coordinates: np.ndarray) -> np.ndarray:
#     """Convert local coordinates to physical coordinates.
#
#     Parameters
#     ----------
#     element
#         The spatial element.
#     coordinate_system_name
#         The name of the coordinate system.
#     coordinates
#         The coordinates to convert.
#
#     Returns
#     -------
#     The physical coordinates.
#     """
#     if coordinate_system_name not in element.coords:
#         raise ValueError(f"Coordinate system {coordinate_system_name} not found.")
#     if coordinates.shape[1] != len(element.dims):
#         raise ValueError(
#             f"Coordinates must have shape (n, {len(element.dims)}), but shape is {coordinates.shape}."
#         )
#     if coordinates.shape[0] == 0:
#         return coordinates
#     if coordinates.shape[0] == 1:
#         return coordinates + element.coords[coordinate_system_name].values
#     return coordinates + element.coords[coordinate_system_name].values[np.newaxis, :]
#
# def physical_to_local_coordinates(element: SpatialElement, coordinate_system_name: str, coordinates: np.ndarray) -> np.ndarray:
#     """Convert physical coordinates to local coordinates.
#
#     Parameters
#     ----------
#     element
#         The spatial element.
#     coordinate_system_name
#         The name of the coordinate system.
#     coordinates
#         The coordinates to convert.
#
#     Returns
#     -------
#     The local coordinates.
#     """
#     if coordinate_system_name not in element.coords:
#         raise ValueError(f"Coordinate system {coordinate_system_name} not found.")
#     if coordinates.shape[1] != len(element.dims):
#         raise ValueError(
#             f"Coordinates must have shape (n, {len(element.dims)}), but shape is {coordinates.shape}."
#         )
#     if coordinates.shape[0] == 0:
#         return coordinates
#     if coordinates.shape[0] == 1:
#         return coordinates - element.coords[coordinate_system_name].values
#     return coordinates - element.coords[coordinate_system_name].values[np.newaxis, :]
#
# points = sdata.points['transcripts']
# points: pa.Table
#
# circles = sdata.shapes['visium']
# a = physical_to_local_coordinates(circles, 'cyx', np.array([[0, 0]], [[55, 55]]))
# 55um
#
# def pixels_to_micrometers()
