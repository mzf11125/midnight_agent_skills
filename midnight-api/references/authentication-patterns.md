# Authentication Patterns

## Overview

Complete guide to implementing user authentication with Midnight Network wallets in DApps.

## Wallet-Based Authentication

### Basic Pattern

Users authenticate by connecting their Midnight wallet (similar to "Sign in with Ethereum"):

```typescript
import { connectWallet } from './wallet';

async function authenticateUser() {
  // 1. Connect wallet
  const api = await connectWallet();
  
  // 2. Get user's address
  const addresses = await api.getShieldedAddresses();
  const userAddress = addresses[0];
  
  // 3. User is now authenticated
  return {
    address: userAddress,
    api
  };
}
```

## Sign-In with Wallet

### Challenge-Response Pattern

Prove wallet ownership by signing a challenge:

```typescript
async function signInWithWallet() {
  // 1. Connect wallet
  const api = await connectWallet();
  const address = (await api.getShieldedAddresses())[0];
  
  // 2. Request challenge from backend
  const challenge = await fetch('/api/auth/challenge', {
    method: 'POST',
    body: JSON.stringify({ address })
  }).then(r => r.json());
  
  // 3. Sign challenge with wallet
  const signature = await api.signMessage(challenge.message);
  
  // 4. Verify signature on backend
  const session = await fetch('/api/auth/verify', {
    method: 'POST',
    body: JSON.stringify({
      address,
      challenge: challenge.message,
      signature
    })
  }).then(r => r.json());
  
  // 5. Store session token
  localStorage.setItem('authToken', session.token);
  
  return session;
}
```

### Backend Verification

```typescript
// Backend: Generate challenge
app.post('/api/auth/challenge', async (req, res) => {
  const { address } = req.body;
  
  // Generate random challenge
  const challenge = {
    message: `Sign in to MyDApp\nNonce: ${crypto.randomBytes(16).toString('hex')}`,
    timestamp: Date.now()
  };
  
  // Store challenge temporarily
  await redis.setex(`challenge:${address}`, 300, JSON.stringify(challenge));
  
  res.json(challenge);
});

// Backend: Verify signature
app.post('/api/auth/verify', async (req, res) => {
  const { address, challenge, signature } = req.body;
  
  // Get stored challenge
  const storedChallenge = await redis.get(`challenge:${address}`);
  if (!storedChallenge) {
    return res.status(400).json({ error: 'Challenge expired' });
  }
  
  // Verify signature
  const isValid = await verifySignature(challenge, signature, address);
  if (!isValid) {
    return res.status(401).json({ error: 'Invalid signature' });
  }
  
  // Create session
  const token = jwt.sign({ address }, process.env.JWT_SECRET, {
    expiresIn: '7d'
  });
  
  res.json({ token, address });
});
```

## Session Management

### Store Authentication State

```typescript
interface AuthState {
  address: string;
  token: string;
  api: ConnectedAPI;
  expiresAt: number;
}

class AuthManager {
  private state: AuthState | null = null;
  
  async signIn(): Promise<AuthState> {
    const session = await signInWithWallet();
    
    this.state = {
      address: session.address,
      token: session.token,
      api: session.api,
      expiresAt: Date.now() + 7 * 24 * 60 * 60 * 1000  // 7 days
    };
    
    // Persist to localStorage
    localStorage.setItem('auth', JSON.stringify({
      address: this.state.address,
      token: this.state.token,
      expiresAt: this.state.expiresAt
    }));
    
    return this.state;
  }
  
  async restore(): Promise<AuthState | null> {
    const stored = localStorage.getItem('auth');
    if (!stored) return null;
    
    const { address, token, expiresAt } = JSON.parse(stored);
    
    // Check expiration
    if (Date.now() > expiresAt) {
      this.signOut();
      return null;
    }
    
    // Reconnect wallet
    try {
      const api = await connectWallet();
      const addresses = await api.getShieldedAddresses();
      
      // Verify same address
      if (addresses[0] !== address) {
        this.signOut();
        return null;
      }
      
      this.state = { address, token, api, expiresAt };
      return this.state;
    } catch (error) {
      this.signOut();
      return null;
    }
  }
  
  signOut() {
    this.state = null;
    localStorage.removeItem('auth');
  }
  
  getState(): AuthState | null {
    return this.state;
  }
  
  isAuthenticated(): boolean {
    return this.state !== null && Date.now() < this.state.expiresAt;
  }
}

// Usage
const auth = new AuthManager();

// Sign in
await auth.signIn();

// Restore on page load
await auth.restore();

// Check auth
if (auth.isAuthenticated()) {
  const state = auth.getState();
  console.log('Logged in as:', state.address);
}
```

