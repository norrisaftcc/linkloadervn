# Link Loader Asset Tracking Specification

**Author**: Julie (UI/Art)  
**Date**: Today  
**Version**: 1.0

## Overview

This document specifies the asset tracking system for Link Loader, designed to help artists and developers manage game assets efficiently.

## Asset Types

### 1. Visual Assets
- **Character Sprites**: .png files in `images/` directory
  - Format: `character_emotion.png` (e.g., `slim_happy.png`)
  - Variations: normal, happy, sad, angry, surprised, etc.
- **Backgrounds**: .png files in `images/` directory
  - Format: `bg_location.png` (e.g., `bg_desert_night.png`)
- **UI Elements**: .png files in `gui/` directory
  - Buttons, frames, boxes, etc.

### 2. Audio Assets
- **Music**: .ogg/.mp3 files in `audio/music/`
- **Sound Effects**: .ogg/.mp3 files in `audio/sfx/`
- **Voice**: .ogg files in `audio/voice/` (future)

### 3. Font Assets
- **Fonts**: .ttf/.otf files in `fonts/` directory

## Core Components

### 1. Asset Scanner

```python
class AssetScanner:
    """Scans game directory for all assets"""
    
    def __init__(self, game_path: str):
        self.game_path = Path(game_path)
        self.assets = {}
        self._scan_directories()
    
    def scan_images(self) -> Dict[str, AssetInfo]:
        """Scan for all image assets"""
        pass
    
    def scan_audio(self) -> Dict[str, AssetInfo]:
        """Scan for all audio assets"""
        pass
    
    def scan_fonts(self) -> Dict[str, AssetInfo]:
        """Scan for all font assets"""
        pass
    
    def get_asset_info(self, path: str) -> AssetInfo:
        """Get detailed info about an asset"""
        pass
```

### 2. Reference Analyzer

```python
class ReferenceAnalyzer:
    """Analyzes script references to assets"""
    
    def __init__(self, game_path: str):
        self.game = RenpyGame(game_path)
        self.references = defaultdict(list)
        self._analyze_references()
    
    def find_image_references(self) -> Dict[str, List[Reference]]:
        """Find all image references in scripts"""
        pass
    
    def find_audio_references(self) -> Dict[str, List[Reference]]:
        """Find all audio references in scripts"""
        pass
    
    def find_unused_assets(self) -> List[str]:
        """Find assets not referenced in scripts"""
        pass
    
    def find_missing_assets(self) -> List[str]:
        """Find referenced assets that don't exist"""
        pass
```

### 3. Asset Report Generator

```python
class AssetReportGenerator:
    """Generates comprehensive asset reports"""
    
    def __init__(self, scanner: AssetScanner, analyzer: ReferenceAnalyzer):
        self.scanner = scanner
        self.analyzer = analyzer
    
    def generate_inventory(self) -> AssetInventory:
        """Generate complete asset inventory"""
        pass
    
    def generate_usage_report(self) -> UsageReport:
        """Generate asset usage statistics"""
        pass
    
    def generate_missing_report(self) -> MissingReport:
        """Generate report of missing assets"""
        pass
    
    def export_manifest(self, format: str) -> None:
        """Export asset manifest in various formats"""
        pass
```

## Asset Tracking Features

### 1. Asset Inventory
- Complete list of all assets
- File sizes and dimensions
- Creation/modification dates
- Format information
- Metadata extraction

### 2. Usage Tracking
- Which scripts reference each asset
- How many times each asset is used
- Context of usage (character, scene, etc.)
- Related assets (variations)

### 3. Quality Checks
- Resolution consistency
- File size optimization
- Format standardization
- Naming convention compliance

### 4. Missing Asset Detection
- Scripts referencing non-existent files
- Placeholder assets still in use
- Broken references after renaming

## Report Formats

### 1. Asset Inventory Report

```yaml
# asset_inventory.yaml
images:
  characters:
    slim:
      - file: slim_normal.png
        size: 124KB
        dimensions: 400x600
        format: PNG
        created: 2024-01-15
        references: 12
      
    clipi:
      - file: clipi_normal.png
        size: 98KB
        dimensions: 400x600
        format: PNG
        created: 2024-01-16
        references: 8
        
  backgrounds:
    - file: bg_desert_night.png
      size: 854KB
      dimensions: 1920x1080
      format: PNG
      references: 3

audio:
  music:
    - file: desert_theme.ogg
      size: 3.2MB
      duration: 2:45
      format: OGG
      bitrate: 192kbps
      references: 1
```

### 2. Usage Report

```yaml
# asset_usage.yaml
used_assets:
  slim_normal.png:
    count: 12
    locations:
      - script.rpy:45
      - script.rpy:89
      - scene2.rpy:12
    contexts:
      - "show slim normal"
      - "show slim normal at left"
      
unused_assets:
  - slim_old_design.png
  - test_background.png
  - unused_music.ogg
  
missing_assets:
  - slim_shocked.png
    referenced_in:
      - script.rpy:234
  - bg_space_station.png
    referenced_in:
      - scene5.rpy:45
```

