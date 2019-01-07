# coding=utf-8

import xmltodict
import ogr
import osr
import gdal
import os
from pprint import pprint


def read_gpx_file(file_path):
    """Reads a GPX file containing geocaching points.
    :param str file_path: The full path to the file.
    """
    with open(file_path) as gpx_file:
        gpx_dict = xmltodict.parse(gpx_file.read())
    output = []
    for wpt in gpx_dict['gpx']['wpt']:
        geometry = [wpt.pop('@lat'), wpt.pop('@lon')]
        # If geocache is not on the dict, skip this wpt.
        try:
            geocache = wpt.pop('geocache')
        except KeyError:
            continue
        attributes = {'status': geocache.pop('@status')}
        # Merge the dictionaries.
        attributes.update(wpt)
        attributes.update(geocache)
        # Construct a GeoJSON feature and append to the list.
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": geometry},
            "properties": attributes}
        output.append(feature)
    return output


def get_datasource_information(datasource, print_results=False):
    """Get informations about the first layer in the datasource.
    :param datasource: An OGR datasource.
    :param bool print_results: True to print the results on
      the screen.
    """
    info = {}
    layer = datasource.GetLayerByIndex(0)
    bbox = layer.GetExtent()
    info['bbox'] = dict(xmin=bbox[0], xmax=bbox[1],
                        ymin=bbox[2], ymax=bbox[3])
    srs = layer.GetSpatialRef()
    if srs:
        info['epsg'] = srs.GetAttrValue('authority', 1)
    else:
        info['epsg'] = 'not available'
    info['type'] = ogr.GeometryTypeToName(layer.GetGeomType())
    # Get the attributes names.
    info['attributes'] = []
    layer_definition = layer.GetLayerDefn()
    for index in range(layer_definition.GetFieldCount()):
        info['attributes'].append(
            layer_definition.GetFieldDefn(index).GetName())
    # Print the results.
    if print_results:
        pprint(info)
    return info


def read_ogr_features(layer):
    """Convert OGR features from a layer into dictionaries.
    :param layer: OGR layer.
    """
    features = []
    layer_defn = layer.GetLayerDefn()
    layer.ResetReading()
    type = ogr.GeometryTypeToName(layer.GetGeomType())
    for item in layer:
        attributes = {}
        for index in range(layer_defn.GetFieldCount()):
            field_defn = layer_defn.GetFieldDefn(index)
            key = field_defn.GetName()
            value = item.GetFieldAsString(index)
            attributes[key] = value
        feature = {
            "type": "Feature",
            "geometry": {
                "type": type,
                "coordinates": item.GetGeometryRef().
                    ExportToWkt()},
            "properties": attributes}
        features.append(feature)
    return features


def open_vector_file(file_path):
    """Open the shapefile, get the first layer and returns
    the ogr datasource.
    :param str file_path: The full path to the file.
    :return: The ogr datasource.
    """
    datasource = ogr.Open(file_path)
    # Check if the file was opened.
    if not datasource:
        if not os.path.isfile(file_path):
            message = "Wrong path."
        else:
            message = "File format is invalid."
        raise IOError(
            'Error opening the file {}\n{}'.format(
                file_path, message))
    metadata = get_datasource_information(datasource)
    file_name, file_extension = os.path.splitext(file_path)
    # Check if it's a GPX and read it if so.
    if file_extension in ['.gpx', '.GPX']:
        features = read_gpx_file(file_path)
    # If not, use OGR to get the features.
    else:
        features = read_ogr_features(
            datasource.GetLayerByIndex(0))
    return features, metadata



def create_transform(src_epsg, dst_epsg):
    """Creates an OSR tranformation.
    :param src_epsg: EPSG code for the source geometry.
    :param dst_epsg: EPSG code for the destination geometry.
    :return: osr.CoordinateTransformation
    """
    src_srs = osr.SpatialReference()
    src_srs.ImportFromEPSG(src_epsg)
    dst_srs = osr.SpatialReference()
    dst_srs.ImportFromEPSG(dst_epsg)
    return osr.CoordinateTransformation(src_srs, dst_srs)


def transform_geometries(datasource, src_epsg, dst_epsg):
    """Transform the coordinates of all geometries in
    the first layer.
    """
    # Part 1
    src_srs = osr.SpatialReference()
    src_srs.ImportFromEPSG(src_epsg)
    dst_srs = osr.SpatialReference()
    dst_srs.ImportFromEPSG(dst_epsg)
    transformation = osr.CoordinateTransformation(src_srs, dst_srs)
    layer = datasource.GetLayerByIndex(0)
    # Part 2
    geoms = []
    layer.ResetReading()
    for feature in layer:
        geom = feature.GetGeometryRef().Clone()
        geom.Transform(transformation)
        geoms.append(geom)
    return geoms


def transform_points(points, src_epsg=4326, dst_epsg=3395):
    transform = create_transform(src_epsg, dst_epsg)
    points = transform.TransformPoints(points)
    return points


if __name__ == "__main__":
    gdal.PushErrorHandler('CPLQuietErrorHandler')
    points, metadata = open_vector_file('C:/geopy/examplecode/data/geocaching.shp')
    print points[0]['properties'].keys()
    points, metadata = open_vector_file('C:/geopy/examplecode/data/geocaching.gpx')
    print points[0]['properties'].keys()
