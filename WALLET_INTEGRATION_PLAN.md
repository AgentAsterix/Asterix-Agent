# 🏦 Aster Finance Wallet Integration Plan

## 📋 Overview
Based on the Aster Finance API documentation analysis, here's the comprehensive plan for real wallet integration with trade execution, balance management, and user warnings.

## 🔐 Authentication Architecture

### API Key Authentication
- **Header**: `X-MBX-APIKEY` for API key
- **Signature**: HMAC SHA256 for signed endpoints (TRADE, USER_DATA)
- **Base URLs**: 
  - Spot: `https://sapi.asterdex.com`
  - Futures: `https://fapi.asterdex.com`

### Required Parameters for Signed Requests
```javascript
{
  "timestamp": 1617939110373,  // Current timestamp
  "signature": "HMAC_SHA256_signature",  // Request signature
  "recvWindow": 5000  // Optional: timing window
}
```

## 💰 Balance Management System

### Spot Account Balance
**Endpoint**: `GET /api/v1/account`
**Response Structure**:
```javascript
{
  "balances": [
    {
      "asset": "USDT",
      "free": "1000.50000000",    // Available balance
      "locked": "0.00000000"      // Locked in orders
    },
    {
      "asset": "BTC", 
      "free": "0.00123000",
      "locked": "0.00000000"
    }
  ]
}
```

### Futures Account Balance
**Endpoint**: `GET /fapi/v3/balance`
**Response Structure**:
```javascript
[
  {
    "asset": "USDT",
    "balance": "122607.35137903",        // Total balance
    "crossWalletBalance": "23.72469206", // Cross margin balance
    "availableBalance": "23.72469206",   // Available for trading
    "maxWithdrawAmount": "23.72469206"   // Max withdrawable
  }
]
```

## 🚨 User Warning System

### Critical Warnings to Implement

1. **Insufficient USDT Balance**
   ```
   ⚠️ Warning: Insufficient USDT balance!
   Required: 100 USDT | Available: 50 USDT
   Please deposit USDT or reduce trade size.
   ```

2. **No USDT in Wallet**
   ```
   🚫 Error: No USDT detected in your wallet!
   USDT is required for all trades on Aster Finance.
   Deposit USDT to start trading.
   ```

3. **High Leverage Risk**
   ```
   ⚠️ High Risk: 10x leverage detected!
   Liquidation Price: $25,000
   Recommended: Use lower leverage for safer trading.
   ```

4. **Position Limit Warning**
   ```
   ⚠️ Position Limit: You have 5/10 open positions
   Consider closing some positions before opening new ones.
   ```

## 🔄 Trade Execution Flow

### Spot Trading Flow
1. **Validate USDT Balance**
2. **Calculate Required USDT**
3. **Check Market Conditions**
4. **Execute Trade**
5. **Confirm Execution**
6. **Update Balance Cache**

### Futures Trading Flow
1. **Check Futures Balance**
2. **Validate Leverage Settings**
3. **Calculate Margin Requirements**
4. **Check Position Limits**
5. **Execute Position**
6. **Monitor Liquidation Risk**

## 📊 Real-Time Balance Monitoring

### Implementation Strategy
```python
class WalletManager:
    def __init__(self, api_key, api_secret):
        self.spot_client = AsterSpotClient(api_key, api_secret)
        self.futures_client = AsterFuturesClient(api_key, api_secret)
        self.balance_cache = {}
        self.last_update = 0
    
    async def get_usdt_balance(self, account_type="spot"):
        """Get USDT balance with caching"""
        if self._is_cache_stale():
            await self._refresh_balance()
        
        return self.balance_cache.get(f"{account_type}_usdt", 0.0)
    
    async def validate_trade_requirements(self, symbol, side, amount, leverage=1):
        """Validate if user can execute the trade"""
        usdt_balance = await self.get_usdt_balance()
        required_usdt = self._calculate_required_usdt(amount, leverage)
        
        if usdt_balance < required_usdt:
            return {
                "valid": False,
                "reason": "insufficient_usdt",
                "required": required_usdt,
                "available": usdt_balance
            }
        
        return {"valid": True}
```

## 🛡️ Safety Mechanisms

### Pre-Trade Validation
```python
async def validate_trade_safety(self, trade_params):
    checks = []
    
    # 1. USDT Balance Check
    usdt_balance = await self.get_usdt_balance()
    if usdt_balance < trade_params['required_usdt']:
        checks.append({
            "type": "insufficient_balance",
            "severity": "error",
            "message": f"Need {trade_params['required_usdt']} USDT, have {usdt_balance}"
        })
    
    # 2. Leverage Risk Check
    if trade_params.get('leverage', 1) > 5:
        checks.append({
            "type": "high_leverage",
            "severity": "warning", 
            "message": f"{trade_params['leverage']}x leverage detected - high liquidation risk"
        })
    
    # 3. Position Limit Check
    open_positions = await self.get_open_positions()
    if len(open_positions) >= 10:
        checks.append({
            "type": "position_limit",
            "severity": "warning",
            "message": "Max positions reached (10/10)"
        })
    
    return checks
```

## 🔧 Implementation Roadmap

### Phase 1: Enhanced Authentication
- [ ] Implement HMAC SHA256 signature generation
- [ ] Add timestamp validation
- [ ] Create secure API key storage
- [ ] Test authentication with sandbox

### Phase 2: Real Balance Integration  
- [ ] Implement spot balance fetching
- [ ] Implement futures balance fetching
- [ ] Create balance caching system
- [ ] Add real-time balance updates

### Phase 3: Trade Execution Engine
- [ ] Build spot order execution
- [ ] Build futures position opening
- [ ] Implement order status tracking
- [ ] Add trade confirmation system

### Phase 4: Safety & Warnings
- [ ] Implement USDT balance warnings
- [ ] Add leverage risk calculations
- [ ] Create position limit monitoring
- [ ] Build liquidation price alerts

### Phase 5: User Experience
- [ ] Real-time balance display in UI
- [ ] Trade confirmation dialogs
- [ ] Success/error notifications
- [ ] Trade history integration

## 🎯 Expected User Experience

### Wallet Connection Flow
1. User enters API key + secret
2. System validates credentials
3. Fetches all account balances
4. Displays USDT balances prominently
5. Shows available trading pairs

### Trade Execution Example
```
User: "Buy 100 USDT worth of BTC"

Agent: "🔍 Checking your wallet...

✅ USDT Balance: 1,250.50 USDT
✅ Required Amount: 100 USDT  
✅ After Trade: 1,150.50 USDT remaining

💼 Trade Preview:
- Pair: BTCUSDT
- Side: BUY
- Amount: 100 USDT
- Est. BTC: ~0.00364 BTC
- Fee: ~0.10 USDT

Confirm execution? [Yes/No]"
```

### Warning Examples
```
⚠️ Low Balance Warning:
"Your USDT balance (50 USDT) is low. Consider depositing more for continued trading."

🚫 Insufficient Funds:
"Cannot execute 200 USDT trade. Available: 150 USDT. Reduce amount or deposit more USDT."

📊 High Risk Alert:
"10x leverage = High liquidation risk! Liquidation at $26,500. Consider 2-3x for safer trading."
```

This comprehensive integration will make Agent Aster a real trading platform with professional-grade safety and user experience! 🚀
