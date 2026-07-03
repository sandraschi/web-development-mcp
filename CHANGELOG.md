
## [Unreleased] — 2026-06-14

### Added
- Tauri native wrapper (native/ directory) with bundle.resources + std::process::Command
- CUA-NSIS: just cua-nsis-test recipe, scripts/cua-smoke.py, scripts/cua-nsis-config.json
- Tauri CORS: tauri://localhost origins for WebView API access
- NSIS installer at dist/ and native/target/release/bundle/nsis/

### Changed
- Frontend API calls use absolute http://127.0.0.1:{port} URLs in production build
- CORS middleware includes allow_origin_regex for tauri.localhost
# Changelog

All notable changes to **Web Development MCP** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2026-01-19

### Added
- **🎨 Revolutionary AI Construction System**: Complete natural language to 3D object conversion
  - `manage_object_construction`: Universal object creation with LLM-generated Web Development scripts
  - `manage_object_repo`: Comprehensive object repository with versioning and search
  - FastMCP 2.14.3 sampling integration for conversational 3D creation
  - Multi-layer security validation (syntax, security scoring, sandbox execution)
  - Iterative refinement system with automatic failure recovery
- **🤖 Agentic Construction Pipeline**: End-to-end AI-powered 3D creation workflow
  - Natural language parsing with contextual understanding
  - LLM script generation with scene context and reference objects
  - Complexity levels (simple/standard/complex) and style presets (realistic/stylized/lowpoly/scifi)
  - Conversational refinement with max iteration limits
- **📚 MCP Resource System**: Structured script collections accessible via URIs
  - `Web Development://scripts/robots`, `Web Development://scripts/furniture`, `Web Development://scripts/rooms`
  - Mock script collections for robots, furniture, rooms, houses, vehicles, nature
  - Resource-based access for LLM-guided construction
- **🔧 Enhanced CLI**: Comprehensive command-line interface improvements
  - `--list-tools`: Display all available MCP tools with descriptions
  - `--show-config`: Show current configuration, environment, and system status
  - Improved help text with detailed examples and environment variables
  - Cross-platform compatibility fixes (removed Unicode emojis)
- **🛡️ Security Architecture**: Production-ready validation and sandboxing
  - Script validation pipeline with security scoring (0-100 scale)
  - Complexity assessment and resource limit enforcement
  - Safe execution environment with timeout and error containment

### Technical Improvements
- **FastMCP 2.14.3 Compliance**: Updated from 2.12.0 to 2.14.3 with sampling capabilities
- **Portmanteau Tool Consolidation**: Reduced tool explosion with versatile multi-operation tools
- **Context Preservation**: Maintains conversational state across LLM sampling calls
- **Import Error Fixes**: Resolved critical import issues for Context and ScriptValidationResult
- **Logger Standardization**: Replaced print statements with proper logging infrastructure
- **Cross-Platform Compatibility**: Windows/PowerShell environment optimizations

### Documentation
- **AI Construction Assessment**: Comprehensive technical analysis in `docs/AI_CONSTRUCTION_ASSESSMENT.md`
- **Enhanced README**: Emphasized revolutionary AI construction capabilities
- **MCPB Manifest Updates**: Added resources capability and tool registration
- **CLI Documentation**: Complete command reference with examples

## [0.2.0] - 2026-01-15

### Added
- **8 New Advanced VR Tools** for professional avatar workflows:
  - `Web Development_validation`: Pre-flight checks for VRChat/Resonite compatibility
  - `Web Development_splatting`: Gaussian Splatting (3DGS) import with proxy objects
  - `Web Development_materials_baking`: Shader conversion (toon→PBR) and material atlasing
  - `Web Development_vrm_metadata`: VRM-specific data (first person, visemes, spring bones)
  - `Web Development_atlasing`: Material/texture merging for mobile VR optimization
  - `Web Development_shapekeys`: Facial animation (visemes A/I/U/E/O, blink, expressions)
  - Extended `Web Development_rigging`: Weight transfer and humanoid bone mapping
  - `Web Development_export_presets`: Platform-specific exports (VRChat, Resonite, Unity)
- **Project AG Integration**: Complete VR avatar creation pipeline
- **Cross-Platform VR Support**: VRChat, Resonite, Unity, and VRM compatibility
- **Advanced Material System**: PBR conversion and draw call optimization
- **Professional Rigging Tools**: Weight painting automation and bone mapping
- **Gaussian Splatting Support**: Hybrid environment creation with collision meshes

### Features
- **VR Avatar Optimization Pipeline**:
  - Automatic polycount validation (VRChat: 70k, Resonite: 100k)
  - Bone count limits and naming conventions (256 max for VRChat)
  - Material atlasing for reduced draw calls
  - Unapplied transform detection and correction
- **Advanced Facial Animation**:
  - VRM-compliant viseme creation (A, I, U, E, O)
  - Blink animation setup with customizable intensity
  - Facial expression blending and weight management
  - Lip sync automation for voice acting
- **Cross-Platform Export System**:
  - VRChat presets (Unity scale 1.0, FBX format)
  - Resonite presets (GLTF format with collision support)
  - Legacy VRChat support (0.01 scale for old workflows)
  - Pre-export validation against platform limits
- **Gaussian Splatting Integration**:
  - Import `.ply`/`.spz` files with performance proxy objects
  - Collision mesh generation for walkable environments
  - Hybrid avatar + environment workflows
  - Resonite export with splat collision data
- **Professional Material Workflow**:
  - Cel-shaded to PBR texture baking
  - Material consolidation into atlas textures
  - VRM shader conversion to standard materials
  - Mobile VR optimization (reduce draw calls)

### Technical
- **FastMCP 2.13+ Portmanteau Pattern**: All tools use consolidated interfaces
- **Advanced Web Development API Integration**: Direct access to rigging, materials, and animation
- **Cross-Platform File Handling**: Pathlib-based operations for Windows/Linux/Mac
- **Comprehensive Error Recovery**: Custom exceptions for each tool category
- **Async/Await Architecture**: All operations properly async for FastMCP compatibility
- **Pydantic Validation**: Type-safe parameter validation for all operations
- **Logging Integration**: Detailed operation logging with loguru

---

## [0.1.0] - 2025-12-24

### Added
- Initial alpha release
- Basic Web Development connectivity
- Core MCP server implementation
- Development infrastructure (CI/CD, testing, documentation)

### Changed
- N/A (initial release)

### Fixed
- N/A (initial release)

### Security
- Basic security scanning implementation
- Input validation for MCP commands

---

## Release Process

### For Contributors
1. Update version in `src/web_development_mcp/__init__.py`
2. Update `CHANGELOG.md` with changes
3. Create pull request
4. CI/CD will handle the rest

### Automated Release
- Push to `main` triggers CI/CD pipeline
- Automatic version bumping available
- MCPB packages built and signed
- GitHub releases created with assets

### Version Types
- **PATCH** (`0.0.X`): Bug fixes, small improvements
- **MINOR** (`0.X.0`): New features, backwards compatible
- **MAJOR** (`X.0.0`): Breaking changes

---

## Types of Changes
- **Added** for new features
- **Changed** for changes in existing functionality
- **Deprecated** for soon-to-be removed features
- **Removed** for now removed features
- **Fixed** for any bug fixes
- **Security** in case of vulnerabilities

---

*This changelog follows the principles of [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).*

