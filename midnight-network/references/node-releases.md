# Node Release Notes

## Node v0.8.0-RC3 (Latest)

### Release Date
2026-02-13

### Features
- Improved consensus performance
- Enhanced peer discovery
- Optimized proof verification
- Better memory management

### Breaking Changes
- Configuration format updated
- API endpoint changes
- Database schema migration required

### Upgrade Instructions
1. Backup current configuration
2. Stop node
3. Install new version
4. Migrate configuration
5. Run database migrations
6. Start node

## Indexer Versions

### v2.1.4 (Recommended)
- Bug fixes
- Performance improvements
- Better error handling

### v2.1.0
- GraphQL API enhancements
- Query optimization
- New indexing strategies

### v2.0.0
- Initial release
- Core indexing functionality
- PostgreSQL support

## Compatibility Matrix

| Node Version | Indexer Version | Compatible |
|--------------|-----------------|------------|
| 0.8.0-RC3    | 2.1.4          | ✅         |
| 0.8.0-RC3    | 2.1.0          | ✅         |
| 0.8.0-RC3    | 2.0.0          | ⚠️         |

## Upgrade Procedures

### Minor Updates
1. Stop service
2. Install new version
3. Start service

### Major Updates
1. Review breaking changes
2. Backup data
3. Stop service
4. Install new version
5. Run migrations
6. Update configuration
7. Start service
8. Verify functionality
