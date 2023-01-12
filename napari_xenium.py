##
import shutil
import numpy as np
import napari
import os
import spatialdata as sd
from spatialdata._core.core_utils import get_default_coordinate_system
from napari_spatialdata import Interactive

# assuming 'spatialdata-sandbox' is available in the parent folder. If not, you can use symplinks

assert os.path.exists("../spatialdata-sandbox")

# SET_LANDMARKS_WITH_NAPARI = False
# SET_LANDMARKS_WITH_NAPARI = True
##
# if SET_LANDMARKS_WITH_NAPARI:
    ##
if False:
    xenium_path = os.path.abspath("../spatialdata-sandbox/xenium/data.zarr")
    visium_path = os.path.abspath("../spatialdata-sandbox/xenium/data_visium.zarr")

    xenium_sdata = sd.SpatialData.read(xenium_path)
    visium_sdata = sd.SpatialData.read(visium_path)

    ##
    merged = sd.SpatialData(
        images={
            "xenium": xenium_sdata.images["morphology_mip"],
            "visium": visium_sdata.images["CytAssist_FFPE_Human_Breast_Cancer"],
        }
    )
    empty = sd.SpatialData()
    interactive = Interactive(sdata=empty, headless=True)
    interactive._add_layers_from_sdata(sdata=merged)
    napari.run()
    ##
    if os.path.isdir("merged.zarr"):
        shutil.rmtree("merged.zarr")
    merged.write("merged.zarr")
    ##
# else:
if True:
    merged = sd.SpatialData.read("merged.zarr")

    ##
    points_reference = merged.points["xenium_landmarks_cyx"].to_pandas().values
    points_moving = merged.points["visium_landmarks_cyx"].to_pandas().values
    from skimage.transform import SimilarityTransform

    model = SimilarityTransform(dimensionality=2)
    model.estimate(points_moving, points_reference)
    transform_matrix = model.params
    print(transform_matrix)
    xy_cs = get_default_coordinate_system(("x", "y"))
    cyx_cs = get_default_coordinate_system(("c", "y", "x"))
    affine = sd.Affine(
        transform_matrix, input_coordinate_system=xy_cs, output_coordinate_system=xy_cs
    )
    # not perfect match but almost, probably because we are forcing an homogenous transformation on data from consecutive
    # slices and with imprecise points
    # assert np.allclose(affine.transform_points(points_moving), points_reference)
    old_visium = sd.get_transform(merged.images["visium"]).to_affine()
    old_xenium = sd.get_transform(merged.images["xenium"]).to_affine()
    ##
    # verbose, this will be simplified in a refactoring of the spatialdata API
    cyx_to_xy = sd.Affine(
        np.array([[0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]]),
        input_coordinate_system=cyx_cs,
        output_coordinate_system=xy_cs,
    )
    xy_to_cyx = sd.Affine(
        np.array([[0, 0, 0], [0, 1, 0], [1, 0, 0], [0, 0, 1]]),
        input_coordinate_system=xy_cs,
        output_coordinate_system=cyx_cs,
    )
    composed = sd.Sequence(
        [old_visium, cyx_to_xy, affine, xy_to_cyx, old_xenium.inverse()],
        input_coordinate_system=cyx_cs,
        output_coordinate_system=cyx_cs,
    )
    # debug stuff
    # with np.printoptions(precision=2, suppress=True, threshold=5):
        # print(affine.affine)
        # print(composed.to_affine().affine)
        # print(sd.get_transform(merged.images["visium"]).to_affine().affine)
        # print(sd.get_transform(merged.images["xenium"]).to_affine().affine)
        # sd.get_transform(merged.points["visium_landmarks_cyx"]).to_affine().affine
        # sd.get_transform(merged.points["xenium_landmarks_cyx"]).to_affine().affine
    ##
    sd.set_transform(merged.images["visium"], composed)
    empty = sd.SpatialData()
    interactive = Interactive(sdata=empty, headless=True)
    interactive._add_layers_from_sdata(sdata=merged)
    napari.run()
    ##
