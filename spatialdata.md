<img src='https://github.com/giovp/spatialdata-sandbox/raw/main/graphics/overview.png'/>

# What is SpatialData?
SpatialData is a library for reading, writing, representing in memory and preprocessing arbitrary multi-sample, multi-omics spatial datasets from any technology.

## File format
For reading and writing we rely on the [Zarr implementation](https://github.com/ome/ome-zarr-py) of the [NGFF specificaiton](https://github.com/ome/ngff). In the future the will read and write fully-valid NGFF objects, but at the momemnt this is not possible becase we need features not yet suppoted by NGFF (but on the roadmap and we are contributing on them). So SpatialData is also a data format, very close to the Zarr implementation of NGFF.

## Spatial elements
We represent arbitrary complex spatial datasets as combinations of simpler *spatial elements* that can be combined, added, removed and aligned to each others. We use standard objects to represent the elements.

*Note: we will probably unify `Shapes`, `Polygons` and `Points` into a single type, but for practical and performance reasons we are keeping them separate for the moment.*
- **2D/3D images, 2D/3D labels**: [`SpatialImage`](https://github.com/spatial-image/spatial-image) with is a valid [`xarray.DataArray`](https://docs.xarray.dev/en/stable/generated/xarray.DataArray.html) object. Lazy-loading is enabled by [`dask`](https://www.dask.org/) which is used under the hood.
- **Mutliscale 2D/3D images/labels**: [`MultiscaleSpatialImage`](https://github.com/spatial-image/multiscale-spatial-image) which is a [`datatree.DataTree`](https://github.com/xarray-contrib/datatree) of [`xarray.DataArray`](https://docs.xarray.dev/en/stable/generated/xarray.DataArray.html).
- **Shapes (=Circles and Squares)**: [`AnnData`](https://anndata.readthedocs.io/en/latest/) object, with coordinates in `.obsm['spatial']`. 
- **Polygons**: a collection of [`shapely.Polygon`](https://shapely.readthedocs.io/en/latest/reference/shapely.Polygon.html#shapely.Polygon) and [`shapely.MultiPolygon`](https://shapely.readthedocs.io/en/latest/reference/shapely.MultiPolygon.html#shapely.MultiPolygon), stored in a [`geopandas.GeoDataFrame`](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.html).
- **Points**: [`pyarrow.Table`](https://arrow.apache.org/docs/python/generated/pyarrow.Table.html).
- **Table**: [`AnnData`](https://anndata.readthedocs.io/en/latest/) object. This object does not contain spatial information but just annotation (for instance gene expression).

Labels, Shapes (=Circles and Squares) and Polygons represent 2D regions (or 3D volumes). We refer to these elements as *Regions*. Regions can be annotated with a Table.

Example. A Visium dataset is a collection of 
 One (or more) images
 A Circles object (="Visium spots")
 A Table annotating the Circles with gene expression, cell-type, etc.

## Transformations and coordinate systems
Spatial elements can be aligned to one or multiple coordinate systems. Coordinate systems can specify physical units. This information is defined by the NGFF specification and it is saved to Zarr.

Examples. 
1) It is possible to align spatial gene expression to images, or multiple samples/slides together. 
2) Handdrawn/histologyical annotations can be saved to the datases.
3) 2D and 3D data can be combined with arbitrary affine transformations.
4) New spatial elements can be added to an existing dataset at any time and the alignment can be modified separately from the data.

## Further reading, docs
More information on our [technical design doc](https://github.com/scverse/spatialdata/blob/main/docs/design_doc.md).

The documentation is not yet hosted online and it is work in progress, but you can see a first draft with
```
cd docs
make html
# open _build/html/index.html
```

# Installation

Please clone and do an editable install the ["temp/spacehack2022" branch](https://github.com/scverse/spatialdata/tree/temp/spacehack2022) of the "spatialdata" repo:
```bash=
# Python 3.9 and 3.10 are supported

# optional: create a clean conda env
conda create -n spacehack python=3.10
conda activate spacehack

git clone --single-branch --branch temp/spacehack2022 https://github.com/scverse/spatialdata
cd spatialdata
pip install -e ".[all]"
```

You need additional packages for reading standard datasets and for visualization.
```bash=
# for reading xenium data
cd ..
git clone https://github.com/scverse/spatialdata-io
cd spatialdata-io
pip install -e .

# for visualization with napari
cd ..
git clone --single-branch --branch spatialdata https://github.com/scverse/napari-spatialdata
cd napari-spatialdata
pip install -e .

# repo with example codes with various datasets
cd ..
git clone https://github.com/giovp/spatialdata-sandbox
```

Additional dependecies:
```
# this dependency will be removed in the future
mamba install -c ome bioformats2raw 
pip install dask_image
```

# Hello world
Example on how to:
1) Download a MIBI-TOF dataset (small, good to start with) from `spatialdata-sandbox`
2) Convert it to `.zarr` and load it in memory with `SpatialData`
3) Visualize it with `napari-spatialdata`

## 1. Download
```bash
cd spatialdata-sandbox/mibitof
# this will create a folder called data/
python download.py
```

## 2. Read in memory
```bash
# this will convert the data into a folder called data.zarr/
python to_zarr.py
```

Read it in memory and print it.
```pythonconsole
>>> import spatialdata as sd
... sdata = sd.SpatialData.read('data.zarr')
... print(sdata)

SpatialData object with:
├── Images
│     ├── 'point16': SpatialImage[cyx] (3, 1024, 1024)
│     ├── 'point23': SpatialImage[cyx] (3, 1024, 1024)
│     └── 'point8': SpatialImage[cyx] (3, 1024, 1024)
├── Labels
│     ├── 'point16': SpatialImage[yx] (1024, 1024)
│     ├── 'point23': SpatialImage[yx] (1024, 1024)
│     └── 'point8': SpatialImage[yx] (1024, 1024)
└── Table
      └── 'AnnData object with n_obs × n_vars = 3309 × 36
    obs: 'row_num', 'point', 'cell_id', 'X1', 'center_rowcoord', 'center_colcoord', 'cell_size', 'category', 'donor', 'Cluster', 'batch', 'library_id'
    uns: 'spatialdata_attrs'
    obsm: 'X_scanorama', 'X_umap', 'spatial'': AnnData (3309, 36)
```

## 3. Visualize

```
from napari_spatialdata import Interactive
Interactive(sdata)
```

# Limitations:
- The on-disk format will slightly change before the release, for instance at the moment we are using `.parquet` files to save points and we switch to `.zarr`.
- The spatial elements will be unified and simplified.
- In particular, at the moment Regions can't contain annotations (annotatoins need to be in a separate Table that annotates them). This will probably be relaxed. Points (that are not Regions) cannot be annotated by Tables, in that case the annotation lives inside the points.
- `napari-spatialdata` will be refactored in the next weeks and will replace the `squidpy` napari viewer. The transition is not complete and some functionalities are not supported or optimized (e.g. slow to plot annotations on points).

# Soon-to-be-delivered features
- There will be importer from the main commercial spatial companies and converter to R
- Squidpy will use `SpatialData` as a backend and so it will be possible to analyze data with it.
- Useful processing functions like rasterization, spatial cropping/subsetting, aggregation signals from multiple layers (e.g. counting single-molecule points inside regions) will be available.
- Napari at the moment doesn't cover the use case of data in a remote machine used for developmemnt (typical Jupyter setup). We are in contact with the Vitessce devs to explore the visualization with it. 
- In the future it will be possible to combine and visualize spatial elements from the local storage and from cloud storage containers (partial support already in ome-zarr-py and napari).