### 3. Quality Report

```yaml
# asset_quality.yaml
resolution_issues:
  inconsistent_character_sizes:
    - slim_happy.png: 400x600
    - slim_sad.png: 380x590
    recommendation: "Standardize to 400x600"
    
file_size_issues:
  oversized_images:
    - bg_desert_day.png: 12.5MB
      recommendation: "Compress or reduce resolution"
      
naming_issues:
  non_standard_names:
    - SlimHappy.png
      suggested: slim_happy.png
    - background-desert.png
      suggested: bg_desert.png
```

## Visual Dashboard

### 1. Asset Overview
```
┌─────────────────────────────────────┐
│          Asset Overview             │
├─────────────────┬─────────┬─────────┤
│ Type            │ Count   │ Size    │
├─────────────────┼─────────┼─────────┤
│ Characters      │ 45      │ 12.3 MB │
│ Backgrounds     │ 12      │ 45.6 MB │
│ UI Elements     │ 23      │ 3.4 MB  │
│ Music           │ 8       │ 32.1 MB │
│ Sound Effects   │ 15      │ 8.7 MB  │
└─────────────────┴─────────┴─────────┘
```

### 2. Usage Heatmap
- Visual representation of asset usage
- Color-coded by frequency
- Filterable by asset type
- Timeline view available

### 3. Character Asset Matrix
```
Character │ normal │ happy │ sad │ angry │ shocked
─────────┼────────┼───────┼─────┼───────┼─────────
Slim     │   ✓    │   ✓   │  ✓  │   ✓   │    ✗
Clipi    │   ✓    │   ✓   │  ✗  │   ✗   │    ✓
Terminal │   ✓    │   ✗   │  ✗  │   ✗   │    ✗
```

## Implementation Plan

### Phase 1: Asset Scanning (Days 1-3)
1. Implement directory scanner
2. Extract asset metadata
3. Create asset database
4. Build basic reporting

### Phase 2: Reference Analysis (Days 4-6)
1. Parse script references
2. Match references to assets
3. Identify missing assets
4. Track usage patterns

### Phase 3: Quality Checks (Days 7-8)
1. Implement resolution checks
2. Add file size analysis
3. Check naming conventions
4. Generate recommendations

### Phase 4: Reporting & UI (Days 9-10)
1. Create report generators
2. Build web dashboard
3. Add export functionality
4. Create API endpoints

## Usage Examples

### Command Line

```bash
# Scan all assets
python asset_tracker.py scan

# Generate usage report
python asset_tracker.py report --type usage

# Find missing assets
python asset_tracker.py check --missing

# Export manifest
python asset_tracker.py export --format json

# Check specific character
python asset_tracker.py analyze --character slim
```

### Integration

```python
# check_assets.py
from linkloader.assets import AssetTracker

tracker = AssetTracker("../game")

# Find unused assets
unused = tracker.find_unused_assets()
print(f"Found {len(unused)} unused assets")

# Check for missing assets
missing = tracker.find_missing_assets()
for asset in missing:
    print(f"Missing: {asset.path}")
    print(f"  Referenced in: {asset.references}")
```

## Automation Features

### 1. Pre-commit Hooks
```bash
#!/bin/bash
# Check for missing assets before commit
python asset_tracker.py check --missing --quiet || exit 1
```

### 2. CI/CD Integration
```yaml
# .github/workflows/assets.yml
name: Asset Checks
on: [push]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: python asset_tracker.py check --all
      - run: python asset_tracker.py report --format html
      - uses: actions/upload-artifact@v2
        with:
          name: asset-report
          path: asset_report.html
```

### 3. Scheduled Reports
- Daily asset inventory updates
- Weekly usage statistics
- Monthly quality reports
- Automated cleanup suggestions

## Future Enhancements

1. **Asset Optimization Pipeline**
   - Automatic image compression
   - Resolution standardization
   - Format conversion
   - Batch processing

2. **Version Control Integration**
   - Track asset history
   - Show who added/modified assets
   - Diff visualization for images
   - Branching support

3. **Cloud Asset Management**
   - Centralized asset repository
   - Collaborative approval workflow
   - Asset versioning
   - CDN integration

4. **AI-Powered Features**
   - Automatic asset tagging
   - Similar asset detection
   - Style consistency checking
   - Placeholder generation

5. **Performance Analytics**
   - Load time analysis
   - Memory usage tracking
   - Bundle size optimization
   - Lazy loading suggestions

## Conclusion

This asset tracking system will help the Link Loader team maintain a clean, organized asset pipeline, catch issues early, and optimize game resources effectively. By automating these checks, artists can focus on creating while the system handles organization and quality assurance.