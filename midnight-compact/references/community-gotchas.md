# Community Gotchas & Lessons Learned

Distilled from Midnight Aliit Fellowship articles at https://dev.to/midnight-aliit

---

## Compact Language Gotchas

### Circuits constrain, they don't execute
The most common mental model mistake. See `best-practices.md` for the full breakdown.

**One-liner:** You are not writing code that runs. You are describing valid states and proving you were in them.

### `export ledger` wrong usage patterns

```compact
// ❌ Block syntax (old, removed)
ledger {
  counter: Counter;
}

// ✅ Individual declarations
export ledger counter: Counter;
export ledger owner: Bytes<32>;
```

```compact
// ❌ Cell<T> is deprecated
export ledger value: Cell<Field>;

// ✅ Direct type
export ledger value: Field;
```

### `disclose()` is not optional

Circuit parameters are private by default. Storing them in public ledger state without `disclose()` is a **compile error**, not a runtime warning.

```compact
// ❌ Compile error: private value flowing into public state
registry.insert(user.bytes, profile_hash);

// ✅ Explicit disclosure
registry.insert(user.bytes, disclose(profile_hash));
```

Disclose as late as possible — directly before the ledger operation.

### `return` inside `for` loops is not allowed

Circuits are finite structures. Use `fold` for accumulation, `map` for transformation.

```compact
// ❌ Not allowed
for (let i = 0; i < 10; i++) {
  if (condition) return value;
}

// ✅ Use fold
const result = fold(0, items, (acc, item) => acc + item);
```

### Enum access uses `.` not `::`

```compact
// ❌ Rust-style
if (state == GameState::playing) { ... }

// ✅ Compact-style
if (state == GameState.playing) { ... }
```

### Witness functions have no body

```compact
// ❌ Wrong
witness get_key(): Bytes<32> {
  return local_secret_key();
}

// ✅ Correct — declaration only
witness local_secret_key(): Bytes<32>;
```

### Counter reads use `.read()` not `.value()`

```compact
// ❌
const val = counter.value();

// ✅
const val = counter.read();
```

---

## On-Chain Architecture Gotchas

### Struct reads are expensive

Every field in a struct is pulled into the circuit on lookup. A 6-field struct costs 6x more than a single value. Prefer flat maps.

### Block limits are hard limits, not gas costs

`BlockLimitExceeded` means your transaction literally cannot execute — not that it costs more. You're fitting inside a box, not paying for computation.

Approximate limits: ~1MB transaction size, ~1s compute time.

### The chain should not compute — it should verify

Move reward computation, scoring, ranking, and aggregation off-chain. Submit a Merkle root. Let users claim with proofs.

---

## SDK & Tooling Gotchas

### `WalletFacade.init()` hangs silently on standalone node (facade 2.x)

See `network-configuration.md` for full details and fix.

### Merkle path must use `findPathForLeaf`, not manual construction

The compact-runtime performs `instanceof` checks. A manually constructed `MerkleTreePath` JSON object will fail even with correct fields.

```typescript
// ❌ Fails instanceof check
const path = { value: [...], alignment: [...] };

// ✅ Use SDK method
const path = context.ledger.allowlist.findPathForLeaf(leaf);
```

### Proof server must be running before deployment

```bash
docker run -p 6300:6300 midnightnetwork/proof-server -- 'midnight-proof-server --network preprod'

# Verify
curl http://localhost:6300
# Expected: We're alive 🎉!
```

### Never commit your wallet seed

The `.env` file containing `SEED_ENV_VAR` must be in `.gitignore`. The seed signs all transactions.

### Merkle root invalidation under concurrent load

Every new leaf changes the root. Users generating proofs concurrently can have their proofs fail mid-generation if another transaction lands. Use `HistoricMerkleTree` for production apps with concurrent users.

---

## Sources

- [Circuits Are Not Functions](https://dev.to/midnight-aliit/circuits-are-not-functions-that-confusion-will-break-you-2do6) — Tushar Pamnani
- [Compact Is Not TypeScript](https://dev.to/midnight-aliit/compact-is-not-typescript-thats-the-whole-point-3d9) — Tushar Pamnani
- [I Hit Midnight's Block Limits Twice](https://dev.to/midnight-aliit/i-hit-midnights-block-limits-twice-and-it-forced-me-to-rethink-everything-1jki) — Tushar Pamnani
- [Working with Maps and Merkle Trees](https://dev.to/midnight-aliit/working-with-maps-and-merkle-trees-in-compact-40i3) — Nasihudeen Jimoh
- [Surviving Midnight SDK](https://dev.to/midnight-aliit/surviving-midnight-sdk-a-700-line-cure-for-the-silent-failure-problem-57p) — Fred Santana
- [Hands-on Deep Dive](https://dev.to/midnight-aliit/hands-on-midnight-deep-dive-start-building-smart-contracts-with-compact-1inb) — Haruki Kondo
- [You're Probably Using export ledger Wrong](https://dev.to/midnight-aliit/youre-probably-using-export-ledger-wrong-4j1c) — Tushar Pamnani
- [How Midnight Coordinates Two-Party Transfers](https://dev.to/midnight-aliit/how-midnight-coordinates-two-party-transfers-3dfh) — Tushar Pamnani
- [ZK Membership Proofs on Midnight](https://dev.to/midnight-aliit/zk-membership-proofs-on-midnight-1e29) — Tushar Pamnani
- [Advanced Compact Patterns for Web3 Developers](https://dev.to/midnight-aliit/advanced-compact-patterns-for-web3-developers-4m9i) — Nasihudeen Jimoh
- [I Spent Hours in the DOM So You Don't Have To](https://dev.to/midnight-aliit/i-spent-hours-in-the-dom-so-you-dont-have-to-e8h) — Tushar Pamnani
- [Troubleshooting Midnight Pre-Prod](https://dev.to/midnight-aliit/troubleshooting-midnight-pre-prod-a-week-in-the-trenches-2g4d) — Gutopro
- [How Midnight Verifies Tokens Without Computing It](https://dev.to/midnight-aliit/how-midnight-verifies-tokens-without-computing-it-5co6) — Tushar Pamnani
- [Building a Fungible Token in Compact](https://dev.to/midnight-aliit/building-a-fungible-token-in-compact-midnight-3nfh) — Neeraj Choubisa
- [DUST vs NIGHT](https://dev.to/midnight-aliit/dust-vs-night-rethinking-how-blockchains-handle-value-and-fees-586l) — Neeraj Choubisa
- [Midnight Mainnet Is Live](https://dev.to/midnight-aliit/midnight-mainnet-is-live-the-privacy-stack-just-got-real-4d65) — Barnabas
- [Selective Disclosure & Self-Managing DIDs for AI Agents](https://dev.to/midnight-aliit/selective-disclosure-self-managing-dids-for-ai-agents-3kcl) — Alex Pestchanker
- [Zero-Knowledge, Zero Friction](https://dev.to/midnight-aliit/zero-knowledge-zero-friction-automating-dapp-development-on-midnight-29f1) — Nasihudeen Jimoh
