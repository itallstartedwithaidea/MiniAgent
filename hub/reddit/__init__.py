"""reddit Ads hub connector. Translates reddit API into normalized schema."""

class redditConnector:
    """Connector for reddit advertising platform."""
    
    PLATFORM = "reddit"
    
    def __init__(self, credentials: dict):
        self.credentials = credentials
    
    async def list_campaigns(self) -> list:
        """List campaigns in normalized format."""
        raise NotImplementedError("reddit connector: coming in v0.3.0")
    
    async def get_performance(self, campaign_id: str, date_range: str = "LAST_30_DAYS") -> dict:
        """Get performance metrics in normalized format."""
        raise NotImplementedError("reddit connector: coming in v0.3.0")
    
    @staticmethod
    def normalize_cost(raw_cost, platform_format: str = "micros") -> float:
        """Normalize cost to dollars."""
        if platform_format == "micros":
            return raw_cost / 1_000_000
        return float(raw_cost)
