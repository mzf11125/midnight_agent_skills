# Address Formats

## Overview

Midnight Network uses **Bech32m** encoding for all addresses as of v4.0.0 (released with DApp Connector API v4.0.0 and Wallet API v4.0.0+).

## Bech32m Format

### Specification
- **Encoding**: Bech32m (improved version of Bech32)
- **Standard**: BIP 350
- **Prefix**: `mn_addr1` for addresses
- **Character Set**: `qpzry9x8gf2tvdw0s3jn54khce6mua7l`
- **Case**: Lowercase only

### Address Structure
```
mn_addr1<encoded_data><checksum>
```

**Example**:
```
mn_addr1asujt0dayj4pelgq97wv75hjhscqv9epmzzpapkf8sy8c87jhh9s6e0fs3
```

### Address Types

#### Shielded Address
- **Prefix**: `mn_addr1`
- **Purpose**: Private transactions
- **Length**: Variable (typically 63+ characters)
- **Example**: `mn_addr1asujt0dayj4pelgq97wv75hjhscqv9epmzzpapkf8sy8c87jhh9s6e0fs3`

#### Unshielded Address
- **Prefix**: `mn_addr1`
- **Purpose**: Public transactions
- **Length**: Variable
- **Example**: `mn_addr1qxyz...`

#### DUST Address
- **Prefix**: `mn_addr1`
- **Purpose**: Transaction fees (DUST tokens)
- **Length**: Variable
- **Example**: `mn_addr1dust...`

## Compatibility

### Version Requirements
- **DApp Connector API**: v4.0.0+
- **Wallet API**: v4.0.0+
- **Lace Wallet**: Latest version
- **Midnight.js**: Compatible versions

### Migration from Pre-v4.0.0
If using older address formats, update to Bech32m:
```typescript
// Old format (pre-v4.0.0) - DO NOT USE
const oldAddress = "0x1234...";

// New format (v4.0.0+) - USE THIS
const newAddress = "mn_addr1asujt0dayj4pelgq97wv75hjhscqv9epmzzpapkf8sy8c87jhh9s6e0fs3";
```

## Validation

### TypeScript Validation
```typescript
function isValidMidnightAddress(address: string): boolean {
  // Check prefix
  if (!address.startsWith('mn_addr1')) {
    return false;
  }
  
  // Check character set (Bech32m)
  const validChars = /^[qpzry9x8gf2tvdw0s3jn54khce6mua7l]+$/;
  const data = address.slice(8); // Remove 'mn_addr1' prefix
  
  if (!validChars.test(data)) {
    return false;
  }
  
  // Minimum length check
  if (address.length < 50) {
    return false;
  }
  
  return true;
}

// Usage
const address = "mn_addr1asujt0dayj4pelgq97wv75hjhscqv9epmzzpapkf8sy8c87jhh9s6e0fs3";
console.log(isValidMidnightAddress(address)); // true
```

### Regex Pattern
```regex
^mn_addr1[qpzry9x8gf2tvdw0s3jn54khce6mua7l]{50,}$
```

## API Usage

### DApp Connector API
```typescript
import { NetworkId } from '@midnight-ntwrk/midnight-js-network-id';

const connectedAPI = await window.midnight.wallet.connect(NetworkId('preprod'));

// Get addresses (all in Bech32m format)
const shieldedAddresses = await connectedAPI.getShieldedAddresses();
// Returns: { shieldedAddress: "mn_addr1..." }

const unshieldedAddress = await connectedAPI.getUnshieldedAddress();
// Returns: "mn_addr1..."

const dustAddress = await connectedAPI.getDustAddress();
// Returns: "mn_addr1..."
```

### Making Transfers
```typescript
import { nativeToken } from '@midnight-ntwrk/ledger';

// Recipient must be Bech32m format
const tx = await connectedAPI.makeTransfer([{
  kind: "unshielded",
  tokenType: nativeToken().raw,
  value: 10_000_000n, // 10 NIGHT
  recipient: "mn_addr1asujt0dayj4pelgq97wv75hjhscqv9epmzzpapkf8sy8c87jhh9s6e0fs3"
}]);
```

## Security Considerations

### Checksum Validation
Bech32m includes built-in checksum for error detection:
- Detects up to 4 character errors
- Prevents typos and transcription errors
- Validates address integrity

### Case Sensitivity
- **Always use lowercase**: `mn_addr1...`
- **Never use uppercase**: `MN_ADDR1...` (invalid)
- **Never mix case**: `Mn_Addr1...` (invalid)

### Display Guidelines
When displaying addresses to users:
```typescript
// Truncate for UI display
function truncateAddress(address: string): string {
  if (address.length <= 20) return address;
  return `${address.slice(0, 12)}...${address.slice(-8)}`;
}

// Example: "mn_addr1asuj...6e0fs3"
```

## Common Errors

### Invalid Prefix
```
Error: Invalid address format
```
**Cause**: Address doesn't start with `mn_addr1`  
**Solution**: Ensure address uses Bech32m format

### Invalid Characters
```
Error: Address contains invalid characters
```
**Cause**: Characters outside Bech32m character set  
**Solution**: Use only valid Bech32m characters

### Checksum Failure
```
Error: Address checksum validation failed
```
**Cause**: Address corrupted or typo  
**Solution**: Verify address is correct, re-copy if needed

## Tools & Libraries

### Bech32m Encoding/Decoding
```typescript
import { bech32m } from 'bech32';

// Encode
const words = bech32m.toWords(data);
const address = bech32m.encode('mn_addr1', words);

// Decode
const decoded = bech32m.decode(address);
console.log(decoded.prefix); // 'mn_addr1'
console.log(decoded.words);  // Uint8Array
```

### Midnight.js Utilities
```typescript
import { Address } from '@midnight-ntwrk/wallet-api';

// Type-safe address handling
const address: Address = "mn_addr1asujt0dayj4pelgq97wv75hjhscqv9epmzzpapkf8sy8c87jhh9s6e0fs3";
```

## Migration Checklist

If migrating from pre-v4.0.0:

- [ ] Update DApp Connector API to v4.0.0+
- [ ] Update Wallet API to v4.0.0+
- [ ] Update all address validation logic
- [ ] Replace old address format with Bech32m
- [ ] Test address encoding/decoding
- [ ] Update UI to display Bech32m addresses
- [ ] Update documentation and examples
- [ ] Test with Lace wallet (latest version)

## Resources

- BIP 350 Specification: https://github.com/bitcoin/bips/blob/master/bip-0350.mediawiki
- Bech32m Library: https://www.npmjs.com/package/bech32
- DApp Connector API: https://docs.midnight.network/api-reference/dapp-connector
- Wallet API: https://docs.midnight.network/api-reference/wallet-api
