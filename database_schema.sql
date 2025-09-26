-- Supabase Database Schema for Agent Aster (tryagentaster.com)
-- Production-ready schema with security and performance

-- Enable Row Level Security
ALTER DATABASE postgres SET "app.jwt_secret" TO 'your-jwt-secret-here';

-- Users table for authentication and sessions
CREATE TABLE IF NOT EXISTS public.users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    session_id VARCHAR(100) UNIQUE NOT NULL,
    session_name VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_demo_mode BOOLEAN DEFAULT false,
    
    -- Encrypted API credentials (use application-level encryption)
    aster_api_key_encrypted TEXT,
    aster_api_secret_encrypted TEXT,
    wallet_address TEXT,
    
    -- Session metadata
    last_active TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    user_agent TEXT,
    ip_address INET,
    
    -- Constraints
    CONSTRAINT valid_session_id CHECK (length(session_id) >= 10),
    CONSTRAINT valid_wallet_address CHECK (wallet_address ~ '^0x[a-fA-F0-9]{40}$' OR wallet_address IS NULL)
);

-- Chat history table
CREATE TABLE IF NOT EXISTS public.chat_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    session_id VARCHAR(100) NOT NULL,
    message_role VARCHAR(20) NOT NULL CHECK (message_role IN ('user', 'assistant', 'system')),
    message_content TEXT NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Metadata
    tokens_used INTEGER DEFAULT 0,
    response_time_ms INTEGER,
    
    -- Indexes for performance
    INDEX idx_chat_session_id (session_id),
    INDEX idx_chat_timestamp (timestamp DESC),
    INDEX idx_chat_user_id (user_id)
);

-- Trading history table
CREATE TABLE IF NOT EXISTS public.trades (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    session_id VARCHAR(100) NOT NULL,
    
    -- Trade details
    trade_type VARCHAR(20) NOT NULL CHECK (trade_type IN ('spot_buy', 'spot_sell', 'futures_long', 'futures_short')),
    symbol VARCHAR(20) NOT NULL,
    amount_usdt DECIMAL(18,6) NOT NULL,
    quantity DECIMAL(18,8),
    price DECIMAL(18,6),
    leverage INTEGER DEFAULT 1,
    slippage DECIMAL(5,4) DEFAULT 0.01,
    
    -- Order details
    order_id VARCHAR(100),
    order_status VARCHAR(20) DEFAULT 'pending' CHECK (order_status IN ('pending', 'filled', 'cancelled', 'failed')),
    
    -- Execution details
    executed_at TIMESTAMP WITH TIME ZONE,
    execution_price DECIMAL(18,6),
    fees_usdt DECIMAL(18,6) DEFAULT 0,
    
    -- Demo vs Real
    is_demo BOOLEAN DEFAULT false,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Indexes
    INDEX idx_trades_session_id (session_id),
    INDEX idx_trades_user_id (user_id),
    INDEX idx_trades_symbol (symbol),
    INDEX idx_trades_created_at (created_at DESC)
);

-- API rate limiting table
CREATE TABLE IF NOT EXISTS public.rate_limits (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    identifier VARCHAR(100) NOT NULL, -- IP address or session_id
    endpoint VARCHAR(100) NOT NULL,
    request_count INTEGER DEFAULT 1,
    window_start TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Composite unique constraint
    UNIQUE(identifier, endpoint, window_start),
    
    -- Auto-cleanup old entries (handled by application)
    INDEX idx_rate_limits_cleanup (window_start)
);

-- Demo wallets table (for demo mode users)
CREATE TABLE IF NOT EXISTS public.demo_wallets (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id VARCHAR(100) UNIQUE NOT NULL,
    
    -- Demo balances
    usdt_balance DECIMAL(18,6) DEFAULT 10000.00,
    available_balance DECIMAL(18,6) DEFAULT 8500.00,
    margin_used DECIMAL(18,6) DEFAULT 1500.00,
    unrealized_pnl DECIMAL(18,6) DEFAULT 0.00,
    
    -- Demo wallet metadata
    demo_address VARCHAR(42) DEFAULT '0x742d35Cc6486C3D5C2431d8f8a47e3B9b5f9D678',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- System configuration table
CREATE TABLE IF NOT EXISTS public.system_config (
    key VARCHAR(100) PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default system configuration
INSERT INTO public.system_config (key, value, description) VALUES
('maintenance_mode', 'false', 'Enable/disable maintenance mode'),
('max_sessions_per_ip', '10', 'Maximum sessions per IP address'),
('demo_starting_balance', '10000.00', 'Starting USDT balance for demo accounts'),
('api_rate_limit_per_minute', '60', 'API requests per minute per session'),
('max_trade_amount_usdt', '10000.00', 'Maximum trade amount in USDT'),
('supported_symbols', 'BTCUSDT,ETHUSDT,SOLUSDT,ADAUSDT,DOGEUSDT', 'Supported trading symbols')
ON CONFLICT (key) DO NOTHING;

-- Row Level Security Policies
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.chat_history ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.trades ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.demo_wallets ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only access their own data
CREATE POLICY "Users can access own data" ON public.users
    FOR ALL USING (session_id = current_setting('app.current_session_id', true));

CREATE POLICY "Users can access own chat history" ON public.chat_history
    FOR ALL USING (session_id = current_setting('app.current_session_id', true));

CREATE POLICY "Users can access own trades" ON public.trades
    FOR ALL USING (session_id = current_setting('app.current_session_id', true));

CREATE POLICY "Users can access own demo wallet" ON public.demo_wallets
    FOR ALL USING (session_id = current_setting('app.current_session_id', true));

-- Functions for maintenance
CREATE OR REPLACE FUNCTION cleanup_old_sessions()
RETURNS void AS $$
BEGIN
    -- Delete sessions inactive for more than 7 days
    DELETE FROM public.users 
    WHERE last_active < NOW() - INTERVAL '7 days';
    
    -- Delete old rate limit entries (older than 1 hour)
    DELETE FROM public.rate_limits 
    WHERE window_start < NOW() - INTERVAL '1 hour';
END;
$$ LANGUAGE plpgsql;

-- Create a scheduled job to run cleanup (if using pg_cron extension)
-- SELECT cron.schedule('cleanup-sessions', '0 2 * * *', 'SELECT cleanup_old_sessions();');

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_session_id ON public.users(session_id);
CREATE INDEX IF NOT EXISTS idx_users_last_active ON public.users(last_active);
CREATE INDEX IF NOT EXISTS idx_users_email ON public.users(email);

-- Comments for documentation
COMMENT ON TABLE public.users IS 'User sessions and encrypted API credentials';
COMMENT ON TABLE public.chat_history IS 'Chat conversation history between users and Agent Aster';
COMMENT ON TABLE public.trades IS 'Trading history including both demo and real trades';
COMMENT ON TABLE public.rate_limits IS 'API rate limiting tracking';
COMMENT ON TABLE public.demo_wallets IS 'Demo mode virtual wallets with starting balances';
COMMENT ON TABLE public.system_config IS 'System-wide configuration parameters';
