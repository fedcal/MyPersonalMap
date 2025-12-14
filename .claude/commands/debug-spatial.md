Help me debug a geospatial/spatial data issue.

I'll help you troubleshoot issues related to:
1. Coordinate validation and format
2. Spatial queries not returning expected results
3. Distance calculations being inaccurate
4. Geocoding issues
5. Spatial index performance problems
6. SRID/projection issues

When you describe the issue, include:
- What you're trying to do
- Expected vs actual behavior
- Relevant code snippet
- Sample coordinates or data

I'll help you:
- Verify coordinate validity (lat: -90 to 90, lon: -180 to 180)
- Check SRID is set to 4326 (WGS84)
- Ensure spatial indexes are being used
- Validate distance calculations
- Debug geocoding API issues
- Optimize spatial queries

Common issues and fixes:
- **Wrong coordinate order**: Longitude comes before latitude in many formats
- **Missing SRID**: Always specify SRID 4326 for GPS coordinates
- **No spatial index**: Add spatial index for performance
- **Wrong distance function**: Use ST_Distance_Sphere for accurate distances
- **Geocoding rate limits**: Nominatim allows 1 request/second
