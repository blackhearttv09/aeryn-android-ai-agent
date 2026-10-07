# Android companion scaffold

This directory contains the foundation for the Android companion app used by Aeryn.

## Expected purpose

- foreground service for lifecycle and boot recovery
- Accessibility Service integration point
- permission handling and device state checks
- virtual mouse / pointer control layer integration
- Android bridge between Python runtime and device control APIs

## Notes

The actual production implementation should be expanded into a full Android Studio project with:

- `app/src/main/AndroidManifest.xml`
- Kotlin service and activity classes
- permission declarations
- accessibility service metadata
- boot receiver / foreground service registration

This scaffold keeps the structure ready for conversion into a full APK later.