## Protected Routes

### React Example

```typescript
import { Navigate } from 'react-router-dom';

function ProtectedRoute({ children }) {
  const auth = useAuth();
  
  if (!auth.isAuthenticated()) {
    return <Navigate to="/login" />;
  }
  
  return children;
}

// Usage
<Route path="/dashboard" element={
  <ProtectedRoute>
    <Dashboard />
  </ProtectedRoute>
} />
```

### API Request Authentication

```typescript
async function authenticatedFetch(url: string, options: RequestInit = {}) {
  const auth = authManager.getState();
  
  if (!auth) {
    throw new Error('Not authenticated');
  }
  
  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${auth.token}`
    }
  });
}

// Usage
const data = await authenticatedFetch('/api/user/profile')
  .then(r => r.json());
```

## Multi-Wallet Support

### Handle Multiple Wallets

```typescript
async function selectWallet() {
  // Get all available wallets
  const wallets = Object.entries(window.midnight || {})
    .filter(([_, wallet]) => wallet.apiVersion)
    .map(([id, wallet]) => ({ id, ...wallet }));
  
  if (wallets.length === 0) {
    throw new Error('No wallets found');
  }
  
  // Show selection UI
  const selected = await showWalletSelector(wallets);
  
  // Connect to selected wallet
  const api = await selected.connect('testnet');
  
  // Store wallet preference
  localStorage.setItem('preferredWallet', selected.id);
  
  return api;
}

// Auto-connect to preferred wallet
async function autoConnect() {
  const preferred = localStorage.getItem('preferredWallet');
  
  if (preferred && window.midnight?.[preferred]) {
    try {
      return await window.midnight[preferred].connect('testnet');
    } catch (error) {
      console.warn('Failed to auto-connect:', error);
    }
  }
  
  return selectWallet();
}
```

## Account Switching

### Detect Account Changes

```typescript
class WalletMonitor {
  private currentAddress: string | null = null;
  private listeners: Set<(address: string) => void> = new Set();
  
  async start(api: ConnectedAPI) {
    this.currentAddress = (await api.getShieldedAddresses())[0];
    
    // Poll for address changes
    setInterval(async () => {
      const addresses = await api.getShieldedAddresses();
      const newAddress = addresses[0];
      
      if (newAddress !== this.currentAddress) {
        this.currentAddress = newAddress;
        this.notifyListeners(newAddress);
      }
    }, 5000);
  }
  
  onChange(listener: (address: string) => void) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }
  
  private notifyListeners(address: string) {
    this.listeners.forEach(listener => listener(address));
  }
}

// Usage
const monitor = new WalletMonitor();
await monitor.start(api);

monitor.onChange((newAddress) => {
  console.log('Account switched to:', newAddress);
  // Re-authenticate or update UI
  auth.signOut();
  window.location.reload();
});
```

## Role-Based Access Control

### On-Chain Roles

```typescript
// Smart contract with roles
interface Roles {
  admin: string[];
  moderator: string[];
  user: string[];
}

async function checkRole(address: string, role: string): Promise<boolean> {
  const contract = new Contract({
    address: contractAddress,
    network: 'testnet',
    wallet: api
  });
  
  const roles: Roles = await contract.query('getRoles');
  return roles[role]?.includes(address) || false;
}

