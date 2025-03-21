in/docs/examples/solar_panel_detection.ipynb

# Solar Panel Detection

This notebook demonstrates how to use the geoai package for solar panel detection using a pre-trained model.

[![image](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/opengeos/geoai/blob/main/docs/examples/solar_panel_detection.ipynb)

## Install package
To use the `geoai-py` package, ensure it is installed in your environment. Uncomment the command below if needed.
"""

# %pip install geoai-py

"""## Import libraries"""

import geoai

"""## Download sample data"""

raster_url = "https://huggingface.co/datasets/giswqs/geospatial/resolve/main/solar_panels_davis_ca.tif"
raster_path = geoai.download_file(raster_url)

geoai.print_raster_info(raster_path)

"""## Visualize data"""

geoai.view_raster(raster_url)

"""## Initialize model"""

detector = geoai.SolarPanelDetector()

"""## Generate masks"""

output_path = "solar_panel_masks.tif"

masks_path = detector.generate_masks(
    raster_path,
    output_path=output_path,
    confidence_threshold=0.4,
    mask_threshold=0.5,
    min_object_area=100,
    overlap=0.25,
    chip_size=(400, 400),
    batch_size=4,
    verbose=False,
)

"""## Visualize masks"""

geoai.view_raster(
    output_path,
    indexes=[2],
    colormap="autumn",
    layer_name="Solar Panels",
    basemap=raster_url,
)

"""## Vectorize masks"""

gdf = geoai.orthogonalize(
    input_path=masks_path, output_path="solar_panel_masks.geojson", epsilon=0.2
)

"""## Visualize initial results"""

geoai.view_vector_interactive(gdf, tiles=raster_url)

"""## Calculate geometric properties"""

gdf = geoai.add_geometric_properties(gdf)
gdf.head()

print(len(gdf))

geoai.view_vector_interactive(gdf, column="elongation", tiles=raster_url)

"""## Filter results"""

gdf_filter = gdf[(gdf["elongation"] < 10) & (gdf["area_m2"] > 5)]
print(len(gdf_filter))

"""## Visualize final results"""

geoai.view_vector_interactive(gdf_filter, column="area_m2", tiles=raster_url)

geoai.view_vector_interactive(
    gdf_filter, style_kwds={"color": "red", "fillOpacity": 0}, tiles=raster_url
)

gdf_filter["area_m2"].hist()

gdf_filter["area_m2"].describe()

gdf_filter["area_m2"].sum()

"""## Save results"""

gdf_filter.to_file("solar_panels.geojson")

"""![image](https://github.com/user-attachments/assets/a38925dc-b840-42b0-a926-326ef99b181c)"""
