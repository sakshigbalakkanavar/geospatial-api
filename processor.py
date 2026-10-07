import geopandas as gpd
import zipfile
from pathlib import Path


def read_file(file_path):
    file_path = Path(file_path)

    if file_path.suffix == ".kml":
        data = gpd.read_file(file_path)

        if data.crs is None:
            data = data.set_crs("EPSG:4326")

        return data

    if file_path.suffix == ".zip":
        folder = file_path.parent / "extracted"
        folder.mkdir(exist_ok=True)

        with zipfile.ZipFile(file_path) as z:
            z.extractall(folder)

        files = list(folder.rglob("*.shp"))

        if not files:
            raise ValueError("No shapefile found")

        return gpd.read_file(files[0])

    raise ValueError("Only KML and ZIP files are allowed")


def calculate_measurements(gdf):
    if gdf.crs is None:
        raise ValueError("CRS is missing")

    if gdf.crs.is_geographic:
        measured = gdf.to_crs(gdf.estimate_utm_crs())
    else:
        measured = gdf

    result = []

    for i in range(len(gdf)):
        geometry = gdf.geometry.iloc[i]
        measured_geometry = measured.geometry.iloc[i]

        data = {
            "id": i,
            "geometry_type": geometry.geom_type,
            "geometry": geometry.__geo_interface__,
            "properties": {
                key: str(value)
                for key, value in gdf.iloc[i].drop("geometry").items()
            }
        }

        if geometry.geom_type == "Polygon":
            data["area"] = measured_geometry.area
        elif geometry.geom_type == "LineString":
            data["length"] = measured_geometry.length
        else:
            data["measurement"] = None

        result.append(data)

    return result