// Middleware
async function requireRole(role: string) {
  const auth = authManager.getState();
  if (!auth) {
    throw new Error('Not authenticated');
  }
  
  const hasRole = await checkRole(auth.address, role);
  if (!hasRole) {
    throw new Error(`Requires ${role} role`);
  }
}

// Usage
async function deletePost(postId: string) {
  await requireRole('moderator');
  // Delete post
}
```

## Signature-Based Actions

### Sign Transactions

```typescript
async function signAndSubmit(action: string, params: any) {
  const auth = authManager.getState();
  if (!auth) throw new Error('Not authenticated');
  
  // Create transaction
  const tx = await auth.api.makeTransfer([{
    kind: 'shielded',
    tokenType: DUST_TOKEN_TYPE,
    value: 0n,  // No value transfer
    recipient: contractAddress
  }]);
  
  // Add action data
  const txWithData = {
    ...tx,
    data: JSON.stringify({ action, params })
  };
  
  // Submit
  const txHash = await auth.api.submitTransaction(txWithData);
  
  return txHash;
}
```

## Complete Authentication Flow

```typescript
import { AuthManager } from './auth';
import { WalletMonitor } from './monitor';

class DAppAuth {
  private auth = new AuthManager();
  private monitor = new WalletMonitor();
  
  async initialize() {
    // Try to restore session
    const restored = await this.auth.restore();
    
    if (restored) {
      console.log('Session restored:', restored.address);
      await this.monitor.start(restored.api);
      this.setupMonitoring();
      return restored;
    }
    
    return null;
  }
  
  async signIn() {
    const session = await this.auth.signIn();
    await this.monitor.start(session.api);
    this.setupMonitoring();
    return session;
  }
  
  signOut() {
    this.auth.signOut();
    window.location.href = '/';
  }
  
  private setupMonitoring() {
    // Handle account changes
    this.monitor.onChange((newAddress) => {
      console.log('Account changed:', newAddress);
      this.signOut();
    });
  }
  
  getUser() {
    return this.auth.getState();
  }
  
  isAuthenticated() {
    return this.auth.isAuthenticated();
  }
}

// App initialization
const dappAuth = new DAppAuth();

// On app load
await dappAuth.initialize();

// Sign in button
document.getElementById('signIn').onclick = async () => {
  await dappAuth.signIn();
  window.location.href = '/dashboard';
};

// Sign out button
document.getElementById('signOut').onclick = () => {
  dappAuth.signOut();
};

// Protected API calls
async function fetchUserData() {
  if (!dappAuth.isAuthenticated()) {
    throw new Error('Not authenticated');
  }
  
  const user = dappAuth.getUser();
  return authenticatedFetch('/api/user/data');
}
```

## Best Practices

### 1. Always Verify Signatures

```typescript
// ✅ CORRECT - verify on backend
const isValid = await verifySignature(message, signature, address);

// ❌ WRONG - trust client
const isValid = true;  // Never do this
```

### 2. Use Short-Lived Sessions

```typescript
// ✅ CORRECT - 7 day expiration
expiresIn: '7d'

// ❌ WRONG - no expiration
expiresIn: '999y'
```

### 3. Handle Wallet Disconnection

```typescript
// ✅ CORRECT - monitor connection
monitor.onChange(() => {
  auth.signOut();
  redirectToLogin();
});

// ❌ WRONG - assume always connected
```

### 4. Secure Token Storage

```typescript
// ✅ CORRECT - httpOnly cookie (backend)
res.cookie('token', token, { httpOnly: true, secure: true });

// ⚠️ OK - localStorage (frontend only)
localStorage.setItem('token', token);

// ❌ WRONG - exposed in URL
window.location.href = `/dashboard?token=${token}`;
```

## Resources

- **Wallet API**: See wallet-api.md
- **DApp Connector**: See dapp-connector-api.md
- **Integration Patterns**: See integration-patterns.md
- **Error Handling**: See error-codes.md
