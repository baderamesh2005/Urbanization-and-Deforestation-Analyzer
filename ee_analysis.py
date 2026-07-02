import ee


def initialize_earth_engine():
    try:
        ee.Initialize(project="dl-urbanization")
    except Exception:
        ee.Authenticate()
        ee.Initialize(project="dl-urbanization")


def get_city_geometry(city_name):
    cities = {
        "Pune": ee.Geometry.Rectangle([73.70, 18.40, 74.00, 18.65]),
        "Mumbai": ee.Geometry.Rectangle([72.77, 18.89, 72.99, 19.30]),
        "Delhi": ee.Geometry.Rectangle([76.84, 28.40, 77.35, 28.88]),
    }
    return cities[city_name]


def get_city_center(city_name):
    centers = {
        "Pune": [18.5204, 73.8567],
        "Mumbai": [19.0760, 72.8777],
        "Delhi": [28.6139, 77.2090],
    }
    return centers[city_name]


def analyze_city(city_name, old_year, new_year):
    initialize_earth_engine()

    region = get_city_geometry(city_name)

    old_start = f"{old_year}-01-01"
    old_end = f"{old_year}-12-31"
    new_start = f"{new_year}-01-01"
    new_end = f"{new_year}-12-31"

    dw_old = (
        ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1")
        .filterBounds(region)
        .filterDate(old_start, old_end)
        .select("label")
        .mode()
        .clip(region)
    )

    dw_new = (
        ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1")
        .filterBounds(region)
        .filterDate(new_start, new_end)
        .select("label")
        .mode()
        .clip(region)
    )

    s2_new = (
        ee.ImageCollection("COPERNICUS/S2_SR")
        .filterBounds(region)
        .filterDate(new_start, new_end)
        .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        .select(["B4", "B3", "B2"])
        .median()
        .clip(region)
    )

    pixel_area = ee.Image.pixelArea()

    forest_old = dw_old.eq(1).multiply(pixel_area)
    forest_new = dw_new.eq(1).multiply(pixel_area)

    urban_old = dw_old.eq(6).multiply(pixel_area)
    urban_new = dw_new.eq(6).multiply(pixel_area)

    forest_old_area = forest_old.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=region,
        scale=10,
        maxPixels=1e13
    )

    forest_new_area = forest_new.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=region,
        scale=10,
        maxPixels=1e13
    )

    urban_old_area = urban_old.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=region,
        scale=10,
        maxPixels=1e13
    )

    urban_new_area = urban_new.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=region,
        scale=10,
        maxPixels=1e13
    )

    forest_old_sqkm = ee.Number(forest_old_area.get("label")).divide(1e6)
    forest_new_sqkm = ee.Number(forest_new_area.get("label")).divide(1e6)

    urban_old_sqkm = ee.Number(urban_old_area.get("label")).divide(1e6)
    urban_new_sqkm = ee.Number(urban_new_area.get("label")).divide(1e6)

    deforestation_percent = (
        forest_old_sqkm.subtract(forest_new_sqkm)
        .divide(forest_old_sqkm)
        .multiply(100)
    )

    urban_growth_percent = (
        urban_new_sqkm.subtract(urban_old_sqkm)
        .divide(urban_old_sqkm)
        .multiply(100)
    )

    forest_loss = dw_old.eq(1).And(dw_new.neq(1)).selfMask().clip(region)
    urban_gain = dw_new.eq(6).And(dw_old.neq(6)).selfMask().clip(region)

    return {
        "city": city_name,
        "old_year": old_year,
        "new_year": new_year,
        "center": get_city_center(city_name),
        "region": region,
        "s2_new": s2_new,
        "dw_old": dw_old,
        "dw_new": dw_new,
        "forest_loss": forest_loss,
        "urban_gain": urban_gain,
        "forest_old_sqkm": forest_old_sqkm.getInfo(),
        "forest_new_sqkm": forest_new_sqkm.getInfo(),
        "urban_old_sqkm": urban_old_sqkm.getInfo(),
        "urban_new_sqkm": urban_new_sqkm.getInfo(),
        "deforestation_percent": deforestation_percent.getInfo(),
        "urban_growth_percent": urban_growth_percent.getInfo(),
    }