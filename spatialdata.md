
repo: spatialdata, branch napari_fix
repo: spatialdata-sandbox, branch main
repo: spatialdata-io, branch main
repo: napari-spatialdata, branch spatialdata
Luca Marconato: dependencies:

create a conda env
install spatialdata, spatialdata-io and napari-spatialdata with pip install -e .
additional dependecies are needed to run code from the 4 repos above. To install all of them use the following:
pip install black pre-commit tqdm scanpy pyarrow imagecodecs loguru pytest psutil "napari[all]"
mamba install -c ome bioinformats2raw
Luca Marconato: data:

the spatialdata-sandbox contains multiple datasets and for each of them there is a download script download.py. Execute it to download the data. After this, each script to_zarr.py will create the data.zarr file.
you can load the data with
import spatialdata as sd
sdata = sd.SpatialData.read('data.zarr')
print(sdata)
and visualize it with

from napari_spatialdata import Interactive
Interactive(sdata)
Luca Marconato: additional notes:

points at the moment are using pyarrow.Table for the in-memory storage due to performance limitations and are saved within the Zarr hierarchy as .parquet files. The rest is the same: each .parquet file is in a zarr group containing the NGFF coordinate transformations
Luca Marconato: splitting the work:

please refer to the first page of the paper draft to see what's to do (strikeout text is not for the next week but for the future).
pick what you prefer, and please add your name next to the element so that we know who is working on what
for each dataset we have three parts:
1) data download (most of them already done)
2) data EDA (viz with napari and screenshot, plots, any EDA you like)
3) analyses following the description in the Results section of the paper draft. These require custom code implementations like rasterization, aggregation etc (see Functions to write section in the paper draft)

if you write code that can be useful for the others to be reused, please push it yolo on spatialdata-sandbox, announce it here and mark it as implemented in the paper draft Functions to write section

please push notebooks in the spatialdata-notebooks repo, and upload figures/screenshots on these slides here
Kevin Yamauchi: Thanks for the instructions, @Luca Marconato !
